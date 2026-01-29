"""
RAG 检索模块 - 优化版
负责从向量数据库检索相关文档
集成本地Reranker、查询扩展、HyDE、缓存等高级技术
"""

import logging
from typing import List, Dict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from .local_reranker import get_reranker
from .query_cache import get_cache

logger = logging.getLogger(__name__)

# 常量配置
DEFAULT_NUM_EXPANDED_QUERIES = 2  # 默认扩展查询数量
SIMILARITY_THRESHOLD_RELAXATION = 0.9  # 查询扩展时相似度阈值放宽系数


def expand_query(query: str, api_key: str, num_queries: int = 3) -> List[str]:
    """
    查询扩展：生成多个相关查询以提升检索全面性
    
    Args:
        query: 原始查询
        api_key: API Key
        num_queries: 生成查询数量
    
    Returns:
        扩展后的查询列表（包含原始查询）
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.3
        )
        
        prompt = f"""作为搜索专家，请将以下查询扩展为{num_queries}个相关的搜索查询。

原始查询：{query}

要求：
1. 保持原意，从不同角度表达
2. 包含相关同义词和专业术语
3. 每行一个查询，不要编号

扩展查询："""
        
        response = llm.invoke(prompt)
        expanded = [line.strip() for line in response.content.split('\n') if line.strip()]
        
        # 确保包含原始查询
        if query not in expanded:
            expanded.insert(0, query)
        
        return expanded[:num_queries + 1]
        
    except Exception as e:
        # 降级：返回原始查询
        return [query]


def generate_hyde_document(query: str, api_key: str) -> str:
    """
    HyDE (Hypothetical Document Embeddings)
    生成假设性文档来改善检索质量
    
    Args:
        query: 查询文本
        api_key: API Key
    
    Returns:
        假设性文档
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.7
        )
        
        prompt = f"""请生成一个假设性的文档片段，该片段可能会回答以下问题。
文档应该简洁（200-300字）、专业、信息丰富。

问题：{query}

假设性文档："""
        
        response = llm.invoke(prompt)
        return response.content
        
    except Exception as e:
        return query  # 降级：使用原始查询


def retrieve_from_knowledge_base(
    query: str,
    vectorstore,
    k: int = 5,
    similarity_threshold: float = 0.7,
    use_reranker: bool = True,
    use_query_expansion: bool = False,
    use_hyde: bool = False,
    use_cache: bool = True,
    api_key: Optional[str] = None
) -> Dict:
    """
    从知识库检索相关内容（优化版）
    
    Args:
        query: 查询文本
        vectorstore: 向量数据库
        k: 返回的文档数量
        similarity_threshold: 相似度阈值
        use_reranker: 是否使用本地Reranker重排序
        use_query_expansion: 是否使用查询扩展
        use_hyde: 是否使用HyDE
        use_cache: 是否使用缓存
        api_key: API Key（查询扩展和HyDE需要）
    
    Returns:
        包含上下文、来源和元数据的字典
    """
    # 尝试从缓存获取
    if use_cache:
        cache = get_cache()
        cache_key_params = {
            "k": k,
            "threshold": similarity_threshold,
            "reranker": use_reranker,
            "expansion": use_query_expansion,
            "hyde": use_hyde
        }
        cached_result = cache.get(query, **cache_key_params)
        if cached_result:
            logger.info(f"缓存命中，跳过检索")
            return cached_result
    
    try:
        all_docs = []
        
        # 策略1: HyDE - 生成假设性文档
        if use_hyde and api_key:
            hyde_doc = generate_hyde_document(query, api_key)
            # 使用HyDE文档进行检索
            retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": k * 2}  # 获取更多候选
            )
            hyde_docs = retriever.invoke(hyde_doc)
            all_docs.extend(hyde_docs)
        
        # 策略2: 查询扩展 - 多角度检索
        if use_query_expansion and api_key:
            expanded_queries = expand_query(query, api_key, num_queries=DEFAULT_NUM_EXPANDED_QUERIES)
            
            for exp_query in expanded_queries:
                retriever = vectorstore.as_retriever(
                    search_type="similarity_score_threshold",
                    search_kwargs={
                        "k": k,
                        "score_threshold": similarity_threshold * SIMILARITY_THRESHOLD_RELAXATION  # 稍微放宽阈值
                    }
                )
                docs = retriever.invoke(exp_query)
                all_docs.extend(docs)
        
        # 策略3: 标准检索
        retriever = vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": k * 2 if use_reranker else k,  # Rerank时获取更多候选
                "score_threshold": similarity_threshold
            }
        )
        standard_docs = retriever.invoke(query)
        all_docs.extend(standard_docs)
        
        # 去重（基于内容）
        unique_docs = []
        seen_contents = set()
        
        for doc in all_docs:
            content = doc.page_content
            if content not in seen_contents:
                seen_contents.add(content)
                unique_docs.append(doc)
        
        if not unique_docs:
            return {
                "context": "",
                "sources": [],
                "num_chunks": 0,
                "chunks": []
            }
        
        # 策略4: Reranker重排序
        if use_reranker and len(unique_docs) > k:
            try:
                reranker = get_reranker()
                doc_contents = [doc.page_content for doc in unique_docs]
                reranked_with_scores = reranker.rerank(query, doc_contents, top_k=k)
                
                # 映射回原始文档
                content_to_doc = {doc.page_content: doc for doc in unique_docs}
                unique_docs = [content_to_doc[content] for content, score in reranked_with_scores]
            except Exception as e:
                # 降级：不使用Reranker，只取前k个
                unique_docs = unique_docs[:k]
        else:
            unique_docs = unique_docs[:k]
        
        # 构建上下文
        context_parts = []
        sources = []
        chunks = []
        
        for doc in unique_docs:
            source = doc.metadata.get('source', '未知来源')
            content = doc.page_content
            
            context_parts.append(f"[来源: {source}]\n{content}")
            sources.append(source)
            chunks.append({
                "content": content,
                "source": source,
                "metadata": doc.metadata
            })
        
        context = "\n\n---\n\n".join(context_parts)
        
        result = {
            "context": context,
            "sources": sources,
            "num_chunks": len(unique_docs),
            "chunks": chunks
        }
        
        # 存入缓存
        if use_cache:
            cache = get_cache()
            cache.set(query, result, **cache_key_params)
        
        return result
        
    except Exception as e:
        raise Exception(f"检索失败: {str(e)}")


def evaluate_coverage(
    query: str,
    kb_context: str,
    api_key: str
) -> Dict:
    """
    评估知识库内容对查询的覆盖度
    
    Args:
        query: 用户查询
        kb_context: 知识库检索到的上下文
        api_key: API Key
    
    Returns:
        包含覆盖度评估的字典
    """
    if not kb_context.strip():
        return {
            "coverage": 0,
            "needs_external": True,
            "gaps": ["知识库中没有相关内容"],
            "summary": "知识库未找到相关信息，需要外部研究",
            "confidence": "low"
        }
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0
        )
        
        evaluation_prompt = f"""
你是一个信息覆盖度评估专家。请评估知识库内容对用户问题的覆盖程度。

【用户问题】
{query}

【知识库内容】
{kb_context[:3000]}...

请按以下格式评估：

覆盖度: [0-100的数字]
需要外部补充: [是/否]
信息缺口: [列出主要缺失的信息点，用分号分隔；如果没有明显缺口，填写"无"]
置信度: [高/中/低]
总结: [一句话概括]

严格按照上述格式输出，不要添加其他内容。
"""
        
        response = llm.invoke(evaluation_prompt)
        result_text = response.content
        
        # 解析结果
        coverage = 50
        needs_external = True
        gaps = []
        summary = ""
        confidence = "medium"
        
        for line in result_text.split('\n'):
            line = line.strip()
            if line.startswith('覆盖度:') or line.startswith('覆盖度：'):
                try:
                    coverage = int(''.join(filter(str.isdigit, line)))
                    coverage = max(0, min(100, coverage))
                except (ValueError, TypeError):
                    pass
            elif line.startswith('需要外部补充:') or line.startswith('需要外部补充：'):
                needs_external = '是' in line
            elif line.startswith('信息缺口:') or line.startswith('信息缺口：'):
                gap_text = line.split(':', 1)[-1].split('：', 1)[-1].strip()
                if gap_text and gap_text not in ['无', '无明显缺口']:
                    gaps = [g.strip() for g in gap_text.split(';') if g.strip()]
            elif line.startswith('总结:') or line.startswith('总结：'):
                summary = line.split(':', 1)[-1].split('：', 1)[-1].strip()
            elif line.startswith('置信度:') or line.startswith('置信度：'):
                conf_text = line.split(':', 1)[-1].split('：', 1)[-1].strip()
                if '高' in conf_text:
                    confidence = "high"
                elif '低' in conf_text:
                    confidence = "low"
                else:
                    confidence = "medium"
        
        return {
            "coverage": coverage,
            "needs_external": needs_external,
            "gaps": gaps if gaps else ["部分信息需要补充"],
            "summary": summary or "知识库提供了部分相关信息",
            "confidence": confidence
        }
        
    except Exception as e:
        return {
            "coverage": 50,
            "needs_external": True,
            "gaps": ["无法准确评估"],
            "summary": f"评估过程出错: {str(e)}",
            "confidence": "low"
        }


def create_constrained_prompt(query: str, kb_context: str, kb_weight: int = 80) -> str:
    """
    创建受约束的研究提示词
    
    Args:
        query: 用户查询
        kb_context: 知识库上下文
        kb_weight: 知识库权重百分比
    
    Returns:
        构建好的提示词
    """
    prompt = f"""
你是一个严谨的研究分析师。请基于提供的内部知识库内容完成研究任务。

【核心约束】
1. 内部知识库内容的权重占 {kb_weight}%，必须作为主要依据
2. 所有核心论点必须来自知识库内容
3. 每个关键信息都要标注来源
4. 保持客观中立，不添加未经验证的信息

【内部知识库内容】
{kb_context}

【研究任务】
{query}

【输出要求】
请按以下结构生成研究报告：

## 执行摘要
[200字以内的核心总结]

## 核心发现
1. [第一个发现] - [来源: XXX]
2. [第二个发现] - [来源: XXX]
3. [第三个发现] - [来源: XXX]

## 详细分析
### [主题1]
[基于知识库的详细分析内容]
[来源: XXX]

### [主题2]
[基于知识库的详细分析内容]
[来源: XXX]

## 结论与建议
1. [结论1]
2. [结论2]
3. [建议1]
4. [建议2]

请严格遵循上述格式生成报告。
"""
    return prompt
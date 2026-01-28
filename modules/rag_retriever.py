"""
RAG 检索模块
负责从向量数据库检索相关文档
"""

from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI


def retrieve_from_knowledge_base(
    query: str,
    vectorstore,
    k: int = 5,
    similarity_threshold: float = 0.7
) -> Dict:
    """
    从知识库检索相关内容
    
    Args:
        query: 查询文本
        vectorstore: 向量数据库
        k: 返回的文档数量
        similarity_threshold: 相似度阈值
    
    Returns:
        包含上下文、来源和元数据的字典
    """
    try:
        # 创建检索器
        retriever = vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": k,
                "score_threshold": similarity_threshold
            }
        )
        
        # 检索相关文档
        docs = retriever.get_relevant_documents(query)
        
        if not docs:
            return {
                "context": "",
                "sources": [],
                "num_chunks": 0,
                "chunks": []
            }
        
        # 构建上下文
        context_parts = []
        sources = []
        chunks = []
        
        for doc in docs:
            source = doc.metadata.get('source', '未知来源')
            content = doc.page_content
            
            context_parts.append(
                f"[来源: {source}]
{content}"
            )
            sources.append(source)
            chunks.append({
                "content": content,
                "source": source,
                "metadata": doc.metadata
            })
        
        context = "\n\n---\n\n".join(context_parts)
        
        return {
            "context": context,
            "sources": sources,
            "num_chunks": len(docs),
            "chunks": chunks
        }
        
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
            "summary": "知识库未找到相关信息，需要外部研究"
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
信息缺口: [列出主要缺失的信息点，用分号分隔]
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
        
        for line in result_text.split('\n'):
            line = line.strip()
            if line.startswith('覆盖度:') or line.startswith('覆盖度：'):
                try:
                    coverage = int(''.join(filter(str.isdigit, line)))
                    coverage = max(0, min(100, coverage))
                except:
                    pass
            elif line.startswith('需要外部补充:') or line.startswith('需要外部补充：'):
                needs_external = '是' in line
            elif line.startswith('信息缺口:') or line.startswith('信息缺口：'):
                gap_text = line.split(':', 1)[-1].split('：', 1)[-1].strip()
                if gap_text and gap_text != '无':
                    gaps = [g.strip() for g in gap_text.split(';') if g.strip()]
            elif line.startswith('总结:') or line.startswith('总结：'):
                summary = line.split(':', 1)[-1].split('：', 1)[-1].strip()
        
        return {
            "coverage": coverage,
            "needs_external": needs_external,
            "gaps": gaps if gaps else ["部分信息需要补充"],
            "summary": summary or "知识库提供了部分相关信息"
        }
        
    except Exception as e:
        return {
            "coverage": 50,
            "needs_external": True,
            "gaps": ["无法准确评估"],
            "summary": f"评估过程出错: {str(e)}"
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
"""
混合研究模块
整合 RAG 检索和 Deep Research
"""

import time
from typing import Dict
import streamlit as st
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI

from .rag_retriever import (
    retrieve_from_knowledge_base,
    evaluate_coverage,
    create_constrained_prompt
)
from .utils import wait_for_interaction_completion

def hybrid_research(
    query: str,
    vectorstore,
    api_key: str,
    enable_external: bool = True,
    similarity_threshold: float = 0.7,
    kb_weight: int = 80,
    use_advanced_retrieval: bool = True
) -> Dict:
    """
    执行混合研究：RAG检索 + 可选的Deep Research（优化版）
    
    Args:
        query: 研究问题
        vectorstore: 向量数据库
        api_key: API Key
        enable_external: 是否启用外部研究
        similarity_threshold: 检索相似度阈值
        kb_weight: 知识库权重
        use_advanced_retrieval: 是否使用高级检索（Reranker + 查询扩展）
    
    Returns:
        研究结果字典
    """
    
    # Step 1: RAG 检索（使用高级策略）
    st.info("🔍 Step 1: 从知识库检索相关内容...")
    
    if use_advanced_retrieval:
        st.text("  ✨ 启用高级检索：本地Reranker + 查询扩展")
    
    kb_result = retrieve_from_knowledge_base(
        query=query,
        vectorstore=vectorstore,
        k=8,
        similarity_threshold=similarity_threshold,
        use_reranker=use_advanced_retrieval,  # 使用本地Reranker
        use_query_expansion=use_advanced_retrieval,  # 使用查询扩展
        use_hyde=False,  # HyDE可选，暂时关闭
        api_key=api_key
    )
    
    if kb_result['num_chunks'] == 0:
        st.warning("⚠️ 知识库中未找到相关内容，将依赖外部研究")
        kb_context = ""
        coverage_info = {
            "coverage": 0,
            "needs_external": True,
            "gaps": ["知识库无相关内容"],
            "summary": "完全依赖外部研究"
        }
    else:
        kb_context = kb_result['context']
        st.success(f"✅ 检索到 {kb_result['num_chunks']} 个相关文档块")
        
        # Step 2: 评估覆盖度
        st.info("📊 Step 2: 评估知识库覆盖度...")
        coverage_info = evaluate_coverage(query, kb_context, api_key)
        
        st.metric("知识库覆盖度", f"{coverage_info['coverage']}%")
        
        if coverage_info['gaps']:
            with st.expander("查看信息缺口"):
                for gap in coverage_info['gaps']:
                    st.markdown(f"- {gap}")
    
    # Step 3: 决定是否需要外部研究
    needs_external = (
        enable_external and
        coverage_info['needs_external'] and
        coverage_info['coverage'] < 90
    )
    
    external_info = None
    
    if needs_external:
        st.info("🌐 Step 3: 执行 Deep Research 补充外部信息...")
        
        try:
            client = genai.Client(api_key=api_key)
            
            # 构建外部研究提示
            gaps_text = "\n".join([f"- {gap}" for gap in coverage_info['gaps']])
            
            deep_research_prompt = f"""
基于内部知识库，我们已有以下信息：

{kb_context[:1500]}...

但仍需要补充以下方面的最新信息：
{gaps_text}

研究问题：
{query}

请进行深度网络研究，重点关注：
1. 补充知识库中缺失的信息
2. 提供最新的数据和趋势
3. 明确标注所有外部来源

输出格式要求：
- 简洁明了，重点突出
- 每个论点都要注明来源
- 按主题组织内容
"""
            
            # 创建交互
            interaction = client.interactions.create(
                agent="deep-research-pro-preview-12-2025",
                input=deep_research_prompt
            )
            
            # 等待完成
            completed_interaction = wait_for_interaction_completion(
                client, 
                interaction.id,
                timeout=300
            )
            
            # 提取结果
            if completed_interaction and hasattr(completed_interaction, 'outputs'):
                external_info = "\n".join([
                    output.text 
                    for output in completed_interaction.outputs 
                    if hasattr(output, 'text') and output.text
                ])
                
                if external_info:
                    st.success(f"✅ 外部研究完成，获得 {len(external_info)} 字补充内容")
                else:
                    st.warning("⚠️ 外部研究未返回有效内容")
            else:
                st.warning("⚠️ 外部研究未完成或超时")
                
        except Exception as e:
            st.error(f"❌ 外部研究失败: {str(e)}")
            external_info = None
    else:
        st.info("✅ Step 3: 知识库内容充分，跳过外部研究")
    
    # Step 4: 合成最终报告
    st.info("📝 Step 4: 合成最终研究报告...")
    
    final_report = synthesize_final_report(
        query=query,
        kb_context=kb_context,
        kb_sources=kb_result['sources'],
        external_info=external_info,
        kb_weight=kb_weight,
        api_key=api_key
    )
    
    st.success("✅ 研究完成！")
    
    return {
        "report": final_report,
        "internal_sources": kb_result['sources'],
        "has_external": external_info is not None,
        "kb_coverage": coverage_info['coverage'],
        "num_kb_chunks": kb_result['num_chunks']
    }

def synthesize_final_report(
    query: str,
    kb_context: str,
    kb_sources: list,
    external_info: str,
    kb_weight: int,
    api_key: str
) -> str:
    """
    合成最终研究报告
    
    Args:
        query: 研究问题
        kb_context: 知识库上下文
        kb_sources: 知识库来源列表
        external_info: 外部研究信息
        kb_weight: 知识库权重
        api_key: API Key
    
    Returns:
        最终报告文本
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=api_key,
            temperature=0.3
        )
        
        # 构建综合提示
        synthesis_prompt = f"""
你是一个专业的研究报告撰写专家。请基于以下信息生成高质量的研究报告。

【研究问题】
{query}

【主要来源：内部知识库（权重 {kb_weight}%）】
{kb_context if kb_context else "（知识库无相关内容）"}

"""
        
        if external_info:
            synthesis_prompt += f"""
【补充来源：外部研究（权重 {100-kb_weight}%）】
{external_info}

"""
        
        synthesis_prompt += """
【报告结构要求】
请严格按照以下结构生成报告：

## 📋 执行摘要
[200字以内，提炼核心要点]

## 🔍 核心发现
1. **[发现标题]**: [详细描述] `[来源标注]`
2. **[发现标题]**: [详细描述] `[来源标注]`
3. **[发现标题]**: [详细描述] `[来源标注]`
[至少3-5条核心发现]

## 📊 详细分析

### [主题1]
[基于证据的深入分析]
- 关键数据点
- 趋势分析
- 影响评估

`来源: [具体来源]`

### [主题2]
[基于证据的深入分析]
`来源: [具体来源]`

### [主题3]
[基于证据的深入分析]
`来源: [具体来源]`

"""
        
        if external_info:
            synthesis_prompt += """
## 🌐 外部补充信息
[来自网络研究的最新补充内容]
`来源: 外部研究`

"""
        
        synthesis_prompt += """
## 💡 结论与建议

### 主要结论
1. [结论1]
2. [结论2]
3. [结论3]

### 战略建议
1. **[建议1]**: [具体行动方案]
2. **[建议2]**: [具体行动方案]
3. **[建议3]**: [具体行动方案]

### 风险提示
- [风险点1]
- [风险点2]

---

【写作要求】
1. 以内部知识库内容为主要依据
2. 所有关键论点必须标注来源
3. 使用清晰的标题和子标题
4. 数据和事实必须准确
5. 保持客观中立的语气
6. 使用专业但易懂的语言
7. 适当使用 Emoji 增强可读性

现在请生成完整的研究报告：
"""
        
        response = llm.invoke(synthesis_prompt)
        report = response.content
        
        # 添加元数据
        metadata = "\n\n---\n\n## 📚 信息来源\n\n"
        metadata += "### 内部文档\n"
        for source in set(kb_sources):
            metadata += f"- 📄 {source}\n"
        
        if external_info:
            metadata += "\n### 外部研究\n"
            metadata += "- 🌐 Google Deep Research (网络实时搜索)\n"
        
        metadata += f"\n---\n\n*报告生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}*"
        
        return report + metadata
        
    except Exception as e:
        raise Exception(f"报告合成失败: {str(e)}")
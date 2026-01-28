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
    kb_weight: int = 80
) -> Dict:
    """
    执行混合研究：RAG检索 + 可选的Deep Research
    
    Args:
        query: 研究问题
        vectorstore: 向量数据库
        api_key: API Key
        enable_external: 是否启用外部研究
        similarity_threshold: 检索相似度阈值
        kb_weight: 知识库权重
    
    Returns:
        研究结果字典
    """
    
    # Step 1: RAG 检索
    st.info("🔍 Step 1: 从知识库检索相关内容...")
    
kb_result = retrieve_from_knowledge_base(
        query=query,
        vectorstore=vectorstore,
        k=8,
        similarity_threshol...
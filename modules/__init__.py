"""
知识库研究助手模块 - v2.0
集成最优技术方案
"""

from .document_processor import process_uploaded_files, get_vectorstore_stats
from .rag_retriever import retrieve_from_knowledge_base, evaluate_coverage
from .hybrid_research import hybrid_research
from .advanced_research_engine import advanced_hybrid_research
from .ppt_generator import generate_ppt
from .utils import init_session_state, clear_session_state
from .local_reranker import get_reranker, rerank_documents

__all__ = [
    'process_uploaded_files',
    'get_vectorstore_stats',
    'retrieve_from_knowledge_base',
    'evaluate_coverage',
    'hybrid_research',
    'advanced_hybrid_research',
    'generate_ppt',
    'init_session_state',
    'clear_session_state',
    'get_reranker',
    'rerank_documents'
]
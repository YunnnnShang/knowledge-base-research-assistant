"""
高级研究引擎测试
"""
import pytest


class TestAdvancedResearchEngine:
    """测试高级研究引擎"""
    
    def test_import_advanced_engine(self):
        """测试导入高级研究引擎"""
        from modules.advanced_research_engine import AdvancedResearchEngine, advanced_hybrid_research
        assert AdvancedResearchEngine is not None
        assert advanced_hybrid_research is not None
    
    def test_query_type_classification(self):
        """测试查询类型分类"""
        from modules.advanced_research_engine import AdvancedResearchEngine
        
        engine = AdvancedResearchEngine(api_key="test")
        
        # 测试不同类型的查询
        assert engine._get_query_type("什么是人工智能？") == "factual"
        assert engine._get_query_type("分析AI的发展趋势") == "analytical"
        assert engine._get_query_type("比较Python和Java") == "comparative"


class TestRAGRetrieverOptimization:
    """测试RAG检索优化"""
    
    def test_import_optimized_functions(self):
        """测试导入优化后的函数"""
        from modules.rag_retriever import (
            retrieve_from_knowledge_base,
            expand_query,
            generate_hyde_document
        )
        assert retrieve_from_knowledge_base is not None
        assert expand_query is not None
        assert generate_hyde_document is not None
    
    def test_retrieve_with_reranker_param(self):
        """测试检索函数支持reranker参数"""
        from modules.rag_retriever import retrieve_from_knowledge_base
        import inspect
        
        sig = inspect.signature(retrieve_from_knowledge_base)
        params = sig.parameters
        
        # 验证新参数存在
        assert 'use_reranker' in params
        assert 'use_query_expansion' in params
        assert 'use_hyde' in params


class TestModuleIntegration:
    """测试模块集成"""
    
    def test_all_modules_importable(self):
        """测试所有模块可以导入"""
        from modules import (
            process_uploaded_files,
            get_vectorstore_stats,
            retrieve_from_knowledge_base,
            evaluate_coverage,
            hybrid_research,
            advanced_hybrid_research,
            generate_ppt,
            init_session_state,
            clear_session_state,
            get_reranker,
            rerank_documents
        )
        
        # 验证所有函数存在
        assert all([
            callable(process_uploaded_files),
            callable(get_vectorstore_stats),
            callable(retrieve_from_knowledge_base),
            callable(evaluate_coverage),
            callable(hybrid_research),
            callable(advanced_hybrid_research),
            callable(generate_ppt),
            callable(init_session_state),
            callable(clear_session_state),
            callable(get_reranker),
            callable(rerank_documents)
        ])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

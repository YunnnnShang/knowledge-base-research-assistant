"""
基础测试 - 验证依赖和模块导入
"""
import pytest


class TestDependencies:
    """测试依赖版本"""
    
    def test_streamlit_version(self):
        """测试Streamlit版本"""
        import streamlit as st
        version = st.__version__
        major, minor = version.split('.')[:2]
        assert int(major) >= 1
        assert int(minor) >= 40, f"Streamlit version should be >= 1.40, got {version}"
    
    def test_langchain_version(self):
        """测试LangChain版本"""
        import langchain
        version = langchain.__version__
        major, minor = version.split('.')[:2]
        assert int(major) >= 0
        assert int(minor) >= 3, f"LangChain version should be >= 0.3, got {version}"
    
    def test_langchain_community_version(self):
        """测试LangChain Community版本（安全补丁）"""
        import langchain_community
        version = langchain_community.__version__
        parts = version.split('.')
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        # 必须 >= 0.3.27（修复XXE漏洞）
        assert (major, minor, patch) >= (0, 3, 27), \
            f"langchain-community must be >= 0.3.27 for security, got {version}"
    
    def test_langchain_core_version(self):
        """测试LangChain Core版本（安全补丁）"""
        import langchain_core
        version = langchain_core.__version__
        parts = version.split('.')
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        # 必须 >= 0.3.81（修复模板注入和序列化注入）
        assert (major, minor, patch) >= (0, 3, 81), \
            f"langchain-core must be >= 0.3.81 for security, got {version}"
    
    def test_chromadb_version(self):
        """测试ChromaDB版本"""
        import chromadb
        version = chromadb.__version__
        major, minor = version.split('.')[:2]
        assert int(major) >= 0
        assert int(minor) >= 5, f"ChromaDB version should be >= 0.5, got {version}"
    
    def test_pypdf_available(self):
        """测试pypdf可用（替代PyPDF2）"""
        try:
            import pypdf
            assert pypdf.__version__ >= "5.0.0"
        except ImportError:
            pytest.fail("pypdf not installed, should replace PyPDF2")
    
    def test_sentence_transformers_available(self):
        """测试sentence-transformers可用（本地Reranker）"""
        try:
            import sentence_transformers
            assert sentence_transformers.__version__ >= "3.0.0"
        except ImportError:
            pytest.fail("sentence-transformers not installed for local reranking")


class TestModuleImports:
    """测试模块导入"""
    
    def test_import_modules(self):
        """测试所有模块可以正常导入"""
        from modules import (
            init_session_state,
            clear_session_state,
            process_uploaded_files,
            get_vectorstore_stats,
            hybrid_research,
            generate_ppt
        )
        
        # 验证函数存在
        assert callable(init_session_state)
        assert callable(clear_session_state)
        assert callable(process_uploaded_files)
        assert callable(get_vectorstore_stats)
        assert callable(hybrid_research)
        assert callable(generate_ppt)
    
    def test_import_document_processor(self):
        """测试文档处理模块"""
        from modules import document_processor
        assert hasattr(document_processor, 'process_uploaded_files')
    
    def test_import_rag_retriever(self):
        """测试RAG检索模块"""
        from modules import rag_retriever
        assert hasattr(rag_retriever, 'retrieve_from_knowledge_base')
    
    def test_import_hybrid_research(self):
        """测试混合研究模块"""
        from modules import hybrid_research
        assert hasattr(hybrid_research, 'hybrid_research')
    
    def test_import_ppt_generator(self):
        """测试PPT生成模块"""
        from modules import ppt_generator
        assert hasattr(ppt_generator, 'generate_ppt')


class TestOptionalDependencies:
    """测试可选依赖"""
    
    def test_pdfplumber_available(self):
        """测试pdfplumber可用（高级表格提取）"""
        try:
            import pdfplumber
            assert pdfplumber.__version__ >= "0.11.0"
        except ImportError:
            pytest.skip("pdfplumber not installed (optional)")
    
    def test_docling_available(self):
        """测试docling可用（OCR和高级文档处理）"""
        try:
            import docling
            # Docling可能没有__version__属性
        except ImportError:
            pytest.skip("docling not installed (optional)")
    
    def test_pillow_available(self):
        """测试Pillow可用（图像处理）"""
        try:
            from PIL import Image
            # Pillow已安装
        except ImportError:
            pytest.skip("Pillow not installed (optional)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

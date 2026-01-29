"""
Reranker测试
"""
import pytest


class TestReranker:
    """测试Reranker功能"""
    
    def test_sentence_transformers_import(self):
        """测试sentence-transformers导入"""
        from sentence_transformers import CrossEncoder
        assert CrossEncoder is not None
    
    def test_reranker_model_available(self):
        """测试Reranker模型可用"""
        pytest.skip("Model download requires network, skipping in basic tests")
        # 在实际环境中需要下载模型
        # from sentence_transformers import CrossEncoder
        # model = CrossEncoder('BAAI/bge-reranker-v2-m3')
        # assert model is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

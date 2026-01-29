"""
测试新增的优化功能
- RAGAS评估
- 查询缓存
- ChromaDB优化
"""

import pytest
import os
from modules.rag_evaluation import RAGEvaluator, METRICS_DESCRIPTION
from modules.query_cache import QueryCache, get_cache


class TestRAGEvaluation:
    """测试RAG评估功能"""
    
    def test_rag_evaluator_initialization(self):
        """测试评估器初始化"""
        # 不使用真实API Key进行初始化测试
        evaluator = RAGEvaluator(api_key="test_key")
        assert evaluator is not None
        # 可能未安装RAGAS，所以只检查对象创建
    
    def test_metrics_description(self):
        """测试指标描述存在"""
        assert "faithfulness" in METRICS_DESCRIPTION
        assert "answer_relevancy" in METRICS_DESCRIPTION
        assert "context_precision" in METRICS_DESCRIPTION
        assert "context_recall" in METRICS_DESCRIPTION
        
        # 检查每个指标都有必要的字段
        for metric_name, metric_info in METRICS_DESCRIPTION.items():
            assert "name" in metric_info
            assert "description" in metric_info
            assert "range" in metric_info
            assert "good_threshold" in metric_info


class TestQueryCache:
    """测试查询缓存功能"""
    
    def test_cache_initialization(self):
        """测试缓存初始化"""
        cache = QueryCache(cache_dir=".cache/test", ttl=60)
        assert cache is not None
        assert cache.ttl == 60
    
    def test_cache_key_generation(self):
        """测试缓存键生成"""
        cache = QueryCache(cache_dir=".cache/test")
        
        # 相同查询应该生成相同的键
        key1 = cache._generate_cache_key("test query", k=5)
        key2 = cache._generate_cache_key("test query", k=5)
        assert key1 == key2
        
        # 不同查询应该生成不同的键
        key3 = cache._generate_cache_key("different query", k=5)
        assert key1 != key3
        
        # 不同参数应该生成不同的键
        key4 = cache._generate_cache_key("test query", k=10)
        assert key1 != key4
    
    def test_cache_get_set(self):
        """测试缓存读写"""
        cache = QueryCache(cache_dir=".cache/test", ttl=60)
        
        if not cache.enabled:
            pytest.skip("diskcache未安装，跳过测试")
        
        # 设置缓存
        test_query = "test query for caching"
        test_result = {
            "context": "test context",
            "sources": ["source1"],
            "num_chunks": 1
        }
        
        success = cache.set(test_query, test_result, k=5)
        assert success is True
        
        # 获取缓存
        cached_result = cache.get(test_query, k=5)
        assert cached_result is not None
        assert cached_result["context"] == "test context"
        assert cached_result["sources"] == ["source1"]
        
        # 不同参数应该无法获取
        cached_result2 = cache.get(test_query, k=10)
        assert cached_result2 is None
        
        # 清理
        cache.clear()
    
    def test_global_cache_singleton(self):
        """测试全局缓存单例模式"""
        cache1 = get_cache()
        cache2 = get_cache()
        
        # 应该是同一个实例
        assert cache1 is cache2
    
    def test_cache_stats(self):
        """测试缓存统计"""
        cache = QueryCache(cache_dir=".cache/test")
        stats = cache.get_stats()
        
        assert "enabled" in stats
        if stats["enabled"]:
            assert "count" in stats
            assert "directory" in stats


class TestChromaDBOptimization:
    """测试ChromaDB优化配置"""
    
    def test_chromadb_config_exists(self):
        """测试ChromaDB配置存在"""
        from config import CHROMADB_CONFIG
        
        assert "hnsw_space" in CHROMADB_CONFIG
        assert "hnsw_construction_ef" in CHROMADB_CONFIG
        assert "hnsw_search_ef" in CHROMADB_CONFIG
        assert "hnsw_M" in CHROMADB_CONFIG
    
    def test_cache_config_exists(self):
        """测试缓存配置存在"""
        from config import CACHE_CONFIG
        
        assert "enabled" in CACHE_CONFIG
        assert "cache_dir" in CACHE_CONFIG
        assert "ttl" in CACHE_CONFIG


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

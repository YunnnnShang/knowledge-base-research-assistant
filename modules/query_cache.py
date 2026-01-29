"""
查询缓存模块
使用diskcache实现轻量级、持久化的查询结果缓存
减少重复查询的API成本和延迟
"""

import hashlib
import json
from typing import Optional, Dict, Any
from datetime import datetime
import os


class QueryCache:
    """
    查询缓存器
    缓存RAG查询结果，减少重复查询成本
    
    特性：
    - 持久化存储（磁盘缓存）
    - 自动过期（TTL）
    - 智能缓存键（基于查询内容哈希）
    - 低开销（无需Redis等外部服务）
    """
    
    def __init__(self, cache_dir: str = ".cache/queries", ttl: int = 3600):
        """
        初始化缓存
        
        Args:
            cache_dir: 缓存目录
            ttl: 缓存有效期（秒），默认1小时
        """
        self.cache_dir = cache_dir
        self.ttl = ttl
        self.cache = None
        self.enabled = False
        
        try:
            from diskcache import Cache
            
            # 确保缓存目录存在
            os.makedirs(cache_dir, exist_ok=True)
            
            # 初始化缓存
            self.cache = Cache(cache_dir)
            self.enabled = True
            
        except ImportError:
            print("⚠️ diskcache未安装，缓存功能不可用。运行: pip install diskcache")
        except Exception as e:
            print(f"⚠️ 缓存初始化失败: {str(e)}")
    
    def _generate_cache_key(self, query: str, **kwargs) -> str:
        """
        生成缓存键
        基于查询内容和参数的哈希值
        
        Args:
            query: 查询文本
            **kwargs: 其他影响结果的参数
        
        Returns:
            缓存键（哈希值）
        """
        # 构建完整的缓存内容
        cache_content = {
            "query": query.strip().lower(),  # 标准化查询
            **kwargs
        }
        
        # 生成哈希
        content_str = json.dumps(cache_content, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()
    
    def get(self, query: str, **kwargs) -> Optional[Dict[Any, Any]]:
        """
        从缓存获取查询结果
        
        Args:
            query: 查询文本
            **kwargs: 查询参数
        
        Returns:
            缓存的结果，如果不存在或已过期则返回None
        """
        if not self.enabled or not self.cache:
            return None
        
        try:
            cache_key = self._generate_cache_key(query, **kwargs)
            cached_data = self.cache.get(cache_key)
            
            if cached_data:
                # 检查是否过期
                if "timestamp" in cached_data:
                    age = (datetime.now() - cached_data["timestamp"]).total_seconds()
                    if age > self.ttl:
                        # 过期，删除缓存
                        self.cache.delete(cache_key)
                        return None
                
                return cached_data.get("result")
            
            return None
            
        except Exception as e:
            print(f"⚠️ 缓存读取失败: {str(e)}")
            return None
    
    def set(self, query: str, result: Dict[Any, Any], **kwargs) -> bool:
        """
        将查询结果存入缓存
        
        Args:
            query: 查询文本
            result: 查询结果
            **kwargs: 查询参数
        
        Returns:
            是否成功存入
        """
        if not self.enabled or not self.cache:
            return False
        
        try:
            cache_key = self._generate_cache_key(query, **kwargs)
            
            cached_data = {
                "result": result,
                "timestamp": datetime.now(),
                "query": query,
                "params": kwargs
            }
            
            # 存入缓存（使用TTL）
            self.cache.set(cache_key, cached_data, expire=self.ttl)
            return True
            
        except Exception as e:
            print(f"⚠️ 缓存写入失败: {str(e)}")
            return False
    
    def clear(self) -> bool:
        """
        清空所有缓存
        
        Returns:
            是否成功清空
        """
        if not self.enabled or not self.cache:
            return False
        
        try:
            self.cache.clear()
            return True
        except Exception as e:
            print(f"⚠️ 缓存清空失败: {str(e)}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息
        
        Returns:
            统计信息字典
        """
        if not self.enabled or not self.cache:
            return {
                "enabled": False,
                "size": 0,
                "count": 0
            }
        
        try:
            return {
                "enabled": True,
                "size": self.cache.volume(),  # 缓存大小（字节）
                "count": len(self.cache),     # 缓存条目数
                "directory": self.cache_dir,
                "ttl": self.ttl
            }
        except Exception as e:
            return {
                "enabled": True,
                "error": str(e)
            }


# 全局缓存实例（单例模式）
_global_cache: Optional[QueryCache] = None


def get_cache(cache_dir: str = ".cache/queries", ttl: int = 3600) -> QueryCache:
    """
    获取全局缓存实例（单例）
    
    Args:
        cache_dir: 缓存目录
        ttl: 缓存有效期（秒）
    
    Returns:
        QueryCache实例
    """
    global _global_cache
    
    if _global_cache is None:
        _global_cache = QueryCache(cache_dir=cache_dir, ttl=ttl)
    
    return _global_cache


def cached_query(func):
    """
    查询缓存装饰器
    自动缓存函数结果
    
    使用示例：
    @cached_query
    def my_rag_function(query: str, vectorstore, api_key: str):
        # ... 执行查询
        return result
    """
    def wrapper(query: str, *args, **kwargs):
        # 获取缓存
        cache = get_cache()
        
        # 尝试从缓存获取
        cached_result = cache.get(query, **kwargs)
        if cached_result is not None:
            print(f"✓ 缓存命中: {query[:50]}...")
            return cached_result
        
        # 执行实际查询
        result = func(query, *args, **kwargs)
        
        # 存入缓存
        cache.set(query, result, **kwargs)
        
        return result
    
    return wrapper

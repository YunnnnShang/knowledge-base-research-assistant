"""
测试世界级Prompt工程模块
"""

import pytest
from modules.elite_prompts import (
    WorldClassPromptFramework,
    McKinseyStylePrompts,
    BCGStylePrompts,
    GartnerStylePrompts,
    AcademicResearchPrompts,
    EnhancedCoverageEvaluation,
    EnhancedSynthesisPrompts,
    get_elite_prompt,
    get_best_prompt_for_query_type
)


class TestWorldClassPromptFramework:
    """测试世界级Prompt框架"""
    
    def test_build_prompt_basic(self):
        """测试基本Prompt构建"""
        prompt = WorldClassPromptFramework.build_prompt(
            role="测试专家",
            task="测试任务",
            context="测试上下文",
            constraints=["约束1", "约束2"],
            output_format="输出格式"
        )
        
        assert "测试专家" in prompt
        assert "测试任务" in prompt
        assert "测试上下文" in prompt
        assert "约束1" in prompt
        assert "输出格式" in prompt
    
    def test_build_prompt_with_thinking(self):
        """测试包含思维过程的Prompt"""
        prompt = WorldClassPromptFramework.build_prompt(
            role="专家",
            task="任务",
            context="上下文",
            constraints=["约束"],
            output_format="格式",
            thinking_process="思维步骤"
        )
        
        assert "思维步骤" in prompt
        assert "分析思路" in prompt


class TestMcKinseyStylePrompts:
    """测试McKinsey式Prompt"""
    
    def test_strategic_analysis_prompt(self):
        """测试战略分析Prompt"""
        query = "如何提升市场竞争力？"
        context = "公司当前市场份额为15%，年增长率为20%"
        
        prompt = McKinseyStylePrompts.strategic_analysis_prompt(query, context)
        
        # 检查McKinsey关键元素
        assert "McKinsey" in prompt
        assert "MECE" in prompt
        assert "金字塔原理" in prompt
        assert "So What" in prompt
        assert query in prompt
        assert "Executive Summary" in prompt or "执行摘要" in prompt


class TestBCGStylePrompts:
    """测试BCG式Prompt"""
    
    def test_growth_strategy_prompt(self):
        """测试成长策略Prompt"""
        query = "如何实现业务增长？"
        context = "当前业务增长放缓"
        
        prompt = BCGStylePrompts.growth_strategy_prompt(query, context)
        
        assert "BCG" in prompt
        assert "增长" in prompt or "成长" in prompt
        assert query in prompt


class TestGartnerStylePrompts:
    """测试Gartner式Prompt"""
    
    def test_technology_assessment_prompt(self):
        """测试技术评估Prompt"""
        query = "AI技术的成熟度如何？"
        context = "AI正在快速发展"
        
        prompt = GartnerStylePrompts.technology_assessment_prompt(query, context)
        
        assert "Gartner" in prompt
        assert "Hype Cycle" in prompt or "成熟度" in prompt
        assert query in prompt


class TestAcademicResearchPrompts:
    """测试学术研究式Prompt"""
    
    def test_systematic_review_prompt(self):
        """测试系统性综述Prompt"""
        query = "机器学习在医疗领域的应用"
        context = "多项研究表明机器学习可以..."
        
        prompt = AcademicResearchPrompts.systematic_review_prompt(query, context)
        
        assert "MIT" in prompt or "Stanford" in prompt
        assert "文献综述" in prompt or "systematic" in prompt.lower()
        assert "证据" in prompt
        assert query in prompt


class TestEnhancedCoverageEvaluation:
    """测试增强覆盖度评估Prompt"""
    
    def test_advanced_coverage_prompt(self):
        """测试高级覆盖度评估"""
        query = "什么是RAG技术？"
        context = "RAG是检索增强生成技术..."
        
        prompt = EnhancedCoverageEvaluation.advanced_coverage_prompt(query, context)
        
        assert "覆盖度" in prompt
        assert "问题分解" in prompt
        assert query in prompt
        assert "置信度" in prompt


class TestEnhancedSynthesisPrompts:
    """测试增强合成Prompt"""
    
    def test_world_class_synthesis_factual(self):
        """测试事实型查询的合成Prompt"""
        prompt = EnhancedSynthesisPrompts.world_class_synthesis_prompt(
            query="什么是人工智能？",
            query_type="factual",
            kb_context="人工智能是...",
            kb_weight=80
        )
        
        assert "McKinsey" in prompt or "学术" in prompt
        assert "核心定义" in prompt
        assert "关键特征" in prompt
    
    def test_world_class_synthesis_comparative(self):
        """测试对比型查询的合成Prompt"""
        prompt = EnhancedSynthesisPrompts.world_class_synthesis_prompt(
            query="Python vs Java",
            query_type="comparative",
            kb_context="Python和Java各有优势",
            kb_weight=70
        )
        
        assert "BCG" in prompt or "Gartner" in prompt
        assert "对比" in prompt or "比较" in prompt
    
    def test_world_class_synthesis_with_external(self):
        """测试包含外部信息的合成"""
        prompt = EnhancedSynthesisPrompts.world_class_synthesis_prompt(
            query="AI趋势分析",
            query_type="analytical",
            kb_context="内部数据...",
            kb_weight=60,
            external_info="外部研究显示..."
        )
        
        assert "McKinsey" in prompt
        assert "外部研究" in prompt


class TestGetElitePrompt:
    """测试便捷函数"""
    
    def test_get_elite_prompt_mckinsey(self):
        """测试获取McKinsey式Prompt"""
        prompt = get_elite_prompt(
            prompt_type='mckinsey_strategic',
            query="战略分析",
            context="背景信息"
        )
        
        assert isinstance(prompt, str)
        assert len(prompt) > 100
        assert "McKinsey" in prompt
    
    def test_get_elite_prompt_invalid_type(self):
        """测试无效的Prompt类型"""
        with pytest.raises(ValueError):
            get_elite_prompt(
                prompt_type='invalid_type',
                query="test",
                context="test"
            )
    
    def test_get_elite_prompt_world_class_synthesis(self):
        """测试world_class_synthesis的kwargs处理"""
        prompt = get_elite_prompt(
            prompt_type='world_class_synthesis',
            query="测试查询",
            context="测试上下文",
            query_type='analytical',
            kb_weight=75,
            external_info="外部信息"
        )
        
        assert isinstance(prompt, str)
        assert len(prompt) > 100
        assert "analytical" in prompt or "分析" in prompt
    
    def test_get_elite_prompt_world_class_synthesis_defaults(self):
        """测试world_class_synthesis使用默认kwargs"""
        prompt = get_elite_prompt(
            prompt_type='world_class_synthesis',
            query="测试",
            context="上下文"
            # 不提供可选kwargs，应使用默认值
        )
        
        assert isinstance(prompt, str)
        assert len(prompt) > 100
    
    def test_get_best_prompt_for_query_type(self):
        """测试根据查询类型获取最佳Prompt"""
        # 事实型
        result = get_best_prompt_for_query_type('factual')
        assert result == 'mckinsey_strategic'
        
        # 对比型
        result = get_best_prompt_for_query_type('comparative')
        assert result == 'bcg_growth'
        
        # 技术型
        result = get_best_prompt_for_query_type('technical')
        assert result == 'gartner_tech'
        
        # 学术型
        result = get_best_prompt_for_query_type('academic')
        assert result == 'academic_review'
        
        # 默认
        result = get_best_prompt_for_query_type('unknown')
        assert result == 'mckinsey_strategic'


class TestPromptQuality:
    """测试Prompt质量"""
    
    def test_prompt_length(self):
        """测试Prompt长度合理"""
        query = "测试问题"
        context = "测试上下文" * 100
        
        # 测试各类Prompt长度
        prompts = [
            McKinseyStylePrompts.strategic_analysis_prompt(query, context),
            BCGStylePrompts.growth_strategy_prompt(query, context),
            GartnerStylePrompts.technology_assessment_prompt(query, context),
            AcademicResearchPrompts.systematic_review_prompt(query, context),
        ]
        
        for prompt in prompts:
            # 确保prompt不为空且有合理长度
            assert len(prompt) > 500
            assert len(prompt) < 50000  # 不超过token限制
    
    def test_prompt_structure(self):
        """测试Prompt结构完整"""
        query = "测试"
        context = "上下文"
        
        prompt = McKinseyStylePrompts.strategic_analysis_prompt(query, context)
        
        # 检查关键结构元素
        assert "# 角色定位" in prompt or "角色" in prompt
        assert "# 任务" in prompt or "任务" in prompt
        assert "# 上下文" in prompt or "上下文" in prompt
        assert "# 约束条件" in prompt or "约束" in prompt
        assert "# 输出格式" in prompt or "输出" in prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

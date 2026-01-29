"""
高级提示词模块
提供各种场景的优化提示词模板
"""

from typing import Dict, List

class PromptTemplates:
    """提示词模板管理类"""
    
    @staticmethod
    def coverage_evaluation_prompt(query: str, kb_context: str) -> str:
        """知识库覆盖度评估提示词"""
        return f"""你是一个信息覆盖度评估专家。请评估知识库内容对用户问题的覆盖程度。

【用户问题】
{query}

【知识库内容】
{kb_context[:3000]}...

请按以下格式评估：

覆盖度: [0-100的数字]
需要外部补充: [是/否]
信息缺口: [列出主要缺失的信息点，用分号分隔]
总结: [一句话概括]

严格按照上述格式输出，不要添加其他内容。"""

    @staticmethod
    def deep_research_prompt(query: str, kb_context: str, gaps: List[str]) -> str:
        """Deep Research 补充提示词"""
        gaps_text = "\n".join([f"- {gap}" for gap in gaps])
        
        return f"""基于内部知识库，我们已有以下信息：

{kb_context[:1500]}...

但仍需要补充以下方面的最新信息：
{gaps_text}

研究问题：
{query}

请进行深度网络研究，重点关注：
1. 补充知识库中缺失的信息
2. 提供最新的数据和趋势（2024-2025年）
3. 明确标注所有外部来源
4. 关注行业权威报告和学术研究

输出格式要求：
- 简洁明了，重点突出
- 每个论点都要注明来源
- 按主题组织内容
- 使用数据和事实支撑观点"""

    @staticmethod
    def synthesis_prompt(query: str, kb_context: str, kb_weight: int, external_info: str = None) -> str:
        """最终报告合成提示词"""
        prompt = f"""你是一个专业的研究报告撰写专家。请基于以下信息生成高质量的研究报告。

【研究问题】
{query}

【主要来源：内部知识库（权重 {kb_weight}%）】
{kb_context if kb_context else "（知识库无相关内容）"}

"""
        
        if external_info:
            prompt += f"""【补充来源：外部研究（权重 {100-kb_weight}%）】
{external_info}

"""
        
        prompt += """【报告结构要求】
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
            prompt += """## 🌐 外部补充信息
[来自网络研究的最新补充内容]
`来源: 外部研究`

"""
        
        prompt += """## 💡 结论与建议

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

现在请生成完整的研究报告："""
        
        return prompt

    @staticmethod
    def query_expansion_prompt(query: str) -> str:
        """查询扩展提示词"""
        return f"""作为搜索专家，请将以下用户查询扩展为3-5个相关的搜索查询，以提高检索全面性。

原始查询：{query}

要求：
1. 保持原意，但从不同角度表达
2. 包含相关的同义词和专业术语
3. 考虑不同的提问方式
4. 每行一个查询

扩展查询："""

    @staticmethod
    def context_compression_prompt(context: str, query: str, max_length: int = 2000) -> str:
        """上下文压缩提示词"""
        return f"""请压缩以下上下文，保留与问题最相关的信息，控制在{max_length}字以内。

【问题】
{query}

【原始上下文】
{context}

【压缩要求】
1. 保留所有关键事实和数据
2. 删除冗余和不相关内容
3. 保持逻辑连贯性
4. 标注信息来源

压缩后的上下文："""

    @staticmethod
    def multi_hop_reasoning_prompt(query: str, contexts: List[str]) -> str:
        """多跳推理提示词"""
        context_text = "\n\n---\n\n".join([f"文档{i+1}:\n{ctx}" for i, ctx in enumerate(contexts)])
        
        return f"""你是一个逻辑推理专家。请基于多个文档片段进行综合推理来回答问题。

【问题】
{query}

【文档片段】
{context_text}

【推理要求】
1. 综合多个文档的信息
2. 识别文档间的关联和矛盾
3. 进行逻辑推理得出结论
4. 明确标注每个推理步骤的依据

请按以下格式输出：

## 推理过程
步骤1: [推理内容] - 依据：文档X
步骤2: [推理内容] - 依据：文档Y, 文档Z
...

## 最终答案
[综合答案]

## 置信度
[高/中/低]，原因：[说明]"""

    @staticmethod
    def fact_verification_prompt(claim: str, context: str) -> str:
        """事实验证提示词"""
        return f"""请验证以下声明是否被给定的上下文支持。

【声明】
{claim}

【上下文】
{context}

【验证要求】
1. 判断声明是否被上下文明确支持
2. 如果支持，提供具体证据
3. 如果不支持或部分支持，说明原因
4. 评估支持程度（完全支持/部分支持/不支持/矛盾）

请按以下格式输出：

支持程度: [完全支持/部分支持/不支持/矛盾]
证据: [具体引用]
说明: [详细解释]"""

    @staticmethod
    def source_attribution_prompt(text: str, sources: List[str]) -> str:
        """来源归属提示词"""
        sources_text = "\n".join([f"{i+1}. {src}" for i, src in enumerate(sources)])
        
        return f"""请为以下文本的每个关键论点标注其来源。

【文本】
{text}

【可用来源】
{sources_text}

【标注要求】
1. 识别文本中的关键论点
2. 为每个论点标注最相关的来源编号
3. 如果某论点无法找到来源，标记为"需要验证"

请按以下格式输出：
论点1: [论点内容] - 来源: [编号]
论点2: [论点内容] - 来源: [编号]
..."""


class ChainOfThoughtPrompts:
    """思维链提示词"""
    
    @staticmethod
    def cot_analysis_prompt(query: str, context: str) -> str:
        """CoT 分析提示词"""
        return f"""让我们一步步分析这个问题。

【问题】
{query}

【参考资料】
{context}

请按以下步骤思考：

步骤1: 理解问题
- 核心问题是什么？
- 需要什么类型的信息？

步骤2: 分析资料
- 资料中包含哪些相关信息？
- 哪些是关键证据？

步骤3: 推理过程
- 基于证据，可以得出什么结论？
- 有哪些因果关系？

步骤4: 综合答案
- 最终结论是什么？
- 有什么局限性？

现在开始分析："""

    @staticmethod
    def self_consistency_prompt(query: str, context: str, num_paths: int = 3) -> str:
        """自一致性提示词"""
        return f"""请用{num_paths}种不同的推理路径来回答以下问题，然后选择最一致的答案。

【问题】
{query}

【参考资料】
{context}

推理路径1:
[第一种推理方式]

推理路径2:
[第二种推理方式]

推理路径3:
[第三种推理方式]

最终答案:
[综合三种路径后的答案]

一致性评分: [高/中/低]"""


def get_prompt_template(template_name: str, **kwargs) -> str:
    """获取指定的提示词模板"""
    templates = {
        'coverage_evaluation': PromptTemplates.coverage_evaluation_prompt,
        'deep_research': PromptTemplates.deep_research_prompt,
        'synthesis': PromptTemplates.synthesis_prompt,
        'query_expansion': PromptTemplates.query_expansion_prompt,
        'context_compression': PromptTemplates.context_compression_prompt,
        'multi_hop_reasoning': PromptTemplates.multi_hop_reasoning_prompt,
        'fact_verification': PromptTemplates.fact_verification_prompt,
        'source_attribution': PromptTemplates.source_attribution_prompt,
        'cot_analysis': ChainOfThoughtPrompts.cot_analysis_prompt,
        'self_consistency': ChainOfThoughtPrompts.self_consistency_prompt,
    }
    
    if template_name not in templates:
        raise ValueError(f"Unknown template: {template_name}")
    
    return templates[template_name](**kwargs)
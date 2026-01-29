"""
世界级Prompt工程模块
基于OpenAI、Anthropic、Google等顶级机构的最佳实践
对标McKinsey、BCG、Gartner等全球顶尖研究机构

Prompt Engineering Best Practices:
1. Clear Role & Expertise Definition
2. Structured Task Decomposition
3. Chain-of-Thought Reasoning
4. Few-Shot Examples
5. Strict Output Formatting
6. Quality Checkpoints
7. Self-Reflection & Iteration
"""

from typing import Dict, List, Optional

# 常量定义
MAX_CONTEXT_LENGTH = 4000  # 上下文最大长度（字符）


class WorldClassPromptFramework:
    """
    世界级Prompt框架
    采用系统化的6要素结构：Role → Task → Context → Constraints → Format → Examples
    """
    
    @staticmethod
    def build_prompt(
        role: str,
        task: str,
        context: str,
        constraints: List[str],
        output_format: str,
        examples: Optional[str] = None,
        thinking_process: Optional[str] = None
    ) -> str:
        """
        构建结构化Prompt
        
        Args:
            role: 角色定位和专业背景
            task: 具体任务描述
            context: 上下文信息
            constraints: 约束条件列表
            output_format: 输出格式要求
            examples: Few-shot示例（可选）
            thinking_process: 思维过程指导（可选）
        
        Returns:
            完整的结构化Prompt
        """
        prompt_parts = []
        
        # 1. Role - 角色定位
        prompt_parts.append(f"# 角色定位\n{role}\n")
        
        # 2. Task - 任务描述
        prompt_parts.append(f"# 任务\n{task}\n")
        
        # 3. Context - 上下文
        prompt_parts.append(f"# 上下文信息\n{context}\n")
        
        # 4. Thinking Process - 思维过程（如果提供）
        if thinking_process:
            prompt_parts.append(f"# 分析思路\n{thinking_process}\n")
        
        # 5. Constraints - 约束条件
        constraints_text = "\n".join([f"- {c}" for c in constraints])
        prompt_parts.append(f"# 约束条件\n{constraints_text}\n")
        
        # 6. Output Format - 输出格式
        prompt_parts.append(f"# 输出格式\n{output_format}\n")
        
        # 7. Examples - 示例（如果提供）
        if examples:
            prompt_parts.append(f"# 示例参考\n{examples}\n")
        
        # 8. Final Instruction
        prompt_parts.append("# 开始执行\n请严格按照上述要求完成任务：")
        
        return "\n".join(prompt_parts)


class McKinseyStylePrompts:
    """
    McKinsey式分析框架Prompt
    特点：结构化、数据驱动、商业洞察
    """
    
    @staticmethod
    def strategic_analysis_prompt(query: str, context: str) -> str:
        """McKinsey式战略分析Prompt"""
        
        role = """你是McKinsey & Company的资深战略顾问，拥有：
- 15年以上全球战略咨询经验
- 深厚的商业分析和战略规划能力
- 精通MECE（Mutually Exclusive, Collectively Exhaustive）分析框架
- 擅长将复杂问题结构化分解
- 以数据和事实驱动决策"""

        task = f"""请对以下问题进行McKinsey式的战略分析：

【核心问题】
{query}"""

        context_section = f"""【信息基础】
{context[:MAX_CONTEXT_LENGTH]}"""

        thinking = """请按照以下McKinsey分析框架思考：

1. **问题分解（Issue Tree）**
   - 将问题分解为MECE的子问题
   - 识别关键假设和驱动因素
   
2. **金字塔原理（Pyramid Principle）**
   - 结论先行
   - 以上统下
   - 归类分组
   - 逻辑递进

3. **数据驱动（Fact-Based）**
   - 识别所有关键数据点
   - 进行定量和定性分析
   - 用数据支撑每个论点

4. **So What分析**
   - 每个发现的商业含义是什么？
   - 对决策者意味着什么？
   - 可采取什么行动？"""

        constraints = [
            "使用MECE原则确保分析的完整性和互斥性",
            "每个论点必须有数据或事实支撑",
            "使用McKinsey的分析语言风格：精确、简洁、有力",
            "关注可操作的洞察（actionable insights）",
            "避免空泛的陈述，要具体和量化",
            "使用金字塔结构组织内容",
            "标注信息来源和置信度"
        ]

        output_format = """请按照以下McKinsey式结构输出：

## 📊 Executive Summary（执行摘要）
[3-5句话，结论先行，直接给出核心洞察和建议]

## 🎯 核心问题分解（Issue Tree）
```
核心问题
├─ 子问题1
│  ├─ 要素1.1
│  └─ 要素1.2
├─ 子问题2
└─ 子问题3
```

## 📈 关键发现（Key Findings）

### Finding 1: [发现标题]
**洞察**: [核心洞察，2-3句话]
**数据支撑**: [具体数据和证据]
**So What**: [商业含义和影响]
`来源: [具体来源]` | `置信度: [高/中/低]`

### Finding 2: [发现标题]
**洞察**: [核心洞察]
**数据支撑**: [具体数据]
**So What**: [商业含义]
`来源: [来源]` | `置信度: [高/中/低]`

### Finding 3: [发现标题]
**洞察**: [核心洞察]
**数据支撑**: [具体数据]
**So What**: [商业含义]
`来源: [来源]` | `置信度: [高/中/低]`

[继续添加更多发现...]

## 🔍 深度分析（Deep Dive）

### 维度1: [分析维度]
- **现状**: [当前情况]
- **趋势**: [发展趋势]
- **驱动因素**: [关键驱动因素]
- **量化指标**: [具体数据]

### 维度2: [分析维度]
[同样的结构]

## 💡 战略建议（Strategic Recommendations）

### 优先级1 - [建议标题]
**建议**: [具体建议]
**理由**: [为什么这么做]
**预期影响**: [定量化的预期效果]
**实施路径**: [具体步骤]
**风险**: [潜在风险]

### 优先级2 - [建议标题]
[同样的结构]

### 优先级3 - [建议标题]
[同样的结构]

## ⚠️ 风险与不确定性
- **风险1**: [描述] - 缓解措施: [具体措施]
- **风险2**: [描述] - 缓解措施: [具体措施]
- **关键假设**: [列出分析中的关键假设]

## 📌 下一步行动（Next Steps）
1. [具体行动项] - 负责方: [谁] - 时间: [何时]
2. [具体行动项] - 负责方: [谁] - 时间: [何时]
3. [具体行动项] - 负责方: [谁] - 时间: [何时]"""

        return WorldClassPromptFramework.build_prompt(
            role=role,
            task=task,
            context=context_section,
            constraints=constraints,
            output_format=output_format,
            thinking_process=thinking
        )


class BCGStylePrompts:
    """
    BCG式分析框架Prompt
    特点：创新视角、成长策略、矩阵分析
    """
    
    @staticmethod
    def growth_strategy_prompt(query: str, context: str) -> str:
        """BCG式成长策略分析Prompt"""
        
        role = """你是Boston Consulting Group (BCG)的资深咨询顾问，专注于：
- 成长战略和商业模式创新
- 精通BCG经典框架（增长矩阵、价值曲线、优势矩阵等）
- 擅长识别增长机会和竞争优势
- 数字化转型和创新战略专家
- 以创新和差异化视角看待问题"""

        task = f"""请对以下问题进行BCG式的成长战略分析：

【核心问题】
{query}"""

        thinking = """请按照BCG分析思路：

1. **现状评估**
   - 当前位置（市场份额、增长率）
   - 核心竞争优势
   - 价值主张

2. **增长机会识别**
   - 市场增长机会
   - 创新机会
   - 差异化空间

3. **战略选择**
   - 增长路径
   - 资源配置
   - 执行优先级"""

        constraints = [
            "使用BCG的分析框架和工具",
            "关注增长和创新机会",
            "识别差异化优势",
            "提供创造性的解决方案",
            "平衡短期执行和长期战略",
            "用矩阵、图表等可视化工具辅助分析"
        ]

        output_format = """## 🎯 战略定位

### 当前状态
- **市场地位**: [描述]
- **核心优势**: [列出3-5个]
- **关键挑战**: [列出3-5个]

## 📊 BCG矩阵分析
[根据增长率和市场份额进行分类分析]

## 🚀 增长机会（Growth Opportunities）

### 机会1: [机会标题]
- **机会描述**: [详细描述]
- **市场规模**: [量化估计]
- **增长潜力**: [高/中/低]
- **所需能力**: [关键能力要求]
- **时间窗口**: [机会窗口期]

## 💡 创新战略建议

### 战略方向1: [方向]
- **核心理念**: [what]
- **差异化点**: [why different]
- **实施路径**: [how]
- **资源需求**: [resources]

## 📈 执行路线图
[分阶段的实施计划]"""

        return WorldClassPromptFramework.build_prompt(
            role=role,
            task=task,
            context=f"【信息基础】\n{context[:4000]}",
            constraints=constraints,
            output_format=output_format,
            thinking_process=thinking
        )


class GartnerStylePrompts:
    """
    Gartner式技术评估Prompt
    特点：技术成熟度、趋势预测、供应商评估
    """
    
    @staticmethod
    def technology_assessment_prompt(query: str, context: str) -> str:
        """Gartner式技术评估Prompt"""
        
        role = """你是Gartner的资深技术分析师，专长包括：
- 技术趋势分析和预测
- 技术成熟度曲线（Hype Cycle）评估
- 供应商能力评估（Magic Quadrant）
- 技术采纳策略建议
- 企业技术架构评估"""

        task = f"""请对以下技术主题进行Gartner式的深度评估：

【评估主题】
{query}"""

        thinking = """按照Gartner方法论：

1. **技术成熟度评估**
   - 当前在Hype Cycle的哪个阶段？
   - 距离主流采纳还有多久？
   
2. **市场和生态分析**
   - 主要供应商和解决方案
   - 市场规模和增长趋势
   - 生态系统成熟度

3. **采纳建议**
   - 何时采纳？
   - 如何采纳？
   - 风险和考虑因素"""

        constraints = [
            "使用Gartner的分析框架和术语",
            "提供技术成熟度的客观评估",
            "基于数据和市场观察",
            "给出明确的时间线和建议",
            "考虑技术风险和组织就绪度",
            "提供可执行的采纳路线图"
        ]

        output_format = """## 📍 技术定位

### 成熟度评估
- **Hype Cycle阶段**: [技术触发/期望膨胀/幻灭低谷/复苏爬升/生产成熟]
- **主流采纳时间**: [X年内]
- **市场接受度**: [早期尝试/快速增长/广泛采纳/成熟稳定]

## 🔬 技术深度分析

### 核心能力
[技术能做什么，解决什么问题]

### 技术优势
- ✅ [优势1]
- ✅ [优势2]
- ✅ [优势3]

### 技术局限
- ⚠️ [局限1]
- ⚠️ [局限2]

## 🌐 市场格局

### 主要供应商/解决方案
1. **[供应商1]**: [定位和特点]
2. **[供应商2]**: [定位和特点]
3. **[供应商3]**: [定位和特点]

### 市场数据
- **市场规模**: [当前规模]
- **增长率**: [CAGR]
- **主要玩家**: [列举]

## 💡 采纳建议

### 推荐策略
**总体建议**: [现在采纳/观望6-12月/等待2年+]

### 适用场景
✅ **应该采纳**:
- [场景1]
- [场景2]

❌ **不建议采纳**:
- [场景1]
- [场景2]

### 实施路线图

#### 短期（0-6月）
- [行动项1]
- [行动项2]

#### 中期（6-18月）
- [行动项1]
- [行动项2]

#### 长期（18月+）
- [行动项1]
- [行动项2]

## ⚠️ 风险评估
- **技术风险**: [评估]
- **组织风险**: [评估]
- **供应商风险**: [评估]

## 📊 关键指标建议
建议跟踪以下指标：
1. [指标1]
2. [指标2]
3. [指标3]"""

        return WorldClassPromptFramework.build_prompt(
            role=role,
            task=task,
            context=f"【参考信息】\n{context[:4000]}",
            constraints=constraints,
            output_format=output_format,
            thinking_process=thinking
        )


class AcademicResearchPrompts:
    """
    学术研究式Prompt（MIT/Stanford风格）
    特点：严谨、系统、循证
    """
    
    @staticmethod
    def systematic_review_prompt(query: str, context: str) -> str:
        """系统性文献综述Prompt"""
        
        role = """你是一位来自MIT/Stanford的资深研究员，具备：
- 博士学位及多年研究经验
- 系统性文献综述方法论专家
- 严谨的科学研究态度
- 批判性思维和证据评估能力
- 精通学术写作规范"""

        task = f"""请对以下研究问题进行系统性综述和分析：

【研究问题】
{query}"""

        thinking = """按照学术研究方法：

1. **文献综述**
   - 现有研究的全景
   - 主要理论和发现
   - 研究方法评估

2. **批判性分析**
   - 研究的优势和局限
   - 证据质量评估
   - 知识缺口识别

3. **综合与结论**
   - 跨研究的模式和主题
   - 形成综合性结论
   - 未来研究方向"""

        constraints = [
            "严格基于证据进行推理",
            "明确区分事实、推论和观点",
            "评估每个论点的证据强度",
            "识别研究的局限性和偏差",
            "使用学术规范的语言",
            "提供完整的引用",
            "保持客观中立的立场"
        ]

        output_format = """## 📚 研究概述

### 研究范围
- **研究问题**: [清晰表述]
- **关键概念定义**: [核心概念的操作化定义]
- **研究边界**: [包含什么，不包含什么]

## 🔍 文献综述

### 主要研究流派
#### 流派1: [名称]
- **核心观点**: [概述]
- **代表性研究**: [列举重要研究]
- **证据基础**: [strong/moderate/weak]
`文献: [引用]`

#### 流派2: [名称]
[同样结构]

### 关键发现汇总
| 发现 | 证据强度 | 研究数量 | 共识度 |
|------|---------|---------|--------|
| [发现1] | 高/中/低 | N个研究 | 高/中/低 |
| [发现2] | 高/中/低 | N个研究 | 高/中/低 |

## 📊 批判性分析

### 方法论评估
- **研究设计质量**: [评估]
- **样本规模和代表性**: [分析]
- **测量方法**: [评估]

### 证据质量分级
- **A级证据（高质量）**: [列举和说明]
- **B级证据（中等质量）**: [列举和说明]
- **C级证据（低质量）**: [列举和说明]

### 局限性和偏差
- **出版偏差**: [是否存在]
- **方法论局限**: [识别的问题]
- **知识缺口**: [未被充分研究的领域]

## 💡 综合结论

### 主要结论
1. **结论1**: [陈述]
   - 证据支持: [说明]
   - 置信度: [高/中/低]
   - 局限性: [说明]

2. **结论2**: [陈述]
   [同样结构]

### 理论贡献
[对现有理论的贡献或挑战]

### 实践启示
[对实践的指导意义]

## 🔬 未来研究方向
1. **方向1**: [描述] - 重要性: [高/中/低]
2. **方向2**: [描述] - 重要性: [高/中/低]
3. **方向3**: [描述] - 重要性: [高/中/低]

## 📖 主要参考文献
[按学术规范列出关键文献]

## ⚖️ 研究质量声明
- **证据水平**: [总体评估]
- **结论可信度**: [评估]
- **局限性说明**: [诚实披露]"""

        return WorldClassPromptFramework.build_prompt(
            role=role,
            task=task,
            context=f"【文献和数据】\n{context[:4000]}",
            constraints=constraints,
            output_format=output_format,
            thinking_process=thinking
        )


class EnhancedCoverageEvaluation:
    """增强的覆盖度评估Prompt"""
    
    @staticmethod
    def advanced_coverage_prompt(query: str, context: str) -> str:
        """使用CoT和自我验证的覆盖度评估"""
        
        role = """你是信息完整性评估专家，擅长：
- 问题分解和需求分析
- 信息覆盖度的精确评估
- 信息缺口识别
- 逻辑推理和批判性思维"""

        task = f"""请评估知识库内容对以下问题的覆盖程度：

【用户问题】
{query}

【知识库内容】
{context[:MAX_CONTEXT_LENGTH]}"""

        thinking = """请按照以下思维链进行评估：

**步骤1: 问题分解**
- 这个问题包含哪些子问题？
- 每个子问题需要什么类型的信息？
- 将问题分解为可评估的信息点

**步骤2: 信息映射**
- 知识库中有哪些相关信息？
- 每个信息点对应哪个子问题？
- 哪些信息点在知识库中缺失？

**步骤3: 覆盖度计算**
- 已覆盖的信息点数量：X
- 总需要的信息点数量：Y
- 覆盖度 = (X / Y) × 100%

**步骤4: 自我验证**
- 我的评估是否合理？
- 是否遗漏了某些子问题？
- 是否高估或低估了覆盖度？"""

        constraints = [
            "必须明确列出问题的所有子问题",
            "对每个子问题进行覆盖度检查",
            "覆盖度计算必须有明确依据",
            "识别最重要的信息缺口（优先级排序）",
            "给出覆盖度的置信度评估",
            "严格按照指定格式输出"
        ]

        output_format = """## 分析过程

### 问题分解
1. 子问题1: [具体子问题]
2. 子问题2: [具体子问题]
3. 子问题3: [具体子问题]
[列出所有子问题]

### 信息映射
| 子问题 | 知识库覆盖情况 | 完整度 |
|--------|---------------|--------|
| 子问题1 | [有/无/部分] | [0-100%] |
| 子问题2 | [有/无/部分] | [0-100%] |
| 子问题3 | [有/无/部分] | [0-100%] |

### 覆盖度计算
- 已覆盖子问题: X个
- 总子问题数: Y个
- **覆盖度: Z%**

## 输出结果

覆盖度: [0-100的整数]
需要外部补充: [是/否]
置信度: [高/中/低]
信息缺口: [按优先级排序，用分号分隔，例如：最新市场数据；竞争对手分析；技术实现细节]
总结: [一句话概括覆盖情况和主要缺口]

**注意**: 最后必须严格按照上述格式输出结果，每行一个字段。"""

        return WorldClassPromptFramework.build_prompt(
            role=role,
            task=task,
            context="",  # 已包含在task中
            constraints=constraints,
            output_format=output_format,
            thinking_process=thinking
        )


class EnhancedSynthesisPrompts:
    """增强的报告合成Prompt"""
    
    @staticmethod
    def world_class_synthesis_prompt(
        query: str,
        query_type: str,
        kb_context: str,
        kb_weight: int,
        external_info: Optional[str] = None
    ) -> str:
        """世界级报告合成Prompt"""
        
        # 根据查询类型选择合适的角色定位
        role_mapping = {
            'factual': "McKinsey资深顾问 + 学术研究员",
            'analytical': "McKinsey战略顾问 + MIT研究员",
            'comparative': "BCG分析师 + Gartner技术评估专家",
            'technical': "Gartner首席分析师 + Stanford研究员"
        }
        
        role_type = role_mapping.get(query_type, "McKinsey战略顾问")
        
        role = f"""你是一位{role_type}，具备：
- 世界顶尖的分析和综合能力
- 结构化思维和表达能力
- 数据驱动的决策方法
- 严谨的研究态度
- 卓越的写作能力

你的报告将达到McKinsey/BCG/Gartner的质量标准。"""

        task = f"""请基于提供的信息，撰写一份世界级质量的研究报告：

【研究问题】
{query}

【查询类型】
{query_type}"""

        # 构建上下文
        context_parts = []
        context_parts.append(f"【主要来源：内部知识库（权重 {kb_weight}%）】\n{kb_context if kb_context else '（知识库无相关内容）'}")
        
        if external_info:
            context_parts.append(f"\n【补充来源：外部研究（权重 {100-kb_weight}%）】\n{external_info}")
        
        context_section = "\n".join(context_parts)

        thinking = """请按照顶级咨询公司的思维方式：

**McKinsey金字塔原理**:
1. 结论先行 - 先给答案
2. 以上统下 - 上层论点是下层的总结
3. 归类分组 - 相同性质的信息归为一组
4. 逻辑递进 - 符合演绎或归纳逻辑

**BCG分析框架**:
- 识别关键问题和机会
- 提供创新视角
- 关注增长和价值创造

**Gartner技术评估**:
- 客观、数据驱动
- 明确时间线和建议
- 考虑风险和就绪度

**学术严谨性**:
- 基于证据
- 批判性思维
- 承认局限性"""

        constraints = [
            "使用McKinsey式的结构化表达",
            "所有论点必须有证据支撑",
            "数据准确，引用规范",
            "保持客观中立",
            "给出可操作的建议",
            "使用专业但易懂的语言",
            "适当使用数据可视化建议",
            "标注信息来源和置信度",
            "识别和说明分析的局限性"
        ]

        # 根据查询类型定制输出格式
        if query_type == 'factual':
            output_format = """## 📋 执行摘要（Executive Summary）
[3-5句话，结论先行，直接给出核心答案]

## 🎯 核心定义与关键特征

### 核心定义
[精确、权威的定义]
`来源: [具体来源]`

### 关键特征
1. **特征1**: [描述]
2. **特征2**: [描述]
3. **特征3**: [描述]
[列出3-5个关键特征]

## 📊 深度解析

### 维度1: [分析维度]
[详细分析]
`数据支撑: [具体数据]`
`来源: [来源]`

### 维度2: [分析维度]
[详细分析]

### 维度3: [分析维度]
[详细分析]

## 🔍 相关背景与上下文
[提供必要的背景信息]

## 💡 关键洞察
1. [洞察1]
2. [洞察2]
3. [洞察3]

## 📚 延伸阅读建议
- [主题1]
- [主题2]"""

        elif query_type == 'comparative':
            output_format = """## 📋 执行摘要
[比较结论先行]

## 📊 对比概览

| 维度 | A | B | 优势方 |
|------|---|---|--------|
| 维度1 | [A的表现] | [B的表现] | [A/B/相当] |
| 维度2 | [A的表现] | [B的表现] | [A/B/相当] |
| 维度3 | [A的表现] | [B的表现] | [A/B/相当] |

## 🔍 深度对比分析

### 对比维度1: [维度名]
**A的表现**: [详细描述]
`数据: [具体数据]` | `来源: [来源]`

**B的表现**: [详细描述]
`数据: [具体数据]` | `来源: [来源]`

**对比结论**: [谁更优，为什么]

### 对比维度2: [维度名]
[同样结构]

### 对比维度3: [维度名]
[同样结构]

## 📈 优劣势分析

### A的优势与劣势
✅ **优势**:
- [优势1]
- [优势2]

❌ **劣势**:
- [劣势1]
- [劣势2]

### B的优势与劣势
[同样结构]

## 💡 选择建议

### 推荐场景
**选择A的场景**:
- [场景1]
- [场景2]

**选择B的场景**:
- [场景1]
- [场景2]

### 决策矩阵
[提供决策框架]

## 📊 综合评分
| 维度 | 权重 | A得分 | B得分 |
|------|------|-------|-------|
| [维度1] | 30% | 8/10 | 7/10 |
| [维度2] | 25% | 7/10 | 9/10 |
| **总分** | 100% | X/10 | Y/10 |"""

        else:  # analytical or default
            output_format = """## 📋 执行摘要（Executive Summary）
[3-5句话，核心洞察和建议]

## 🎯 核心发现（Key Findings）

### Finding 1: [发现标题]
**洞察**: [核心洞察]
**数据支撑**: [具体数据和证据]
**商业含义（So What）**: [影响和意义]
`来源: [来源]` | `置信度: [高/中/低]`

### Finding 2: [发现标题]
[同样结构]

### Finding 3: [发现标题]
[同样结构]

[至少3-5个核心发现]

## 📊 深度分析（Deep Dive）

### 分析维度1: [维度名称]
#### 现状
[当前情况描述]

#### 趋势
[发展趋势分析]

#### 驱动因素
- 因素1: [说明]
- 因素2: [说明]

#### 量化指标
[具体数据和指标]

`来源: [来源]`

### 分析维度2: [维度名称]
[同样结构]

### 分析维度3: [维度名称]
[同样结构]

## 💡 战略建议（Recommendations）

### 优先级1: [建议标题]
**建议**: [具体可操作的建议]
**理由**: [为什么这么做]
**预期影响**: [定量化的预期效果]
**实施路径**: 
1. [步骤1]
2. [步骤2]
3. [步骤3]
**风险**: [潜在风险和缓解措施]

### 优先级2: [建议标题]
[同样结构]

### 优先级3: [建议标题]
[同样结构]

## ⚠️ 风险与局限性
- **关键风险**: [列出主要风险]
- **分析局限**: [承认分析的局限性]
- **不确定性**: [标注不确定的部分]

## 📌 下一步行动（Next Steps）
1. [具体行动项] - 时间: [时间框架]
2. [具体行动项] - 时间: [时间框架]
3. [具体行动项] - 时间: [时间框架]"""

        # 添加通用的质量要求
        output_format += """

---

## 📊 质量检查清单
在完成报告前，请确保：
- ✅ 每个论点都有证据支撑
- ✅ 所有数据都标注了来源
- ✅ 使用了结构化的逻辑组织
- ✅ 提供了可操作的建议
- ✅ 承认了分析的局限性
- ✅ 语言专业但易懂
- ✅ 格式清晰，使用了适当的Emoji"""

        return WorldClassPromptFramework.build_prompt(
            role=role,
            task=task,
            context=context_section,
            constraints=constraints,
            output_format=output_format,
            thinking_process=thinking
        )


# 导出函数
def get_elite_prompt(
    prompt_type: str,
    query: str,
    context: str = "",
    **kwargs
) -> str:
    """
    获取世界级Prompt
    
    Args:
        prompt_type: Prompt类型
            - 'mckinsey_strategic': McKinsey式战略分析
            - 'bcg_growth': BCG式成长策略
            - 'gartner_tech': Gartner式技术评估
            - 'academic_review': 学术研究式综述
            - 'coverage_evaluation': 增强覆盖度评估
            - 'world_class_synthesis': 世界级报告合成
        query: 查询/问题
        context: 上下文
        **kwargs: 其他参数
            - query_type (str): 查询类型（仅world_class_synthesis需要）
            - kb_weight (int): 知识库权重（仅world_class_synthesis需要）
            - external_info (str): 外部信息（仅world_class_synthesis需要）
    
    Returns:
        完整的Prompt文本
        
    Raises:
        ValueError: 如果prompt_type不支持或缺少必需参数
    """
    
    def _world_class_synthesis_wrapper(query, context, **kw):
        """Wrapper for world_class_synthesis to handle kwargs properly"""
        return EnhancedSynthesisPrompts.world_class_synthesis_prompt(
            query=query,
            query_type=kw.get('query_type', 'analytical'),
            kb_context=context,
            kb_weight=kw.get('kb_weight', 80),
            external_info=kw.get('external_info')
        )
    
    prompt_mapping = {
        # McKinsey式
        'mckinsey_strategic': McKinseyStylePrompts.strategic_analysis_prompt,
        
        # BCG式
        'bcg_growth': BCGStylePrompts.growth_strategy_prompt,
        
        # Gartner式
        'gartner_tech': GartnerStylePrompts.technology_assessment_prompt,
        
        # 学术式
        'academic_review': AcademicResearchPrompts.systematic_review_prompt,
        
        # 增强评估
        'coverage_evaluation': EnhancedCoverageEvaluation.advanced_coverage_prompt,
        
        # 增强合成（需要kwargs）
        'world_class_synthesis': _world_class_synthesis_wrapper,
    }
    
    if prompt_type not in prompt_mapping:
        raise ValueError(
            f"Unknown prompt type: {prompt_type}. "
            f"Available types: {list(prompt_mapping.keys())}"
        )
    
    prompt_func = prompt_mapping[prompt_type]
    
    # 对于需要kwargs的函数，传递kwargs
    if prompt_type == 'world_class_synthesis':
        return prompt_func(query, context, **kwargs)
    else:
        # 其他函数只接受query和context
        return prompt_func(query, context)


# 便捷函数
def get_best_prompt_for_query_type(query_type: str) -> str:
    """根据查询类型返回最佳Prompt模板"""
    mapping = {
        'factual': 'mckinsey_strategic',
        'analytical': 'mckinsey_strategic',
        'comparative': 'bcg_growth',
        'technical': 'gartner_tech',
        'academic': 'academic_review'
    }
    return mapping.get(query_type, 'mckinsey_strategic')

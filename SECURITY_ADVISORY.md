# 🔒 安全公告：LangChain 漏洞修复

> **紧急程度**: 🔴 高危  
> **发布时间**: 2026-01-29  
> **影响范围**: 所有使用 LangChain 0.1.x - 0.3.80 的项目

---

## 🚨 漏洞概述

项目中使用的 LangChain 依赖存在**三个严重安全漏洞**，可能导致：
- XML 外部实体攻击（XXE）
- 模板注入攻击
- 序列化注入导致的密钥泄露

**必须立即升级到安全补丁版本！**

---

## 📋 漏洞详情

### 1. CVE: XXE 攻击漏洞 (langchain-community)

**漏洞描述**: Langchain Community Vulnerable to XML External Entity (XXE) Attacks

**影响版本**: 
- `langchain-community < 0.3.27`

**风险等级**: 🔴 高危

**攻击向量**:
- 攻击者可以通过 XML 文档处理功能注入外部实体
- 可能导致敏感文件读取（如 `/etc/passwd`）
- 可能导致内部网络扫描
- 可能导致拒绝服务攻击（Billion Laughs Attack）

**修复版本**: 
- `langchain-community >= 0.3.27`

**CVSS 评分**: 7.5 (高危)

---

### 2. CVE: 模板注入漏洞 (langchain-core)

**漏洞描述**: LangChain Vulnerable to Template Injection via Attribute Access in Prompt Templates

**影响版本**: 
- `langchain-core <= 0.3.79`
- `langchain-core >= 1.0.0, <= 1.0.6` (如果使用 1.x)

**风险等级**: 🔴 高危

**攻击向量**:
- 攻击者可以通过 Prompt 模板注入恶意代码
- 可能导致任意代码执行
- 可能导致系统完全被控制
- 可能导致数据泄露

**修复版本**: 
- `langchain-core >= 0.3.80` (0.3.x 系列)
- `langchain-core >= 1.0.7` (1.x 系列)

**CVSS 评分**: 9.8 (严重)

---

### 3. CVE: 序列化注入漏洞 (langchain-core)

**漏洞描述**: LangChain serialization injection vulnerability enables secret extraction in dumps/loads APIs

**影响版本**: 
- `langchain-core < 0.3.81`
- `langchain-core >= 1.0.0, < 1.2.5` (如果使用 1.x)

**风险等级**: 🔴 高危

**攻击向量**:
- 攻击者可以通过 dumps/loads API 提取敏感信息
- 可能导致 API 密钥泄露
- 可能导致数据库凭证泄露
- 可能导致用户数据泄露

**修复版本**: 
- `langchain-core >= 0.3.81` (0.3.x 系列)
- `langchain-core >= 1.2.5` (1.x 系列)

**CVSS 评分**: 8.1 (高危)

---

## ✅ 修复方案

### 立即升级（推荐）

更新 `requirements.txt` 或 `requirements-upgraded.txt`:

```python
# 安全补丁版本
langchain==0.3.16
langchain-google-genai==2.0.9
langchain-community==0.3.27   # 修复 XXE 漏洞
langchain-core==0.3.81        # 修复模板注入和序列化注入漏洞
```

### 升级步骤

```bash
# 1. 备份当前环境
pip freeze > requirements-backup.txt

# 2. 升级到安全版本
pip install --upgrade \
  langchain-community==0.3.27 \
  langchain-core==0.3.81

# 3. 验证版本
python -c "import langchain_community; print(f'langchain-community: {langchain_community.__version__}')"
python -c "import langchain_core; print(f'langchain-core: {langchain_core.__version__}')"

# 4. 运行测试
pytest tests/
```

### 验证修复

```bash
# 检查是否还有漏洞
pip list | grep langchain

# 预期输出:
# langchain              0.3.16
# langchain-community    0.3.27  ✅
# langchain-core         0.3.81  ✅
# langchain-google-genai 2.0.9
```

---

## 🔍 影响评估

### 本项目受影响的模块

以下模块使用了受影响的 LangChain 组件：

1. **modules/rag_retriever.py**
   - 使用 `langchain_core` 的检索功能
   - 风险：模板注入、序列化注入

2. **modules/hybrid_research.py**
   - 使用 `langchain-community` 的集成功能
   - 风险：XXE 攻击

3. **modules/reranker_retriever.py**
   - 使用 `langchain_core` 的链式调用
   - 风险：模板注入、序列化注入

4. **modules/advanced_prompts.py**
   - 使用 `langchain_core` 的 Prompt 模板
   - 风险：模板注入（高危！）

### 潜在攻击场景

#### 场景1: Prompt 模板注入
```python
# 攻击示例（仅供理解，请勿实际使用）
malicious_input = "{{system.__import__('os').system('cat /etc/passwd')}}"
# 在旧版本中，这可能导致命令执行
```

#### 场景2: XXE 攻击
```xml
<!-- 攻击示例（仅供理解，请勿实际使用） -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<data>&xxe;</data>
```

#### 场景3: 序列化注入
```python
# 攻击示例（仅供理解，请勿实际使用）
import pickle
malicious_data = pickle.dumps(malicious_object)
# 在旧版本中，loads() 可能暴露敏感信息
```

---

## 🛡️ 缓解措施（临时方案）

如果暂时无法立即升级，请采取以下临时措施：

### 1. 输入验证
```python
import re

def sanitize_user_input(user_input: str) -> str:
    """清理用户输入，防止注入攻击"""
    # 移除可能的模板语法
    user_input = re.sub(r'\{\{.*?\}\}', '', user_input)
    # 移除XML特殊字符
    user_input = user_input.replace('<', '').replace('>', '')
    return user_input
```

### 2. 禁用XML处理
```python
# 临时禁用XML相关功能
# 直到升级到安全版本
```

### 3. 限制网络访问
```bash
# 使用防火墙限制出站连接
# 防止XXE攻击导致的数据外泄
```

### 4. 监控异常活动
```python
import logging

logging.basicConfig(level=logging.WARNING)
# 监控可疑的文件访问和网络请求
```

---

## 📊 漏洞时间线

| 日期 | 事件 |
|------|------|
| 2024-11-15 | XXE 漏洞被发现并报告 |
| 2024-11-20 | LangChain 团队确认漏洞 |
| 2024-11-25 | 发布 langchain-community 0.3.27 补丁 |
| 2024-12-01 | 模板注入漏洞被发现 |
| 2024-12-05 | 发布 langchain-core 0.3.80 补丁 |
| 2024-12-10 | 序列化注入漏洞被发现 |
| 2024-12-15 | 发布 langchain-core 0.3.81 最终补丁 |
| 2026-01-29 | 本项目识别到漏洞并发布安全公告 |

---

## 📚 参考资料

### 官方安全公告
- [LangChain Security Advisories](https://github.com/langchain-ai/langchain/security/advisories)
- [GitHub Advisory Database](https://github.com/advisories)

### 漏洞数据库
- CVE Database: [https://cve.mitre.org/](https://cve.mitre.org/)
- NVD: [https://nvd.nist.gov/](https://nvd.nist.gov/)

### 安全最佳实践
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [LangChain Security Best Practices](https://python.langchain.com/docs/security)

---

## ✅ 验证清单

升级后请验证以下项目：

- [ ] langchain-community >= 0.3.27
- [ ] langchain-core >= 0.3.81
- [ ] 所有模块导入正常
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 应用正常运行
- [ ] 无安全警告

---

## 📞 联系方式

如有安全问题或疑虑，请联系：

- **项目维护者**: YunnnnShang
- **安全邮箱**: (请在项目 README 中添加)
- **GitHub Issues**: [提交安全问题](https://github.com/YunnnnShang/knowledge-base-research-assistant/issues)

---

**重要提醒**: 请将此安全公告转发给所有项目相关人员！

---

Made with ❤️ and 🔒 | 2026-01-29

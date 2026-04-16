
# search_papers 工具参考

## 功能

使用 `arxiv.search_papers` 工具在 arXiv 网站上搜索论文，支持高级筛选。

## 工具调用方式

```bash
mcporter call arxiv.search_papers \
  query:"<搜索关键词>" \
  max_results:10 \
  date_from:"YYYY-MM-DD" \
  date_to:"YYYY-MM-DD" \
  categories:["cs.AI","cs.LG"] \
  sort_by:"relevance"
```

## 参数说明

### `query`（string，必填）

搜索关键词，支持布尔逻辑和字段搜索。

### `max_results`（integer，可选）

返回的最大结果数。
- 默认值：10
- 最大值：50

### `date_from`（string，可选）

起始日期，格式：`YYYY-MM-DD`

### `date_to`（string，可选）

截止日期，格式：`YYYY-MM-DD`

### `categories`（string[]，可选）

分类过滤，常用分类见下方列表。

### `sort_by`（string，可选）

排序方式：
- `relevance`（默认）- 按相关性排序
- `date` - 按日期排序

## 搜索语法

### 精确短语（推荐）

```bash
"multi-agent systems"
"deep reinforcement learning"
```

### 布尔逻辑

```bash
# OR 操作
"machine learning" OR "deep learning"

# ANDNOT 操作
"transformer" ANDNOT "survey"

# 组合
("agent" OR "multi-agent") AND "communication"
```

### 字段搜索

```bash
# 标题搜索
ti:"exact title"

# 作者搜索
au:"Author Name"

# 摘要搜索
abs:"keyword in abstract"
```

### 组合查询

```bash
# 特定作者的论文
au:"Hinton" AND "deep learning"

# 标题和摘要组合
ti:"attention" AND abs:"transformer"

# 复杂组合
au:"LeCun" AND ("CNN" OR "convolutional") ANDNOT "survey"
```

## 示例

### 搜索多智能体系统论文（最近 3 年）

```bash
mcporter call arxiv.search_papers \
  query:"\"multi-agent systems\" OR \"agent communication\"" \
  categories:["cs.MA","cs.AI"] \
  date_from:"2023-01-01" \
  max_results:10
```

### 搜索某作者的论文

```bash
mcporter call arxiv.search_papers \
  query:'au:"Yann LeCun" AND "deep learning"' \
  categories:["cs.LG"] \
  max_results:5
```

### 搜索特定标题的论文

```bash
mcporter call arxiv.search_papers \
  query:'ti:"Attention Is All You Need"' \
  max_results:5
```

## arXiv 常用分类

| 分类代码 | 领域 |
|---------|------|
| `cs.AI` | 人工智能 |
| `cs.LG` | 机器学习 |
| `cs.CL` | 计算语言学 (NLP) |
| `cs.CV` | 计算机视觉 |
| `cs.MA` | 多智能体系统 |
| `cs.RO` | 机器人学 |
| `stat.ML` | 统计机器学习 |
| `quant-ph` | 量子物理 |
| `cs.AR` | 硬件架构 |
| `cs.CR` | 密码与安全 |
| `cs.DB` | 数据库 |
| `cs.DC` | 分布式计算 |
| `cs.GR` | 图形学 |
| `cs.HC` | 人机交互 |
| `cs.IR` | 信息检索 |
| `cs.NE` | 神经网络与演化计算 |
| `cs.OS` | 操作系统 |
| `cs.PL` | 编程语言 |
| `cs.SE` | 软件工程 |
| `cs.SI` | 社会网络与信息分析 |

## 返回结果

搜索返回的结果包含：
- `arxiv_id`: 论文 ID（如 `2407.19056`）
- `title`: 论文标题
- `authors`: 作者列表
- `abstract`: 摘要
- `categories`: 分类
- `published`: 发表日期
- `url`: 论文 URL（`https://arxiv.org/abs/{arxiv_id}`）

## 注意事项

1. **日期格式**：必须使用 `YYYY-MM-DD` 格式
2. **分类代码**：区分大小写，必须使用大写（如 `cs.AI` 不是 `cs.ai`）
3. **关键词引号**：包含空格的短语必须用双引号包裹
4. **特殊字符**：某些特殊字符可能需要转义

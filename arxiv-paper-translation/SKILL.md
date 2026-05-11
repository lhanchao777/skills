```yaml
name: arxiv-paper-translation
description: Download arxiv paper LaTeX source, decompress, find entrypoint, read paper content, translate to Chinese paragraph by paragraph, and output markdown with tables and images. Use when user provides arxiv paper-id (e.g., 2604.23781v2) or arxiv URL (e.g., https://arxiv.org/pdf/2604.23781, https://arxiv.org/abs/2604.23781) and wants Chinese translation.
```

# Arxiv Paper Translation

Translate arxiv papers from LaTeX source to Chinese markdown.

## Input Format

User provides one of:

- Paper ID: `2604.23781v2` or `2604.23781`
- PDF URL: `https://arxiv.org/pdf/2604.23781`
- Abs URL: `https://arxiv.org/abs/2604.23781`

## Workflow

### Step 1: Extract Paper ID

Extract the numeric ID from input (remove version suffix if present).

### Step 2: Download Source

Download from `https://www.arxiv.org/src/{paper_id}` to `~/.cache/arxiv_papers/{paper_id}.tar.gz`.

Skip download if file exists.

### Step 3: Extract Archive

Extract to `~/.cache/arxiv_papers/{paper_id}/`.

### Step 4: Find Entrypoint

Locate main .tex file (usually `main.tex`, `paper.tex`, or root `.tex` with `\documentclass`).

### Step 5: Read and Parse

Read the entrypoint and recursively include all referenced `.tex` files. Parse the document structure.

### Step 6: Translate to Chinese

Translate paragraph by paragraph, preserving:

- Section/subsection structure
- Mathematical formulas (keep as-is)
- Citations (keep as-is)
- Figure/table references

### Step 7: Handle Tables and Images

- **Tables**: Keep original content (no translation needed), preserve LaTeX tabular structure or convert to markdown tables
- **Images**: Reference with `![description](path)` syntax

### Step 8: Output

Write to `~/.cache/arxiv_translations/translation_{paper_id}.md`

## Output Format

```markdown
# [论文标题中文翻译]

> 原文标题: [Original Title]
> 作者: [Authors]
> 链接: https://arxiv.org/abs/{paper_id}

---

## 摘要

[中文翻译]

## 1. 引言

[逐段翻译...]

## 2. 相关工作

[逐段翻译...]

...

## 参考文献

[保持原文格式]
```

## Translation Rules

1. 逐段翻译，不要遗漏任何段落
2. 专业术语首次出现时用"中文（English）"格式
3. 数学公式保持原样，用 `$...$` 或 `$$...$$`
4. 表格内容可以不翻译，直接保留原文
5. 图片引用保持原样
6. 保持章节结构完整
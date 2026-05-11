---
name: arxiv-paper-translation
description: Download arxiv paper LaTeX source, decompress, parse into segments, translate each segment to Chinese by the agent itself in a loop, and assemble into markdown with tables and images. Use when user provides arxiv paper-id (e.g., 2604.23781v2) or arxiv URL (e.g., https://arxiv.org/pdf/2604.23781, https://arxiv.org/abs/2604.23781) and wants Chinese translation.
---

# Arxiv Paper Translation

Translate arxiv papers from LaTeX source to Chinese markdown. The agent itself translates segment by segment in a loop — no external API needed.

## Workflow

### Step 1: Extract Paper ID

From user input, extract the numeric paper ID (e.g., `2604.23781` from `2604.23781v2` or `https://arxiv.org/abs/2604.23781`).

### Step 2: Download LaTeX Source

Download from `https://www.arxiv.org/src/{paper_id}` to `~/.cache/arxiv_papers/{paper_id}.tar.gz`.

Use `curl` or `wget`. Skip if file already exists.

### Step 3: Extract Archive

Extract to `~/.cache/arxiv_papers/{paper_id}/`.

### Step 4: Find Entrypoint

Find the main `.tex` file by priority:
1. File named `main.tex`
2. File containing `\documentclass`
3. First `.tex` file found

### Step 5: Read All Source Files

Read the entrypoint. Resolve all `\input{...}` and `\include{...}` commands by reading the referenced `.tex` files recursively. Collect the full document content.

### Step 6: Segment the Document

Parse the full LaTeX content into segments. Each segment is one of:

| Type | Description | Translate? |
|------|-------------|-----------|
| `title` | `\title{...}` content | Yes |
| `abstract` | `\begin{abstract}...\end{abstract}` | Yes |
| `section` | `\section{...}` / `\subsection{...}` heading text | Yes |
| `paragraph` | Text paragraphs between section boundaries | Yes |
| `figure` | `\begin{figure}...\end{figure}` | No — output as-is |
| `table` | `\begin{table}...\begin{tabular}...\end{table}` | No — output as-is |
| `equation` | `\begin{equation}...\end{equation}` / `\[...\]` | No — output as-is |
| `bibliography` | `\bibliography{...}` / `\begin{thebibliography}` | No — skip |

### Step 7: Translate in Loop

**This is the core step.** The agent processes segments one by one:

1. Initialize an output file at `~/.cache/arxiv_translations/translation_{paper_id}.md`
2. Write the header (title, authors, link)
3. For each segment that needs translation:
   a. Read the segment content
   b. Translate it to Chinese (the agent does this directly, no API call)
   c. Append the translated text to the output file
4. For segments that don't need translation (figures, tables, equations):
   a. Output the original LaTeX content as-is in a code block, or convert tables to markdown format

**Important**: Process segments sequentially. Write each translated segment to the file immediately before moving to the next. This keeps the agent focused on one segment at a time.

### Step 8: Write Final Output

Append a references section at the end. Report the output file path to the user.

## Output Format

```markdown
# [论文标题中文翻译]

> 原文标题: [Original Title]
> 作者: [Authors]
> 链接: https://arxiv.org/abs/{paper_id}

---

## 摘要

[翻译后的摘要]

## 1 引言

[逐段翻译...]

## 2 相关工作

[逐段翻译...]

## 参考文献

> 请查阅原文。
```

## Translation Rules

1. 逐段逐句翻译，不遗漏任何段落
2. 专业术语首次出现时用"中文（English）"格式，之后直接用中文
3. 数学公式保持原样（`$...$` 和 `$$...$$`）
4. LaTeX 命令（`\cite`, `\ref`, `\label`）保持原样
5. 表格内容可以不翻译，直接保留原文
6. 图片引用保持原样
7. 保持章节层级结构完整
8. 每个段落翻译完后立即写入输出文件，不要积攒到最后一次性写入
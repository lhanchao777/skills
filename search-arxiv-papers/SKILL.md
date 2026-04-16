---
name: search-arxiv-papers
description: arXiv 论文自动化检索，当用户提出需要检索指定主题、指定搜索词、指定时间范围内的arXiv论文时，使用本技能。
---

# 处理流程

1. 使用 `mcporter call arxiv.search_papers` 命令搜索论文，参考[references/search-papers.md](references/search-papers.md)

2. 将 `mcporter call arxiv.search_papers` 命令的返回结果保存到 `~/.cache/searched_arxiv_papers/{time}.json` 文件中，time为当前的执行时间，格式为 `YYYY-MM-DD HH:MM:SS`

3. 执行 `python scripts/parse_useful_arxiv_url.py --src-file ~/.cache/searched_arxiv_papers/{time}.json --readed_papers ~/.cache/readed_papers.json --dst-file ~/.cache/useful_arxiv_src_urls/{time}.json` 获取没有阅读过的 arXiv 论文 URL 列表（输出文件为 `[{ "id": "...", "url": "https://arxiv.org/src/..." }, ...]`，如果返回的列表为空，则表示本次结果都已读过或被去重。

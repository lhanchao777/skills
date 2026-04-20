---
name: arxiv-paper-reading
description: Use this skill when asked to read an arxiv paper given an arxiv URL or arxiv paper id like '2504.13958', '2407.19056'
---

You will be given a URL of an arxiv paper URL, for example: https://arxiv.org/abs/2407.19056.

You will also be given an arxiv id (the number part in last of the paper URL), such as '2504.13958', '2407.19056'

### Part 1: Normalize the URL

The goal is to fetch the TeX Source of the paper (not the PDF!), the URL always looks like this:

https://www.arxiv.org/src/2601.07372

Notice the /src/ in the url. Once you have the URL.


### Part 2: Download the paper source

Fetch the url to a local .tar.gz file. A good location is `~/.cache/arxiv_papers/{arxiv_id}.tar.gz`.

(If the file already exists, there is no need to re-download it).

### Part 3: Unpack the file in that folder

Unpack the contents into `~/.cache/arxiv_papers/{arxiv_id}` directory.

### Part 4: Locate the entrypoint

Every latex source usually has an entrypoint, such as `main.tex` or something like that.

### Part 5: Read the paper

Once you've found the entrypoint, Read the contents and then recurse through all other relevant source files to read the paper.

### Part 6: Report

Once you've read the paper, produce a summary of the paper into a markdown file at `~/.cache/arxiv_paper_summaries/summary_{arxiv_id}.md`

The summary markdown file should be written in Chinese and be organized following the template in [references/analysis-template.md](references/analysis-template.md)


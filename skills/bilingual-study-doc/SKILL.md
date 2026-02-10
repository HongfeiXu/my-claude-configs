---
name: bilingual-study-doc
description: |
  Create bilingual (English-Chinese) study documents from English periodicals, magazines, or articles.
  Use when user uploads PDF/document files of English publications (The Economist, Time, The Atlantic, 
  Harvard Business Review, Scientific American, etc.) and wants to create study materials.
  
  Triggers: "翻译", "双语", "学习", "对照", "bilingual", "study document", "学英语", "英语学习",
  "帮我翻译这篇文章", "创建学习文档", "提取文章并翻译", "选几篇文章"
  
  Output: Markdown file with paragraph-by-paragraph English-Chinese alignment, plus vocabulary lists 
  with example sentences for language learning.
---

# Bilingual Study Document Generator

Create professional bilingual study documents from English periodicals for language learning.

## Workflow

### Step 1: Extract Content from Source

```python
import pdfplumber

def extract_pdf_text(pdf_path):
    """Extract text from PDF, preserving structure"""
    all_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_pages.append(text)
    return '\n\n'.join(all_pages)
```

For PDF files, use `pdfplumber` (install: `pip install pdfplumber --break-system-packages`).

### Step 2: Identify Article Boundaries

Common patterns for article separation:
- URL markers: `This article was downloaded from...`
- Section headers: `Leaders`, `Business`, `Culture`, etc.
- Date lines: `January 22nd 2026`
- Bylines and author credits

```python
import re

def split_articles(full_text, separator_pattern):
    """Split text into individual articles"""
    # Example for Economist-style documents
    pattern = r'This article was downloaded by.*?from (https://[^\n]+)'
    matches = list(re.finditer(pattern, full_text))
    
    articles = []
    for i, match in enumerate(matches):
        start = matches[i-1].end() if i > 0 else 0
        end = match.start()
        content = full_text[start:end].strip()
        url = match.group(1)
        articles.append({'content': content, 'url': url})
    return articles
```

### Step 3: Clean and Format Paragraphs

PDF extraction often breaks paragraphs at line endings. Fix this:

```python
def fix_paragraphs(text):
    """Merge lines broken by PDF extraction into proper paragraphs"""
    lines = text.split('\n')
    result = []
    current_para = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_para:
                result.append(' '.join(current_para))
                current_para = []
        else:
            # Handle hyphenated words at line breaks
            if current_para and current_para[-1].endswith('-'):
                current_para[-1] = current_para[-1][:-1] + line
            else:
                current_para.append(line)
    
    if current_para:
        result.append(' '.join(current_para))
    return result
```

### Step 4: Generate Bilingual Markdown

Use this output structure:

```markdown
# [Publication Name] [Issue Date]

> **学习指南 | Study Guide**
> 格式：英文原文（引用块）后紧跟中文翻译

---

## [Article Title]
## [中文标题]

**[Section] | [分类]**  
*[Subtitle]*  
*[副标题翻译]*

📅 [Date]

---

> [English paragraph 1]

[中文翻译段落 1]

---

> [English paragraph 2]

[中文翻译段落 2]

---

### 📚 重点词汇 | Key Vocabulary

| 词汇 | 音标 | 释义 | 例句 |
|------|------|------|------|
| **word** | /phonetic/ | n. 词性+释义 | *Example sentence from article* |
```

### Step 5: Select Vocabulary

For each article, select 5-10 key vocabulary items based on:

1. **Difficulty**: Advanced/academic words (not basic vocabulary)
2. **Usefulness**: High-frequency in business/academic English
3. **Context**: Words that are best learned in context
4. **Variety**: Mix of nouns, verbs, adjectives, phrases

Good vocabulary examples:
- `diatribe` (n. 长篇抨击)
- `conciliatory` (adj. 和解的)
- `penny-pinching` (adj. 精打细算的)
- `crack the code` (phrase 破解密码)

### Step 6: Article Selection Guidelines

When user asks to select articles, choose based on:

1. **Topic diversity**: Different sections (politics, business, tech, culture)
2. **Content richness**: Articles with substantial paragraphs (>500 words)
3. **Learning value**: Rich vocabulary and varied sentence structures
4. **Interest**: Engaging topics that motivate continued reading

## Output Format Options

### Full Translation (Default)
- Every paragraph translated
- Complete vocabulary list
- Best for intensive study

### Summary Mode
- Key paragraphs only
- Extended vocabulary (10-15 words)
- Best for review/overview

### Vocabulary Focus
- Minimal translation
- Expanded vocabulary (15-20 words)
- Multiple example sentences per word
- Best for vocabulary building

## Quality Checklist

Before finalizing output, verify:

- [ ] Paragraphs properly merged (no mid-sentence breaks)
- [ ] Translations accurate and natural
- [ ] Vocabulary includes phonetics
- [ ] Example sentences are from original text
- [ ] Markdown renders correctly
- [ ] File saved to `/mnt/user-data/outputs/`

## Common Publication Patterns

| Publication | Article Separator | Section Headers |
|-------------|-------------------|-----------------|
| The Economist | URL markers | Leaders, Briefing, Business, etc. |
| The New Yorker | Author bylines | Comment, Profiles, Fiction, etc. |
| The Atlantic | --- dividers | Ideas, Politics, Culture, etc. |
| Wired | Author bylines | Ideas, Gear, Science, etc. |
| Time | Page breaks | Nation, World, Ideas, etc. |
| HBR | Article titles | Features, Ideas, Case Studies |

## Tips for Better Results

1. **Ask user preference**: Number of articles, topics of interest
2. **Preview before translating**: Show article list for selection
3. **Batch processing**: Process multiple articles efficiently
4. **Preserve formatting**: Keep emphasis, lists, quotes from original

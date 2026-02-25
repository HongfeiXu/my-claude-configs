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

**Preferred**: Use Claude's built-in `Read` tool to read PDF files directly (supports up to 20 pages per request via the `pages` parameter). This requires no extra dependencies.

**Fallback** (for large PDFs or batch processing): Use the helper script at `scripts/extract_pdf.py`:

```bash
pip install --user pdfplumber
python scripts/extract_pdf.py input.pdf -o output.json
python scripts/extract_pdf.py input.pdf -f economist -o output.json  # Economist-specific splitting
```

The script handles: text extraction, paragraph merging (fixing PDF line breaks), article splitting (Economist URL markers), and ad/noise cleanup.

### Step 2: Identify Article Boundaries

Common patterns for article separation (see `references/publications.md` for per-publication details):
- URL markers: `This article was downloaded from...`
- Section headers: `Leaders`, `Business`, `Culture`, etc.
- Date lines: `January 22nd 2026`
- Bylines and author credits

### Step 3: Clean and Format Paragraphs

PDF extraction often breaks paragraphs at line endings. The `scripts/extract_pdf.py` script handles this automatically (merging broken lines, fixing hyphenated words). When using the `Read` tool directly, manually check for and fix mid-sentence line breaks before translating.

### Step 4: Generate Bilingual Markdown

Use this output structure:

```markdown
# [Publication Name] [Issue Date]

> **学习指南 | Study Guide**
> 格式：英文原文后紧跟中文翻译（灰色引用块）

---

## [Article Title]
## [中文标题]

**[Section] | [分类]**
*[Subtitle]*
*[副标题翻译]*

---

[English paragraph 1]

> [中文翻译段落 1]

---

[English paragraph 2]

> [中文翻译段落 2]

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
- [ ] File saved to user's preferred output directory (ask user if not specified)

## Common Publication Patterns

| Publication | Article Separator | Section Headers |
|-------------|-------------------|-----------------|
| The Economist | URL markers | Leaders, Briefing, Business, etc. |
| The New Yorker | Author bylines | Comment, Profiles, Fiction, etc. |
| The Atlantic | --- dividers | Ideas, Politics, Culture, etc. |
| Wired | Author bylines | Ideas, Gear, Science, etc. |
| Time | Page breaks | Nation, World, Ideas, etc. |
| HBR | Article titles | Features, Ideas, Case Studies |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| PDF text extraction garbled | Scanned/image-based PDF | Ask user for a text-based PDF or OCR version |
| PDF is encrypted/password-protected | DRM protection | Cannot process; ask user to provide an unlocked version |
| pdfplumber not installed | Missing dependency | Use Claude's built-in `Read` tool instead (supports PDF natively, up to 20 pages per request) |
| Large PDF (>20 pages) | Exceeds Read tool limit | Use `Read` with `pages` parameter for specific ranges, or use `scripts/extract_pdf.py` |
| Broken paragraphs after extraction | PDF line-break artifacts | Run through `scripts/extract_pdf.py` or manually merge lines before translating |

## Tips for Better Results

1. **Ask user preference**: Number of articles, topics of interest
2. **Preview before translating**: Show article list for selection
3. **Batch processing**: Process multiple articles efficiently
4. **Preserve formatting**: Keep emphasis, lists, quotes from original

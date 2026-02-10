#!/usr/bin/env python3
"""
PDF Text Extraction Utility for Bilingual Study Documents
"""

import re
import json
import argparse


def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file"""
    import pdfplumber
    
    all_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                all_pages.append(text)
    return '\n\n'.join(all_pages)


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
            if current_para and current_para[-1].endswith('-'):
                current_para[-1] = current_para[-1][:-1] + line
            else:
                current_para.append(line)
    
    if current_para:
        result.append(' '.join(current_para))
    return result


def split_articles_economist(full_text):
    """Split Economist-style PDF into individual articles"""
    pattern = r'This article was downloaded by.*?from (https://www\.economist\.com//[^\n]+)'
    matches = list(re.finditer(pattern, full_text))
    
    articles = []
    for i, match in enumerate(matches):
        url = match.group(1)
        end_pos = match.start()
        start_pos = matches[i-1].end() if i > 0 else 0
        
        content = full_text[start_pos:end_pos].strip()
        
        # Extract category from URL
        category = url.split('//')[-1].split('/')[0] if '//' in url else 'unknown'
        
        articles.append({
            'content': content,
            'url': url,
            'category': category
        })
    
    return articles


def clean_content(text):
    """Remove ads and unwanted content"""
    # Common ad patterns (customize as needed)
    ad_patterns = [
        r'优质App推荐.*?点击下载',
        r'英阅阅读器.*?点击下',
        r'Notability.*?点击下载',
        r'欧路词典.*?点击下载',
        r'Duolingo.*?点击下载',
    ]
    
    for pattern in ad_patterns:
        text = re.sub(pattern, '', text, flags=re.DOTALL)
    
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def main():
    parser = argparse.ArgumentParser(description='Extract text from PDF for bilingual study')
    parser.add_argument('pdf_path', help='Path to PDF file')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    parser.add_argument('--format', '-f', choices=['economist', 'generic'], 
                        default='generic', help='Document format')
    
    args = parser.parse_args()
    
    # Extract text
    full_text = extract_text_from_pdf(args.pdf_path)
    full_text = clean_content(full_text)
    
    if args.format == 'economist':
        articles = split_articles_economist(full_text)
        result = {'articles': articles, 'count': len(articles)}
    else:
        paragraphs = fix_paragraphs(full_text)
        result = {'paragraphs': paragraphs, 'count': len(paragraphs)}
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

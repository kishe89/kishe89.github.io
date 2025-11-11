#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import re
import os
from pathlib import Path

def remove_front_matter(content):
    """Jekyll front matter 제거"""
    # Front matter는 ---로 시작하고 끝남
    pattern = r'^---\s*\n(.*?\n)---\s*\n'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    return content.strip()

def markdown_to_pdf(md_file, pdf_file):
    """마크다운 파일을 PDF로 변환"""
    # 현재 작업 디렉토리 가져오기
    base_dir = Path(md_file).parent.absolute()
    
    # 마크다운 파일 읽기
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Front matter 제거
    md_content = remove_front_matter(md_content)
    
    # Jekyll 변수 처리 ({{ site.baseurl }} 등)
    md_content = md_content.replace('{{ site.baseurl }}', '')
    
    # 마크다운을 HTML로 변환 (기본적으로 HTML 태그는 유지됨)
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'nl2br']
    )
    
    # 이미지 경로를 절대 경로로 변환
    # 상대 경로(/assets/...)를 절대 경로로 변환
    def fix_image_paths(html):
        # <img src="/assets/..." 형태를 절대 경로로 변환
        pattern = r'src="(/assets/[^"]+)"'
        def replace_path(match):
            rel_path = match.group(1)
            abs_path = base_dir / rel_path.lstrip('/')
            # 파일 존재 여부 확인
            if not abs_path.exists():
                print(f"경고: 이미지 파일을 찾을 수 없습니다: {abs_path}")
            # Windows 경로를 file:// URL 형식으로 변환
            return f'src="{abs_path.as_uri()}"'
        return re.sub(pattern, replace_path, html)
    
    html_content = fix_image_paths(html_content)
    
    # HTML 래퍼 추가
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #333;
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #2c3e50;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }}
            h1 {{ font-size: 24pt; }}
            h2 {{ font-size: 20pt; }}
            h3 {{ font-size: 16pt; }}
            h4 {{ font-size: 14pt; }}
            h5 {{ font-size: 12pt; }}
            h6 {{ font-size: 11pt; }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
            }}
            table th, table td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            table th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            hr {{
                border: none;
                border-top: 1px solid #ddd;
                margin: 2em 0;
            }}
            img {{
                max-width: 100%;
                height: auto;
            }}
            img.profile {{
                max-width: 200px;
                width: 200px;
                height: auto;
                border-radius: 50%;
                display: block;
                margin: 1em 0;
            }}
            ul, ol {{
                margin: 1em 0;
                padding-left: 2em;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 1em;
                border-radius: 5px;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # PDF 생성 (base_url을 설정하여 이미지 경로 해결)
    HTML(string=full_html, base_url=str(base_dir)).write_pdf(pdf_file)
    print(f"PDF 파일이 생성되었습니다: {pdf_file}")

if __name__ == '__main__':
    markdown_to_pdf('about.md', 'about.pdf')


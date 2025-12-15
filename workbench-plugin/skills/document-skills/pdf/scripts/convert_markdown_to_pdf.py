#!/usr/bin/env python3
"""
Simple, fast Markdown to PDF converter with professional formatting.

Uses reportlab for direct PDF generation - no external dependencies beyond Python.
Fast, reliable, and produces professional-looking documents.

Usage:
    python3 convert_markdown_to_pdf.py input.md output.pdf

    Or if running from project root with venv:
    .venv/bin/python3 convert_markdown_to_pdf.py input.md output.pdf
"""

import argparse
import sys
import re
import warnings
from pathlib import Path

# Suppress all warnings for cleaner output
warnings.filterwarnings('ignore')

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY


def sanitize_text(text):
    """Remove or replace characters that can't be rendered in PDF."""
    # Common emoji and symbol replacements
    emoji_map = {
        '✅': '[YES]', '❌': '[NO]', '⚠️': '[!]', '⭐': '[*]',
        '✓': '[YES]', '✗': '[NO]', '★': '[*]', '☆': '[*]',
        '→': '->', '←': '<-', '↔': '<->', '•': '-',
        '►': '>', '▶': '>', '▼': 'v', '▲': '^', '■': '-', '□': '-',
        '├': '|', '└': '|', '─': '-', '│': '|',
        '📍': '[LOC]', '📅': '[DATE]', '📧': '[EMAIL]', '📞': '[PHONE]',
        '🔗': '[LINK]', '📝': '[NOTE]', '💡': '[TIP]', '🎯': '[TARGET]',
        '🚀': '[GO]', '⚡': '[FAST]', '🔥': '[HOT]', '❤️': '[LOVE]',
        '👍': '[OK]', '👎': '[BAD]', '🎉': '[YAY]', '🏆': '[WIN]',
        '📊': '[CHART]', '📈': '[UP]', '📉': '[DOWN]',
        '🌟': '[*]', '💪': '[STRONG]', '🤔': '[?]', '😊': ':)',
        '—': '-', '–': '-', '"': '"', '"': '"', ''': "'", ''': "'",
        '…': '...', '°': 'deg', '±': '+/-', '×': 'x', '÷': '/',
        'Å': 'A', 'å': 'a', 'Ø': 'O', 'ø': 'o', 'Æ': 'AE', 'æ': 'ae',
    }
    for emoji, replacement in emoji_map.items():
        text = text.replace(emoji, replacement)

    # Remove **bold** markers (convert to plain text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)

    return text


def parse_markdown_table(lines, start_idx):
    """Parse a markdown table starting at start_idx."""
    table_lines = []
    i = start_idx

    while i < len(lines) and '|' in lines[i]:
        table_lines.append(lines[i])
        i += 1

    if len(table_lines) < 2:
        return None, start_idx

    # Parse table
    rows = []
    for line in table_lines:
        if re.match(r'^\s*\|[\s\-:|]+\|', line):  # Separator line
            continue
        # Process cells and handle <br> tags
        cells = []
        for cell in line.split('|')[1:-1]:
            cell = cell.strip()
            # Replace <br> with line break for reportlab
            cell = cell.replace('<br>', '\n')
            cell = sanitize_text(cell)
            cells.append(cell)
        rows.append(cells)

    return rows, i


def create_professional_pdf(input_file: str, output_file: str):
    """Create a professional PDF from markdown."""

    # Read markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    # Create PDF
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Styles
    styles = getSampleStyleSheet()

    # Ocean Depths Theme Colors
    # Deep Navy #1a2332, Teal #2d8b8b, Seafoam #a8dadc, Cream #f1faee

    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a2332'),  # Deep Navy
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1a2332'),  # Deep Navy
        spaceBefore=12,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )

    h3_style = ParagraphStyle(
        'H3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#1a2332'),  # Deep Navy
        spaceBefore=8,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY
    )

    list_style = ParagraphStyle(
        'List',
        parent=body_style,
        leftIndent=30,
        bulletIndent=15,
        spaceAfter=4
    )

    # Build story
    story = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Page break - only for explicit page break divs, ignore --- separators
        if '<div style="page-break-after: always;"></div>' in line:
            story.append(PageBreak())
            i += 1
            continue

        # Horizontal rule separator (not a page break)
        if line.strip() == '---':
            story.append(Spacer(1, 12))
            i += 1
            continue

        # Code block - skip ``` markers and filter decorative lines
        if line.strip().startswith('```'):
            i += 1
            # Process lines inside code block
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_line = lines[i].rstrip()
                # Skip purely decorative lines (only box chars, arrows, pipes)
                stripped = code_line.strip()
                if stripped and not re.match(r'^[\s\|\-\>\<\^\v├└─│►▶▼▲■□]+$', stripped):
                    # Keep substantive content
                    text = sanitize_text(code_line)
                    if text.strip():
                        story.append(Paragraph(text, body_style))
                i += 1
            i += 1  # Skip closing ```
            continue

        # Title (# )
        if line.startswith('# '):
            text = sanitize_text(line[2:])
            story.append(Paragraph(text, title_style))
            i += 1
            continue

        # H2 (## )
        if line.startswith('## '):
            text = sanitize_text(line[3:])
            story.append(Paragraph(text, h2_style))
            i += 1
            continue

        # H3 (### )
        if line.startswith('### '):
            text = sanitize_text(line[4:])
            story.append(Paragraph(text, h3_style))
            i += 1
            continue

        # H4 (#### )
        if line.startswith('#### '):
            text = sanitize_text(line[5:])
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            story.append(Paragraph(text, h3_style))
            i += 1
            continue

        # Table
        if '|' in line and i + 1 < len(lines) and '|' in lines[i+1]:
            table_data, next_i = parse_markdown_table(lines, i)
            if table_data:
                # Determine column count
                num_cols = len(table_data[0])

                # Calculate column widths and font sizes based on table width
                page_width = 7.0 * inch  # Letter size with margins

                if num_cols >= 7:  # Wide table (like Query Performance)
                    # Calculate equal column widths
                    col_widths = [page_width / num_cols] * num_cols
                    header_font = 7
                    cell_font = 6.5
                    padding = 3
                elif num_cols >= 5:
                    col_widths = [page_width / num_cols] * num_cols
                    header_font = 8
                    cell_font = 7
                    padding = 4
                else:  # Normal table
                    col_widths = None  # Auto-calculate
                    header_font = 9
                    cell_font = 8
                    padding = 4

                # Wrap text in cells for proper line breaks
                wrapped_data = []
                for row_idx, row in enumerate(table_data):
                    wrapped_row = []
                    for cell in row:
                        if row_idx == 0:  # Header
                            wrapped_row.append(Paragraph(f'<b>{cell}</b>', body_style))
                        else:
                            wrapped_row.append(Paragraph(cell, body_style))
                    wrapped_data.append(wrapped_row)

                # Create table with column widths
                t = Table(wrapped_data, colWidths=col_widths, repeatRows=1)

                # Style - Ocean Depths Theme
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d8b8b')),  # Teal header
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), header_font),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTSIZE', (0, 1), (-1, -1), cell_font),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#708090')),  # Slate gray grid
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f1faee'), colors.HexColor('#a8dadc')]),  # Cream/Seafoam
                    ('TOPPADDING', (0, 0), (-1, -1), padding),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), padding),
                    ('LEFTPADDING', (0, 0), (-1, -1), padding),
                    ('RIGHTPADDING', (0, 0), (-1, -1), padding),
                ])

                t.setStyle(table_style)
                story.append(t)
                story.append(Spacer(1, 12))
                i = next_i
                continue

        # Bold metadata
        if line.startswith('**') and '**' in line[2:]:
            text = sanitize_text(line)
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            story.append(Paragraph(text, body_style))
            i += 1
            continue

        # List items
        if line.startswith(('- ', '* ', '✅ ', '❌ ', '⚠️ ')):
            # Extract text after the bullet/emoji
            text = line.lstrip('- *✅❌⚠️ ')

            # Convert emoji to ASCII-safe symbols at start if present
            if line.startswith('✅ '):
                text = f'[YES] {text}'
            elif line.startswith('❌ '):
                text = f'[NO] {text}'
            elif line.startswith('⚠️ '):
                text = f'[!] {text}'

            text = sanitize_text(text)
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'`([^`]+)`', r'<font name="Courier" size="8">\1</font>', text)
            story.append(Paragraph(f'- {text}', list_style))
            i += 1
            continue

        # Numbered list
        if re.match(r'^\d+\.\s', line):
            text = re.sub(r'^\d+\.\s+', '', line)
            text = sanitize_text(text)
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'`([^`]+)`', r'<font name="Courier" size="8">\1</font>', text)
            story.append(Paragraph(text, list_style))
            i += 1
            continue

        # Regular paragraph
        text = sanitize_text(line)
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'`([^`]+)`', r'<font name="Courier" size="8">\1</font>', text)
        text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)

        if text.strip():
            story.append(Paragraph(text, body_style))
            story.append(Spacer(1, 4))

        i += 1

    # Build PDF
    doc.build(story)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Convert Markdown to PDF with professional formatting',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('input', help='Input Markdown file')
    parser.add_argument('output', help='Output PDF file')

    args = parser.parse_args()

    # Check input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        create_professional_pdf(args.input, args.output)
        print(f"✓ {args.output}")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

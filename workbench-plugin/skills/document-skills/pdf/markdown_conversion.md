# Markdown to PDF Conversion Guide

This guide covers converting Markdown files to professionally formatted PDFs using the PDF skill.

## Quick Start

### Basic Conversion

```bash
python3 scripts/convert_markdown_to_pdf.py input.md output.pdf
```

### With Custom Styling

```bash
python3 scripts/convert_markdown_to_pdf.py input.md output.pdf --css custom.css
```

### Using Pandoc Directly

```bash
pandoc input.md -o output.pdf
```

---

## Conversion Methods

### Method 1: Pandoc (Recommended)

Pandoc is the industry-standard tool for document conversion with excellent formatting capabilities.

**Advantages:**
- Professional-quality PDF output
- Table of contents generation
- Syntax highlighting for code blocks
- Extensive customization options
- Handles complex documents with tables, images, and math

**Installation:**
```bash
brew install pandoc
```

**Basic usage:**
```bash
pandoc document.md -o document.pdf
```

### Method 2: Python Fallback

Uses Python's `markdown` and `reportlab` libraries when pandoc is unavailable.

**Advantages:**
- No external dependencies (besides Python packages)
- Works everywhere Python is available
- Simpler, more predictable output

**Disadvantages:**
- Basic formatting only
- Limited table support
- No syntax highlighting
- Less sophisticated layout

**Usage:**
```bash
python3 scripts/convert_markdown_to_pdf.py input.md output.pdf --fallback
```

---

## Styling Options

### Using CSS (Pandoc)

Create a custom CSS file for styling:

```css
/* custom-style.css */
body {
    font-family: Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
}

h1 {
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 0.3em;
}

table {
    border-collapse: collapse;
    width: 100%;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #f2f2f2;
}
```

Apply the CSS:
```bash
python3 scripts/convert_markdown_to_pdf.py input.md output.pdf --css custom-style.css
```

### Using Templates (Pandoc)

Pandoc supports custom LaTeX templates for advanced formatting:

```bash
python3 scripts/convert_markdown_to_pdf.py input.md output.pdf --template mytemplate.tex
```

---

## Adding Metadata

Add document metadata like title, author, and date:

```bash
python3 scripts/convert_markdown_to_pdf.py input.md output.pdf \
    --metadata title="My Report" \
    --metadata author="John Doe" \
    --metadata date="2025-11-07"
```

Or include metadata in your Markdown file:

```markdown
---
title: My Report
author: John Doe
date: 2025-11-07
---

# Chapter 1
Content here...
```

---

## PDF Engines

Different PDF engines provide different capabilities:

### pdflatex (Default)

Best for general documents with text, tables, and basic formatting.

```bash
python3 scripts/convert_markdown_to_pdf.py input.md output.pdf --engine pdflatex
```

### xelatex

Better Unicode support and modern fonts.

```bash
python3 scripts/convert_markdown_to_pdf.py input.md output.pdf --engine xelatex
```

### wkhtmltopdf

HTML/CSS-based rendering (requires wkhtmltopdf installation).

```bash
python3 scripts/convert_markdown_to_pdf.py input.md output.pdf --engine wkhtmltopdf
```

---

## Common Use Cases

### Technical Documentation

```bash
# With table of contents, numbered sections, and syntax highlighting
pandoc technical-doc.md -o technical-doc.pdf \
    --toc \
    --number-sections \
    --highlight-style=tango \
    -V geometry:margin=1in
```

### Reports with Tables

Markdown tables are automatically converted:

```markdown
| Metric | Value | Status |
|--------|-------|--------|
| Speed  | 95ms  | ✅ Fast |
| Memory | 512MB | ⚠️ High |
```

### Code Documentation

Code blocks with syntax highlighting:

````markdown
```python
def hello_world():
    print("Hello, World!")
```
````

### Academic Papers

```bash
pandoc paper.md -o paper.pdf \
    --citeproc \
    --bibliography=references.bib \
    --csl=ieee.csl
```

---

## Troubleshooting

### Issue: "Pandoc not found"

**Solution:** Install pandoc via homebrew:
```bash
brew install pandoc
```

### Issue: LaTeX errors

**Solution:** Install a LaTeX distribution:
```bash
brew install basictex
```

### Issue: Poor table formatting

**Solution:** Use HTML tables in your Markdown for more control:

```html
<table>
  <tr>
    <th>Header</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Data</td>
    <td>123</td>
  </tr>
</table>
```

### Issue: Images not appearing

**Solution:** Use absolute paths or ensure images are in the same directory:

```markdown
![My Image](./path/to/image.png)
```

### Issue: Python fallback looks basic

**Solution:** Install pandoc for professional output, or customize the Python script for your needs.

---

## Advanced Features

### Custom Page Margins

```bash
pandoc input.md -o output.pdf -V geometry:margin=0.75in
```

### Different Page Sizes

```bash
pandoc input.md -o output.pdf -V papersize:a4
pandoc input.md -o output.pdf -V papersize:letter
```

### Font Customization

```bash
pandoc input.md -o output.pdf \
    -V mainfont="Times New Roman" \
    -V fontsize=12pt
```

### Include Multiple Files

```bash
pandoc intro.md chapter1.md chapter2.md -o book.pdf
```

---

## Best Practices

1. **Use semantic Markdown**: Proper heading hierarchy (# → ## → ###)
2. **Keep it simple**: Markdown is designed for readable, simple markup
3. **Test early**: Convert small samples to verify formatting before converting large documents
4. **Use version control**: Keep your source Markdown files in git
5. **Separate content and style**: Use CSS/templates for styling, keep Markdown clean
6. **Add metadata**: Include title, author, and date for professional documents
7. **Check file paths**: Ensure all images and referenced files are accessible

---

## Script Options Reference

```
Usage: python3 convert_markdown_to_pdf.py input.md output.pdf [options]

Options:
  --css FILE          Apply custom CSS styling (pandoc only)
  --template FILE     Use custom pandoc template
  --metadata KEY=VAL  Add metadata (e.g., title, author)
  --fallback          Force use of Python fallback method
  --engine ENGINE     PDF engine: pdflatex, xelatex, or wkhtmltopdf
```

### Examples

```bash
# Basic conversion
python3 scripts/convert_markdown_to_pdf.py report.md report.pdf

# With custom CSS
python3 scripts/convert_markdown_to_pdf.py report.md report.pdf --css style.css

# With metadata
python3 scripts/convert_markdown_to_pdf.py report.md report.pdf \
    --metadata title="Quarterly Report" \
    --metadata author="Finance Team"

# Force Python fallback
python3 scripts/convert_markdown_to_pdf.py report.md report.pdf --fallback

# Use different PDF engine
python3 scripts/convert_markdown_to_pdf.py report.md report.pdf --engine xelatex
```

---

## See Also

- [Pandoc User's Guide](https://pandoc.org/MANUAL.html)
- [Markdown Guide](https://www.markdownguide.org/)
- [LaTeX Documentation](https://www.latex-project.org/)
- PDF Skill: Other PDF manipulation capabilities (merge, split, extract, forms)

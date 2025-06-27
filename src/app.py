import os
import re
import sys
import argparse

from pathlib import Path
from markdown import markdown, Markdown
from playwright.sync_api import sync_playwright
from markdown.extensions.toc import TocExtension

from html_template import HTML_TEMPLATE


def get_parser():
    parser = argparse.ArgumentParser(
        prog="Md2Pdf", description="Convert a markdown file to pdf file"
    )

    parser.add_argument("filename", help="Input filename")
    parser.add_argument("--output_dir", help="Output directory", required=False)
    parser.add_argument("--output_file", help="Output filename", required=False)
    parser.add_argument(
        "--style",
        "-s",
        help="style sheet CSS",
        required=False,
        default="./styles/default.css",
    )
    parser.add_argument(
        "--html", help="Save the auxiliar HTML file", action="store_true"
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=[
            "Letter",
            "Legal",
            "Tabloid",
            "Ledger",
            "A0",
            "A1",
            "A2",
            "A3",
            "A4",
            "A5",
            "A6",
        ],
        help="Format file",
        default="Letter",
        required=False,
    )

    return parser


def convert_mermaid_blocks(md_text: str) -> str:
    """Convert Mermaid code blocks to <div class="mermaid">...</div>

    Args:
        md_text (str): _description_

    Returns:
        str: _description_
    """
    return re.sub(
        r"```mermaid\n(.*?)```",
        r'<div class="mermaid">\n\1</div>',
        md_text,
        flags=re.DOTALL,
    )


def export_task(**kwargs) -> None:
    try:
        filename = kwargs["filename"]
        output_directory = "" if kwargs["output_dir"] is None else kwargs["output_dir"]
        stylesheet = os.path.abspath(kwargs["style"])

        name, _ = os.path.splitext(os.path.basename(filename))
        output_name = name if kwargs["output_file"] is None else kwargs["output_file"]
        output_name, _ = os.path.splitext(os.path.basename(output_name))

        pdf_output_file = os.path.join(output_directory, output_name + ".pdf")
        html_output_file = os.path.join(output_directory, output_name + ".html")

        os.makedirs(output_directory, exist_ok=True)

        # Read Markdown file
        md_content = ""
        with open(filename, "r", encoding="utf-8") as f:
            filtered_lines = []
            for line in f.readlines():
                if line.strip().startswith("#") and "<!-- omit in toc -->" in line:
                    # Replace the heading with a paragraph or blank so it's not added to TOC
                    # You can also just skip it if you don't want it in the HTML at all
                    # Example: filtered_lines.append("")
                    header_html = "<h{0}>{1}</h{0}>"
                    new_line = re.sub(r"\s*<!-- omit in toc -->", "", line).strip()
                    header = new_line.split(maxsplit=1)
                    filtered_lines.append(
                        header_html.format(len(header[0]), header[1])
                    )  # keep in HTML, omit from TOC
                else:
                    filtered_lines.append(line)
            md_content = "\n".join(filtered_lines)

        # Convert Mermaid blocks
        md_content = convert_mermaid_blocks(md_content)

        md_obj = Markdown(
            tab_length=2,
            extensions=[
                "fenced_code",
                "tables",
                "md_in_html",
                TocExtension(toc_depth="2-5"),
            ],
        )

        # Convert Markdown to HTML
        html_body = md_obj.convert(md_content)

        # Create full HTML with Mermaid JS (non-module)
        html_template = HTML_TEMPLATE.format(output_name, stylesheet, html_body)

        # Save HTML file
        html_path = Path(html_output_file)
        html_path.write_text(html_template, encoding="utf-8")

        # Export to PDF with Playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(html_path.absolute().as_uri())
            page.wait_for_timeout(3000)  # wait for JS to render Mermaid
            page.pdf(
                path=pdf_output_file,
                format=kwargs["format"],
                display_header_footer=False,
                header_template="<div></div>",
                footer_template="<div style=\"font-size: 9px; margin: 0 auto;\"><span class='pageNumber'></span></div>",
            )
            browser.close()

        if not kwargs["html"]:
            os.remove(html_output_file)

        print("✅ PDF exported")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    kwargs = vars(get_parser().parse_args(sys.argv[1:]))
    export_task(**kwargs)

# Markdown to PDF

```sh
usage: Md2Pdf [-h] [--output_dir OUTPUT_DIR] [--output_file OUTPUT_FILE] [--style STYLE] [--html]
              [--format {Letter,Legal,Tabloid,Ledger,A0,A1,A2,A3,A4,A5,A6}]
              filename
```

Convert a markdown file to pdf file

```sh
positional arguments:
filename              Input filename

options:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR
                        Output directory
  --output_file OUTPUT_FILE
                        Output filename
  --style STYLE, -s STYLE
                        style sheet CSS
  --html                Save the auxiliar HTML file
  --format {Letter,Legal,Tabloid,Ledger,A0,A1,A2,A3,A4,A5,A6}, -f {Letter,Legal,Tabloid,Ledger,A0,A1,A2,A3,A4,A5,A6}
                        Format file
```

## Example

```sh
python src/app.py path/document.md --output_dir path/output
```
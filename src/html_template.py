HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{0}</title>
  <link rel="stylesheet" href="{1}">
</head>
<body>
  {2}
</body>
<script src="https://unpkg.com/mermaid/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{ startOnLoad: true }});
</script>
</html>
"""
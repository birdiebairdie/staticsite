import os
from pathlib import Path
from block_markdown import markdown_to_html_node

def generate_pages_recursive(
  dir_path_content, 
  template_path, 
  dest_dir_path,
  ):

  for file in os.listdir(dir_path_content):
    from_path = os.path.join(dir_path_content, file)
    dest_path = os.path.join(dest_dir_path, file)
    if os.path.isfile(from_path):
      dest_path = Path(dest_path).with_suffix('.html')
      generate_page(from_path, template_path, dest_path)
    else:
      generate_pages_recursive(from_path, template_path, dest_path)
  

def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")

  with open(from_path) as f:
    source = f.read()

  with open(template_path) as f:
    template = f.read()

  content_node = markdown_to_html_node(source)
  content = content_node.to_html()

  title = extract_title(source)

  template = template.replace('{{ Title }}', title)
  template = template.replace('{{ Content }}', content)

  dest_dir_path = os.path.dirname(dest_path)
  if dest_dir_path != "":
    os.makedirs(dest_dir_path, exist_ok=True)
  to_file = open(dest_path, "w")
  to_file.write(template)

def extract_title(markdown):
  lines = markdown.split('\n')
  for line in lines:
    if line.startswith('# '):
      return line[2:]
  raise ValueError('no title found')

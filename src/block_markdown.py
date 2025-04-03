import re

def markdown_to_blocks(markdown):
  split_markdown = markdown.split("\n\n")
  print(f"initial split: {split_markdown}")
  stripped_markdown = []
  for item in split_markdown:
    if item == "":
      continue
    stripped_markdown.append(item.strip())
  print(f"after stripping: {stripped_markdown}")
  pattern = "(\s{2,})"
  final = []
  for item in stripped_markdown:
    final.append(re.sub(pattern, '\n', item))
  print(f"final: {final}")
  return final 

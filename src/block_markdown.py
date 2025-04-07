import re
from enum import Enum

class BlockType(Enum):
  PARAGRAPH = 'paragraph'
  HEADING = 'heading'
  CODE = 'code'
  QUOTE = 'quote'
  ULIST = 'unordered_list'
  OLIST = 'ordered_list'

def markdown_to_blocks(markdown):
  split_markdown = markdown.split("\n\n")
  stripped_markdown = []
  for item in split_markdown:
    if item == "":
      continue
    stripped_markdown.append(item.strip())
  pattern = "(\s{2,})"
  final = []
  for item in stripped_markdown:
    final.append(re.sub(pattern, '\n', item))
  return final 

def block_to_block_type(markdown):
  lines = markdown.split('\n')
  if re.match('^(#{1,6}\s).', markdown):
    return BlockType.HEADING
  if len(lines) > 1 and re.match('^`{3}\n', markdown) and re.search('\n`{3}$', markdown):
    return BlockType.CODE
  if re.match('^>', markdown):
    for line in lines:
      if not re.match('^>', line):
        return BlockType.PARAGRAPH
    return BlockType.QUOTE
  if re.match('^(- )', markdown):
    for line in lines:
      if line == "":
        continue
      if not re.match ('^(- )', line):
        return BlockType.PARAGRAPH
    return BlockType.ULIST
  if re.match('1. ', markdown):
    i = 1
    for line in lines:
      if line == "":
        continue
      if not re.match (f'^{i}\. ', line):
        return BlockType.PARAGRAPH
      i += 1
    return BlockType.OLIST
  else:
    return BlockType.PARAGRAPH

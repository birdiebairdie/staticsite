import re
from enum import Enum

from htmlnode import ParentNode, HTMLNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

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
  
def markdown_to_html_node(markdown):
  children = []
  blocks = markdown_to_blocks(markdown)
  for block in blocks:
    html_node = block_to_html_node(block)
    children.append(html_node)
  return ParentNode("div", children)

def block_to_html_node(block):
  # take the block type and do something specific for each (needs more helper functions)
  match block_to_block_type(block):
    case BlockType.PARAGRAPH:
      return paragraph_to_html_node(block)
    case BlockType.HEADING:
      return heading_to_html_node(block)
    case BlockType.CODE:
      return code_to_html_node(block)
    case BlockType.QUOTE:
      return quote_to_html_node(block)
    case BlockType.ULIST:
      return ulist_to_html_node(block)
    case BlockType.OLIST:
      return olist_to_html_node(block)
    case _:
      raise ValueError("invalid block type")


def text_to_children(text):
  # turn the input text into text nodes, change each of those to an html node, build a list of children, and return
  children = []
  nodes = text_to_textnodes(text)
  for node in nodes:
    html_node = text_node_to_html_node(node)
    children.append(html_node)
  return children

def paragraph_to_html_node(block):
  # take a block of known type paragraph and return an html parent node
  lines = block.split('\n')
  paragraph = " ".join(lines)
  children = text_to_children(paragraph)
  if not children:
    text_node = TextNode(paragraph, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    children = [html_node]
  return ParentNode('p', children)

def heading_to_html_node(block):
  level = 0
  for char in block:
    if char == '#':
      level += 1
    else:
      break
  # if there are too many #s or if there is no text
  if level > 6 or level >= len(block):
    raise ValueError("invalid heading format")
  text = block[level+1:]
  children = text_to_children(text)
  return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
  lines = block.split('\n')
  new_lines = []
  for line in lines:
    if not re.match('^>', line):
      raise ValueError("invalid quote format")
    new_lines.append(line.lstrip('>').strip())
  text = ' '.join(new_lines)
  children = text_to_children(text)
  return ParentNode("blockquote", children)

def ulist_to_html_node(block):
  list_items = block.split('\n')
  html_items = []
  for item in list_items:
    text = item[2:]
    children = text_to_children(text)
    html_items.append(ParentNode('li', children))
  return ParentNode('ul', html_items)

def olist_to_html_node(block):
  list_items = block.split('\n')
  html_items = []
  for item in list_items:
    text = item[2:]
    children = text_to_children(text)
    html_items.append(ParentNode('li', children))
  return ParentNode('ol', html_items)
    


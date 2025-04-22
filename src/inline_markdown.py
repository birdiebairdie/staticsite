import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, new_text_type):
  # need an empty list to populate
  new_nodes = []

# Handle case where old_nodes might be a single string instead of a list of TextNodes
  if isinstance(old_nodes, str):
      # Convert the string to a TextNode first
      old_nodes = [TextNode(old_nodes, TextType.TEXT)]
  elif not isinstance(old_nodes, list):
      # If it's a single TextNode object, wrap it in a list
      old_nodes = [old_nodes]

  # for every item in the list of nodes (which may only contain one item)
  for old_node in old_nodes:
    # if the text type is anothing other than TEXT, just add it to the final list as is
    if old_node.text_type != TextType.TEXT:
      new_nodes.append(old_node)
      continue
    # if the text type is TEXT - therefore it can contain other types - the node is split
    # we need another empty list to hold the results of nodes that need splitting
    split_nodes = []
    # take the text of the list item we're working on (line 27) and split it with the input delimiter into a list of text strings
    sections = old_node.text.split(delimiter)
    # there should only be matched pairs of delimiters, meaning the smallest number of sections will be 3 and will go up by 2s
    if len(sections) % 2 == 0:
      raise ValueError("invalid markdown, formatted section not closed")
    # considering the number of sections we have, which can vary, look at each section
    for i in range(len(sections)):
      # if the section is an empty string, continue
      if sections[i] == "":
        continue
      # for the even indices, these will be type TEXT as they are the wrappers for the formatted text
      if i % 2 == 0:
        split_nodes.append(TextNode(sections[i], TextType.TEXT))
      # for the odd indices, these are the ones that should be tagged with the new text type that is input in the function
      else:
        split_nodes.append(TextNode(sections[i], new_text_type))
    # take the list of nodes that we have made from our old_node list item and add all the items to the final list
    new_nodes.extend(split_nodes)
  # return the final list
  return new_nodes

def extract_markdown_images(text):
  pattern = r"!\[(.*?)\]\((.*?)\)"
  extracted_images = re.findall(pattern, text)
  return extracted_images

def extract_markdown_links(text):
  pattern = r"\[(.*?)\]\((.*?)\)"
  extracted_links = re.findall(pattern, text)
  return extracted_links
 
def split_nodes_image(old_nodes,):
  new_nodes = []
  for node in old_nodes:
    if len(extract_markdown_images(node.text)) > 0:
      image_tuple = extract_markdown_images(node.text)[0]
      alt_text, url = image_tuple
      sections = node.text.split(f"![{alt_text}]({url})", 1)

      if sections[0]:
        new_nodes.append(TextNode(sections[0], TextType.TEXT))
      new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

      if sections[1]:
        remaining_nodes = split_nodes_image([TextNode(sections[1], TextType.TEXT)])
        new_nodes.extend(remaining_nodes)
    else:
      new_nodes.append(node)
  return new_nodes
      
def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if len(extract_markdown_links(node.text)) > 0:
      link_tuple = extract_markdown_links(node.text)[0]
      link_text, url = link_tuple
      sections = node.text.split(f"[{link_text}]({url})", 1)

      if sections[0]:
        new_nodes.append(TextNode(sections[0], TextType.TEXT))
      new_nodes.append(TextNode(link_text, TextType.LINK, url))

      if sections[1]:
        remaining_nodes = split_nodes_link([TextNode(sections[1], TextType.TEXT)])
        new_nodes.extend(remaining_nodes)
    else:
      new_nodes.append(node)
  return new_nodes

def text_to_textnodes(text):
  nodes = [TextNode(text, TextType.TEXT)]
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
  nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
  nodes = split_nodes_image(nodes)
  nodes = split_nodes_link(nodes)
  return nodes

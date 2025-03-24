from textnode import TextNode, TextType

print("hello world")
def main():
  dummy_node = TextNode("text go here", TextType.LINK, "url go here")
  print(dummy_node)

main()
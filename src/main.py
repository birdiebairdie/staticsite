import os
import shutil

def copy_static_files(source, destination):
  if os.path.exists(destination):
    shutil.rmtree(destination)

  os.mkdir(destination)

  items = os.listdir(source)

  for item in items:
    source_item = os.path.join(source, item)
    destination_item = os.path.join(destination, item)

    if os.path.isfile(source_item):
      shutil.copy(source_item, destination_item)
      print(f"Copied file: {source_item} to {destination_item}")
    else:
      os.mkdir(destination_item)
      print(f"Created directory: {destination_item}")
      copy_static_files(source_item, destination_item)

def main():
  copy_static_files('static', 'public')

if __name__ == "__main__":
  main()
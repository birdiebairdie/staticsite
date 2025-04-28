import os
import shutil

def copy_static_files_recursive(source, destination):
  if not os.path.exists(destination):
    os.mkdir(destination)
    print(f"Created directory: {destination}")

  filenames = os.listdir(source)

  for filename in filenames:
    from_path = os.path.join(source, filename)
    dest_path = os.path.join(destination, filename)
    print(f"Copied file: {from_path} to {dest_path}")
    
    if os.path.isfile(from_path):
      shutil.copy(from_path, dest_path)
    else:
      copy_static_files_recursive(from_path, dest_path)
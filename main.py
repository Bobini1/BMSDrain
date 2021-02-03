import os
import glob


def main():
    lib_dir = input("Enter the directory you want to drain: ")
    drain_dir = input("Enter the directory you want to drain: ")
    library = [{"file": file, "size": os.path.getsize(file)} for file in
               glob.glob(lib_dir + '/*/*/*.[bp]m[sel]') if
               not file.lower().endswith(('.pme', '.pml'))]
    drain = [{"file": file, "size": os.path.getsize(file)} for file in
             glob.glob(lib_dir + '/*/*.[bp]m[sel]') if
             not file.lower().endswith(('.pme', '.pml'))]
    print(library)

if __name__ == "__main__":
    main()

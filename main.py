import os
import glob
import filecmp
import shutil
import distutils
import distutils.dir_util
import distutils.errors
import stat
# Fix long path access:
import ntpath
ntpath.realpath = ntpath.abspath
# Fix long path access.


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def main():
    lib_dir = input("Enter your library folder: ")
    drain_dir = input("Enter the directory you want to drain: ")
    drain = {}
    for file in glob.glob(drain_dir + '/*/*.[bp]m[sel]'):
        if not file.lower().endswith(('.pme', '.pml')):
            size = os.path.getsize(file)
            if size not in drain:
                drain[size] = {file}
            else:
                drain[size].add(file)
    library = {}
    for file in glob.glob(lib_dir + '/*/*/*.[bp]m[sel]'):
        if not file.lower().endswith(('.pme', '.pml')):
            size = os.path.getsize(file)
            if size not in library:
                library[size] = {file}
            else:
                library[size].add(file)
    size_matched = {size for size in drain if size in library}
    for size in size_matched:
        for drain_file in drain[size]:
            for lib_file in library[size]:
                if os.path.exists(drain_file) and os.path.exists(lib_file):
                    if filecmp.cmp(drain_file, lib_file) is True:
                        print(drain_file, lib_file)
                        destination = os.path.dirname(lib_file)
                        destination_files = os.listdir(os.path.dirname(lib_file))
                        origin_dir = os.path.dirname(drain_file)
                        for file in os.listdir(origin_dir):
                            if file not in destination_files:
                                if os.path.isfile(os.path.join(origin_dir, file)):
                                    shutil.copy2(os.path.join(origin_dir, file), destination)
                                else:
                                    distutils.dir_util.copy_tree(os.path.join(origin_dir, file), destination)
                        shutil.rmtree(os.path.dirname(drain_file), onerror=remove_readonly)
                        break


if __name__ == "__main__":
    main()

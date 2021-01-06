import os
import inspect
import zipfile


def current_function_name(depth=1):
    return inspect.getouterframes(inspect.currentframe())[depth].function


def make_zip_archive(src_path, dst_path):
    with zipfile.ZipFile(dst_path, 'w') as archive:
        for (dirPath, _, filenames) in os.walk(src_path):
            for name in filenames:
                path = os.path.join(dirPath, name)
                archive.write(path, os.path.relpath(path, src_path))

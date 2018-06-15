import os
import shutil
import time

# DIRECTORY_PATH = r"F:\Projects\django2exe-dist\django2exe-dist\phone_zilla"
DIRECTORY_PATH = r"F:\Projects\phone_zilla"

# generate pyc files
# os.popen("python -m compileall -f {}".format(DIRECTORY_PATH))

# time.sleep(5)
# place pyc file in structured format
for root, directory, file in os.walk(DIRECTORY_PATH):
    if "__pycache__" in directory:
        cache_dir = os.path.join(root, "__pycache__")
        for pyc in os.listdir(cache_dir):
            src = os.path.join(cache_dir, pyc)
            try:
                new_name = '.'.join(pyc.split('.')[:-2]) + os.path.splitext(pyc)[-1]
            except:
                print(pyc, src)
            print(pyc, new_name)
            dest = os.path.join(root, new_name)
            print("Copying... {} to {}".format(src, dest))
            if os.path.exists(dest):
                os.remove(dest)
            shutil.copy2(src, dest)

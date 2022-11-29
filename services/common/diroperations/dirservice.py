import os
import shutil
from definitions import ROOT_DIR


TMP_RELATIVE_STEP_FILE_PATH = "/tmp/stl/"

"""
Switch to current tmp folder and return the path
"""


def switch_to_path(path=TMP_RELATIVE_STEP_FILE_PATH):
    root_path = ROOT_DIR
    print("CURRENT DIRECTORY ------------" + root_path)
    print("CHOSEN PATH ------------------" + path)
    try:
        os.chdir(root_path + path)
    except FileNotFoundError as fne:
        print ("Error: %s - %s." % (fne.filename, fne.strerror))
    finally:
        return os.getcwd()


def remove_user_directory(path):
    print("DIR TO BE DELETED: -----------------" + path)
    os.chdir(ROOT_DIR)
    try:
        shutil.rmtree(path)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))


def create_user_directory(user_code="uknownuser"):
    temporary_path = switch_to_path()
    new_path = temporary_path + "/" + user_code    
    if not os.path.exists(new_path):
        try:
            os.makedirs(new_path)
            print("NEW MADE DIRECTORY" + new_path)
            os.chdir(new_path)
            return os.getcwd()
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
    else:
        os.chdir(new_path)
        print(new_path)
        return new_path

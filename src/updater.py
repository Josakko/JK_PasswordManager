from utils import parse_version, VERSION, GITHUB_RELEASE_API
import requests
from tkinter import messagebox
import webbrowser
import os
import sys
import subprocess


def get_latest_version():
    try: 
        res = requests.get(GITHUB_RELEASE_API)
    except Exception as e: 
        return None

    if res.status_code == 200:
        return res.json()


def needs_update(current, new):
    if new[0] < current[0]:
        return False
    elif new[0] > current[0]:
        return True
    else:
        if new[1] < current[1]:
            return False
        elif new[1] > current[1]:
            return True
        else:
            if new[2] < current[2]:
                return False
            elif new[2] > current[2]:
                return True
            else:
                if new[3] == current[3]:
                    return False
                elif new[3] == "Release" and current[3] == "Beta":
                    return True
                else:
                    return False


def check_update(release):
    if not release:
        return False

    new_version = parse_version(release["tag_name"])
    current_version = parse_version(VERSION)

    return needs_update(current_version, new_version)


def download_files(release):
    curr_file = os.path.abspath(__file__)
    to_get = ""
    if curr_file.endswith(".exe"):
        to_get = "win"
    else: 
        to_get = "linux"

    url = ""
    filename = ""
    for asset in release["assets"]:
        if "executable" in asset["name"] and to_get in asset["name"]:
            url = asset["browser_download_url"]
            filename = asset["name"]
            break

    if url == "" or filename == "":
        return False

    download_filepath = os.path.join(os.path.dirname(curr_file), filename)
    try:
        fb = requests.get(url).content
    except:
        return False

    open(download_filepath, "wb").write(fb)

    return run_update(download_filepath, curr_file)


def run_update(update_filename, current_filename):
    cmd = [update_filename, "--do-update", update_filename, current_filename] + sys.argv

    if sys.platform == "win32":
        try:
            subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except: return False
        # subprocess.CREATE_NO_WINDOW, subprocess.DETACHED_PROCESS, subprocess.CREATE_NEW_PROCESS_GROUP
    
    # elif sys.platform == "linux" or sys.platform == "linux2":
    else:
        try:
            subprocess.Popen(cmd, start_new_session=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except: return False

    sys.exit(0)


def update(disable_update):
    release = get_latest_version()
    if not check_update(release):
        return


    if disable_update:
        ret = messagebox.askyesno("Update", f"There is an update available, do you want to update now?\n Your current version is {VERSION} and the latest one is {release['tag_name']}.")
        if not ret:
            return

        webbrowser.open(release["html_url"])        
        return

    if "--updated" in sys.argv or not download_files(release):
        ret = messagebox.askyesno("Update", f"There is an update available however auto update has failed! Do you want to update now manually?\n Your current version is {VERSION} and the latest one is {release['tag_name']}.")
        if not ret:
            return

        webbrowser.open(release["html_url"])


def post_update():
    try: 
        arg_index = sys.argv.index("--updated") + 1
    except: 
        return

    if len(sys.argv) < (arg_index + 1):
        return
        
    to_delete = sys.argv[arg_index]
    if not os.path.isfile(to_delete):
        return
    
    try: 
        os.remove(to_delete)
    except:
        pass
    

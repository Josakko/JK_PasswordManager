from utils import parse_version, VERSION, GITHUB_RELEASE_API
import requests
from tkinter import messagebox
import webbrowser


def get_latest_version():
    try: 
        res = requests.get(GITHUB_RELEASE_API)
    except Exception as e: 
        return None

    if res.status_code == 200:
        return res.json()


def needs_update(current, new):
    if new[0] <= current[0]:
        if new[1] <= current[1]:        
            if new[2] <= current[2]:
                if new[3] == current[3]:
                    if new[3] == "Release" and current[3] == "Beta":
                        return True
                    else:
                        return False
                else:
                    return True
        else:
            return True
    else: 
        return True


def check_update(release):
    if not release:
        return False

    new_version = parse_version(release["tag_name"])
    current_version = parse_version(VERSION)

    return needs_update(current_version, new_version)


def update():
    release = get_latest_version()
    if not check_update(release):
        return
    
    # should be temporary only
    ret = messagebox.askyesno("Update", f"There is an update available, do you want to update now?\n Your current version is {VERSION} and the latest one is {release['tag_name']}.")
    if not ret:
        return
    
    webbrowser.open(release["html_url"])


import os
import sys
import utils
import subprocess


def main(argv):
    temp_update_filename = argv[2]
    to_update_filename = argv[3]
    other_args = argv[4:]

    if not os.path.isfile(temp_update_filename):
        launch(to_update_filename, temp_update_filename, other_args)
        sys.exit(0)

    utils.copyfile(temp_update_filename, to_update_filename)
    
    # os.access()

    launch(to_update_filename, temp_update_filename, other_args)
    sys.exit(0)
    

def launch(to_run, to_delete, other_args):
    cmd = [to_run, "--updated", to_delete] + other_args
    subprocess.Popen(cmd, start_new_session=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


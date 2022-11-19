import logging
from os import path, chdir, getcwd
from pathlib import Path
from shutil import rmtree
import tkinter as tk

from general import get_current_game_ver
from mods import mc_cc

# TODO put in config file, vars are used in two files
DOWNLOAD_PATH = f"./tmp" 
SAVED_PATH = f"./sav"


def set_up_cwd():
    # set absolute path to file
    abspath = path.abspath(__file__)
    dname = path.dirname(abspath)
    chdir(dname)
    logging.debug(f"Current dir has been changed: {getcwd()}")


def set_up_logging():
    # set up logging system
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    log_format = "%(asctime)s | %(levelname)s: %(message)s"
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)
    logger.debug("Logging has been set up")


def init():
    set_up_logging()
    set_up_cwd()

    for path in (SAVED_PATH, DOWNLOAD_PATH):
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)


def del_tmp():
    tmp_folder = Path(DOWNLOAD_PATH)
    if tmp_folder.exists():
        rmtree(tmp_folder)


def main():
    init()
    window = tk.Tk()
    game_version = get_current_game_ver()

    try:
        mc_cc.run(game_version)
    except Exception as e:
        error_message = tk.Label(
            text=str(e),
            fg="white",
            bg="black",
            width=140,
            height=40
        )
        error_message.pack()
        window.mainloop()

    del_tmp()


if __name__ == "__main__":
    main()

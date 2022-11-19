from datetime import datetime
import logging
import os
import pathlib
import shutil
from urllib import request
from zipfile import ZipFile


GAME_DOC_DIR = fr"{pathlib.Path.home()}\Documents\Electronic Arts\The Sims 4"
GAME_VER_FILE_NAME = "GameVersion.txt"
DOWNLOAD_PATH = f"./tmp"
SAVED_PATH = f"./sav"

# set up requests
opener = request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
request.install_opener(opener)


def get_file_name_from_url(file_url):
    print("opening url", file_url)
    rq = request.urlopen(file_url)
    print("trying to get the basename")
    return os.path.basename(rq.url)


def download_extract_files(file_url, file_name=None):
    """
    This downloads a file given an endpoint, unzips it.
    returns path of new downloaded mod

    - download the files to tmp
    - extract them in tmp
    :return: new unzipped mod directory
    """
    if not file_name:
        file_name = get_file_name_from_url(file_url)

    print("downloading mod")
    download_new_mod_path = download_mod(file_url, file_name)
    print("done")
    return unzip_file(download_new_mod_path, file_name)


def download_mod(file_url, file_name):
    """
    Downloads a mod given an end point in programs tmp file
    returns the path of the new downloaded file

    :param file_url: endpoint to download the new mod from
    :param file_name: what to name the file to.
    :return: the path where the new mod was downloaded to.
    """
    if not file_name:
        file_name = get_file_name_from_url(file_url)

    logging.info(f"Downloading the file with the basename f{file_name}")

    download_new_mod_path = pathlib.Path(f"{DOWNLOAD_PATH}/{file_name}")
    logging.debug(
        f"Starting download for file {file_url}. DL it to {download_new_mod_path}")

    # request.urlretrieve(file_url, f"{os.path.basename(resp.url)}")

    request.urlretrieve(file_url, download_new_mod_path)
    logging.info(f"Finished downloading {file_url}")
    return download_new_mod_path


def unzip_file(zipped_file, file_name):
    logging.info(f"Attempting to unpack/unzip {zipped_file=}")
    new_mod_dir = None
    # loading the temp.zip and creating a zip object
    with ZipFile(zipped_file, 'r') as zObject:
        base_file_name = file_name.split(".")
        if len(base_file_name) > 2:
            base_file_name = ".".join(base_file_name[:-1])
        else:
            base_file_name = base_file_name[0]
        # Extracting all the members of the zip
        # into a specific location.
        new_mod_dir = pathlib.Path(f"{DOWNLOAD_PATH}/{base_file_name}")

        # create directory
        if not os.path.exists(new_mod_dir):
            os.makedirs(new_mod_dir)

        # extract the zipped mod in to the new directory that we made
        zObject.extractall(path=new_mod_dir)

    logging.info(
        f"created a new mod dir, with the extracted mod {new_mod_dir=}")

    return new_mod_dir


def find_original_mod_file(mod_base_name):
    file = pathlib.Path(f"{GAME_DOC_DIR}")
    file = file / "Mods"
    logging.info(
        f"Starting:[{mod_base_name}] trying to find mod file in [{file}]")

    want_file = file.rglob(mod_base_name)

    try:
        want_file = want_file.__next__()
    except Exception as e:
        raise FileNotFoundError(
            f"The wanted mod file was not found for {mod_base_name}...")

    return want_file


def copy_mod_file(og_mod_file):
    """
    TODO create a new dir for every script run, rather than create loose files

    :param: mod_base_name REGEX used for finding the mod dir
            we want to replace in original mod folder
    :return: the destination of the saved mod in sav folder
    """

    logging.info(f"Starting: copying original mod to our sav dir")

    # copy folder contents to saved.
    logging.debug("copying file to new dir")
    dst_dir = pathlib.Path(
        f"{SAVED_PATH}/{og_mod_file.name}_SAVED_{datetime.today():%Y_%m_%d-%H_%M}")
    shutil.copytree(og_mod_file, dst_dir)
    logging.info(f"Successfully copied original old mod to sav dir")

    return dst_dir


def replace_mod_file(og_mod_file, new_mod):
    """replaces the new downloaded mod with old mod (in game folder)"""
    logging.debug(f"Starting: coping {new_mod} into our original mod file.")
    file = pathlib.Path(f"{GAME_DOC_DIR}/Mods")

    # we want to delete that file and insert a new file
    del_old_mod_file = pathlib.Path(og_mod_file)
    if del_old_mod_file.exists():
        shutil.rmtree(del_old_mod_file)

    dst_dir = pathlib.Path(f"{file}/{new_mod.name}")
    print(f"{dst_dir=} {dst_dir.absolute()}")
    shutil.copytree(new_mod, dst_dir)


def add_mod_file():
    pass


def copy_files_to(src_dir, trg_dir, files):
    """
    Copies a list of files over to trg_dir

    :param src_dir: settings to copy FROM
    :param trg_dir: settings to copy TO
    :param files:   what files should we copy over to.
    :return:
    """

    if isinstance(files, str):
        files = [files]

    for file in files:
        # go through all the files you are trying to copy and put it in the scr dest

        src_file = src_dir
        try:
            # try to get the file from the source destination
            src_file = pathlib.Path(src_dir) / f"{file}"
            if not src_file.exists():
                raise FileNotFoundError()

            shutil.copy2(src_file, trg_dir)
            logging.debug(
                f"file {file} was successfully copied from {src_dir} to {trg_dir}!")
        except Exception as e:
            logging.error(f"The file we tried to copy over, {file} DNE! {e}")


def get_current_game_ver():
    q = pathlib.Path(GAME_DOC_DIR)
    w = pathlib.Path(q / GAME_VER_FILE_NAME)
    logging.debug(f"Grabbing game version from {w}")
    with open(w, "r+") as game_ver:
        exp_str = game_ver.readlines()[1]
        # expected ['\n', '\x00\x00\x00<GAME_VERSION>']
        logging.debug(f"Game version retrieved: {exp_str[3:]}")
        return exp_str[3:]

"""
Deletes The Sims 4's cache files.

Cleaning up cache files help performance and fix unknown problems.

It is advised to run this script when:
- There is a new patch
- New cc is installed
- CC is removed
- The game acts buggy

This process follows the recommended steps in
[this post](https://www.carls-sims-4-guide.com/help/cache.php)
"""

from general import GAME_DOC_DIR
from itertools import chain
from pathlib import Path
from shutil import rmtree


def run(method: str = ""):
    """This methods clears TS4 cache

    There are different recommended ways of clearing the cache dir.
    To choose how you would like to clear the cache, pass through

    - all
    - except_cfg
    - default

    If the argument passed through doesn't match the above, the default
    means of clearing cache will follow.
    """
    clean_cache(method)


def clean_cache(cache_del_method="default"):
    """Deletes cached files in sims4 game dir for better game play

    deletes files:
    - localthumbcache.package (the article adds an s)
    - cachewebkit

    delete dirs:
    - onlinethumbnailcache
    - lotcachedata

    cleans dir:
    - cachestr
    - cache (cleans files based on what is selected)
        - [.cache, .jpg, .dat] extensions.
        - all files
        - all files except FileCache.cfg
    """
    # get all constant dir and files to delete
    del_files = chain((
        Path(GAME_DOC_DIR) / "localthumbcache.package",
        Path(GAME_DOC_DIR) / "cachewebkit",
        *(Path(GAME_DOC_DIR) / "cachestr").iterdir())
    )
    dir = [
        Path(GAME_DOC_DIR) / "onlinethumbnailcache",
        Path(GAME_DOC_DIR) / "lotcachedata",
    ]

    # get the files in cache dir to delete (based on arg passed through)
    cache_path = Path(GAME_DOC_DIR) / "cache"
    if cache_del_method == "all":
        del_files = chain(del_files, cache_path.glob("*"))
    elif cache_del_method == "except_cfg":
        del_files = chain(del_files, [
            file for file in cache_path.glob("*")
            if file.name != "FileCache.cfg"])
    else:
        # safest
        del_files = chain(del_files, *map(cache_path.glob,
                          ("*.cache", "*.jpg", "*.dat")))

    # delete
    for f in del_files:
        print(f"Attempting to delete: {f.name}", end=" ")
        if f.exists():
            print("[DELETED]")
            f.unlink()
        else:
            print("[NOT FOUND]")

    for d in dir:
        print(f"Attempting to delete: {d.name}", end=" ")
        if d.exists():
            print("[DELETED]")
            rmtree(d)
        else:
            print("[NOT FOUND]")

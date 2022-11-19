"""
Deletes The Sims 4's cache files.

Cleaning up the cache files help performance and fix unknown problems.

It is advised to run this whenever:
- there is a new patch
- new cc is installed
- cc is removed
- your game acts buggy

This process follows the recommended steps in
[this post](https://www.carls-sims-4-guide.com/help/cache.php)
"""

from general import GAME_DOC_DIR
from itertools import chain
from pathlib import Path
from shutil import rmtree


def run():
    """Deletes cached files in sims4 game dir for better game play

    deletes files:
    - localthumbcache.package (the article adds an s)
    - cachewebkit

    delete dirs:
    - onlinethumbnailcache
    - lotcachedata

    cleans dir:
    - cachestr
    - cache (cleans files with [.cache, .jpg, .dat] exts.)
    """
    files = chain((
        Path(GAME_DOC_DIR) / "localthumbcache.package",
        Path(GAME_DOC_DIR) / "cachewebkit",
        *(Path(GAME_DOC_DIR) / "cachestr").iterdir()),
        *map((Path(GAME_DOC_DIR) / "cache").glob, ("*.cache", "*.jpg", "*.dat")))

    dir = [
        Path(GAME_DOC_DIR) / "onlinethumbnailcache",
        Path(GAME_DOC_DIR) / "lotcachedata",
    ]

    for f in files:
        print(f)
        if f.exists():
            print("deleting...")
            f.unlink()
        else:
            print("could not delete", f)

    for d in dir:
        print(d)
        if d.exists():
            rmtree(d)


def expanded_run():
    """Follows step by step the instructions from link to clear cache"""
    # 1. Delete the localthumbscache.package
    local_thumbs_cache = Path(GAME_DOC_DIR) / "localthumbcache.package"
    if local_thumbs_cache.exists():
        local_thumbs_cache.unlink()

    # 2. Go inside the cache folder and delete all files w/ ext (cache|jpg|dat)
    cache_dir = Path(GAME_DOC_DIR) / "cache"
    # cache_files = cache_dir.glob("*.@(cache|jpg|dat)")  # :/
    file_ext = ("*.cache", "*.jpg", "*.dat")
    for file in chain(*map(cache_dir.glob, file_ext)):
        file.unlink()

    # 3. Delete all files in cachestr
    cache_str = Path(GAME_DOC_DIR) / "cachestr"
    for file in cache_str.iterdir():
        file.unlink()

    # 4. del onlinethumbnailcache folder
    online_thumbnail_cache = Path(GAME_DOC_DIR) / "onlinethumbnailcache"
    if online_thumbnail_cache.exists():
        rmtree(online_thumbnail_cache)

    # delete  cachewebkit file and lotcachedata dir
    cache_web_kit = Path(GAME_DOC_DIR) / "cachewebkit"
    if cache_web_kit.exists():
        cache_web_kit.unlink()

    lot_cache_data = Path(GAME_DOC_DIR) / "lotcachedata"
    if lot_cache_data.exists():
        rmtree(lot_cache_data)
        print("lot_cache_data has been deleted")

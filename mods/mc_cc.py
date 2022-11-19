from bs4 import BeautifulSoup
from urllib import request
import general
import os
from browser_user import BrowserUser
import re
from collections import namedtuple

MC_CC_URL = "https://deaderpool-mccc.com/#/releases"


def run(game_version):
    bu = BrowserUser()
    page_source = bu.grab_page_source(MC_CC_URL)
    mc_url, mc_wh_url = grab_dl_links(game_version, page_source)
    print(f"{mc_url=}")
    print(f"{mc_wh_url=}")
    mod_template = namedtuple("Mod", ["url", "glob", "files"])
    mods = [
        mod_template(mc_url, "*McCmdCenter_AllModules*", "mc_settings.cfg"),
        mod_template(mc_wh_url, "*MCWoohoo*", None)
    ]

    for mod in mods:
        r = request.urlopen(mod.url)
        working_mod_dir = general.download_extract_files(
            mod.url,
            os.path.basename(r.url)
        )
        og_mod_file = general.find_original_mod_file(mod.glob)
        copy_mod_dir = general.copy_mod_file(og_mod_file)

        # save user settings
        if mod.files:
            general.copy_files_to(
                copy_mod_dir,
                working_mod_dir,
                mod.files
            )

        print(f"{copy_mod_dir=}, {working_mod_dir=}")
        general.replace_mod_file(og_mod_file, working_mod_dir)
    bu.close_driver()
    pass


def grab_dl_links(game_version, page_resource=None):
    """Grabs mod's download links associated with game version.

    This function grabs associated download links for for the given game version in the given page resource

    returns (Mc_CC)

    """
    soup = BeautifulSoup(page_resource, 'html.parser')
    rows = soup.select('tbody.site-body table.table-grid tr')

    found_mod = False
    mc_cc_url = None

    for row in rows:
        # Each row is expected to have 3 tds
        # 0 td, is `Release`` (download link w/ mod name.ver)
        # 1 td, compatibility (this contains the game patch ver associate)
        # 2 td, change logs (no import info, ignore)

        data = row.find_all('td')

        if game_version in data[1].text:
            found_mod = True
            mc_cc_url = data[0].a['href']
        elif found_mod:
            # Note: the add on mod will always follow the main mod
            # TODO configure, if user does not want the add-on mod, then reject.
            return mc_cc_url, data[0].a['href']

    # ! should only be reached if we could not find a suited mod for the game version
    data = rows[1].find_all('td')
    pattern = r"\d{1}\.\d{2}\.\d{2,3}\.\d{4}"
    pc_ver, mac_ver, *_ = re.findall(pattern, data[1].text)

    print(f"{pc_ver=}")
    print(f"{mac_ver=}")

    if game_version > pc_ver and game_version > mac_ver:
        # mod is not up to date with game
        raise Exception(
            """
            GAME VERSION IS NOT SUPPORTED BY Mccc. 
            This mod is not up-to-date with the newest S4 patch. 
            Please give the modder time to update the files.
            Thank you :).
            """
        )
    else:
        # game patch is not supported by mod (game is too old)
        raise Exception(
            """
            GAME VERSION IS NOT SUPPORTED. 
            MCCC chooses not to support game patches older than a specific patch.
            Please update your game. 
            If you've already updated it, launch your game before running this script.
            """
        )


if __name__ == "__main__":
    run()

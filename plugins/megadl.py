
"""
✘ Commands Available -

•`{i}megadl <link>`
  It Downloads and Upload Files from mega.nz links.
"""

import glob
import time
from datetime import datetime

from . import *


@ultroid_cmd(pattern="megadl ?(.*)")
async def _(e):
    link = e.pattern_match.group(1)
    if os.path.isdir("mega"):
        os.system("rm -rf mega")
    os.mkdir("mega")
    xx = await eor(e, f"Processing...\nTo Check Progress : `{HNDLR}ls mega`")
    s = datetime.now()
    x, y = await bash(f"megadl {link} --path mega")
    afl = glob.glob("mega/*")
    ok = [*sorted(afl)]
    tt = time.time()
    k = []
    for x in ok:
        if os.path.isdir(x):
            k.append(x)
            break
    if k:
        await xx.edit(
            "Your Unzipped File Saved in `mega` folder.\nDo `{i}ls mega` and browse storage\nUse `{i}ul <path>` To upload.".format(
                i=HNDLR
            )
        )
    else:
        c = 0
        for kk in ok:
            try:
                res = await uploader(kk, kk, tt, xx, "Uploading...")
                await ultroid_bot.send_file(
                    e.chat_id,
                    res,
                    caption="`" + kk.split("/")[-1] + "`",
                    force_document=True,
                    thumb="resources/extras/ultroid.jpg",
                )
                c += 1
            except Exception as er:
                LOGS.info(er)
        ee = datetime.now()
        t = time_formatter(((ee - s).seconds) * 1000)
        size = 0
        for path, dirs, files in os.walk("mega"):
            for f in files:
                fp = os.path.join(path, f)
                size += os.path.getsize(fp)
        await xx.delete()
        await ultroid_bot.send_message(
            e.chat_id,
            f"Downloaded And Uploaded Total - `{c}` files of `{humanbytes(size)}` in `{t}`",
        )
        os.system("rm -rf mega")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})

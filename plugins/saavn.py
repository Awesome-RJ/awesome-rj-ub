
"""
✘ Commands Available -

• `{i}saavn <search query>`
    Download songs from Saavn

"""

import os
import time
from urllib.request import urlretrieve

import requests as r
from telethon.tl.types import DocumentAttributeAudio

from . import *


@ultroid_cmd(pattern="saavn ?(.*)")
async def siesace(e):
    song = e.pattern_match.group(1)
    if not song:
        return await eod(e, "`Give me Something to Search")
    hmm = time.time()
    lol = await eor(e, "`Searching on Saavn...`")
    sung = song.replace(" ", "%20")
    url = f"https://jostapi.herokuapp.com/saavn?query={sung}"
    try:
        k = (r.get(url)).json()[0]
    except IndexError:
        return await eod(lol, "`Song Not Found.. `")
    title = k["song"]
    urrl = k["media_url"]
    img = k["image"]
    duration = k["duration"]
    singers = k["singers"]
    urlretrieve(urrl, f'{title}.mp3')
    urlretrieve(img, f'{title}.jpg')
    okk = await uploader(
        f'{title}.mp3', f'{title}.mp3', hmm, lol, f"Uploading {title}..."
    )

    await ultroid_bot.send_file(
        e.chat_id,
        okk,
        caption=f"`{title}`" + "\n`From Saavn`",
        attributes=[
            DocumentAttributeAudio(
                duration=int(duration),
                title=title,
                performer=singers,
            )
        ],
        supports_streaming=True,
        thumb=f'{title}.jpg',
    )

    await lol.delete()
    os.remove(f'{title}.mp3')
    os.remove(f'{title}.jpg')


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})

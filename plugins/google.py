
"""
✘ Commands Available -

• `{i}google <query>`
    For doing google search.

• `{i}img <query>`
  `{i}img <query> ; <no of results>`
    For doing Images search.

• `{i}reverse <query>`
    Reply an Image or sticker to find its sauce.
"""

import os
from shutil import rmtree

import requests
from bs4 import BeautifulSoup as bs
from PIL import Image
from search_engine_parser import GoogleSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError as GoglError

from strings import get_string

from . import *


@ultroid_cmd(pattern="google ?(.*)")
async def google(event):
    inp = event.pattern_match.group(1)
    if not inp:
        return await event.edit("`Give something to search..`")
    x = await eor(event, get_string("com_2"))
    gs = GoogleSearch()
    try:
        res = await gs.async_search(f"{inp}", cache=False)
    except GoglError as e:
        return await eor(event, str(e))
    out = ""
    for i in range(len(res["links"])):
        text = res["titles"][i]
        url = res["links"][i]
        des = res["descriptions"][i]
        out += f" 👉🏻  [{text}]({url})\n`{des}`\n\n"
    omk = f"**Google Search Query:**\n`{inp}`\n\n**Results:**\n{out}"
    opn = []
    for bkl in range(0, len(omk), 4095):
        opn.append(omk[bkl : bkl + 4095])
    for bc in opn:
        await ultroid_bot.send_message(event.chat_id, bc, link_preview=False)
    await x.delete()
    opn.clear()


@ultroid_cmd(pattern="img ?(.*)")
async def goimg(event):
    query = event.pattern_match.group(1)
    if not query:
        return await eor(event, "`Give something to search...`")
    nn = await eor(event, "`Processing Keep Patience...`")
    if ";" in query:
        try:
            lmt = int(query.split(";")[1])
            query = query.split(";")[0]
        except BaseExceptaion:
            lmt = 5
    else:
        lmt = 5
    gi = googleimagesdownload()
    args = {
        "keywords": query,
        "limit": lmt,
        "format": "jpg",
        "output_directory": "./resources/downloads/",
    }
    pth = gi.download(args)
    ok = pth[0][query]
    await event.client.send_file(event.chat_id, ok, caption=query, album=True)
    rmtree(f"./resources/downloads/{query}/")
    await nn.delete()


@ultroid_cmd(pattern="reverse")
async def reverse(event):
    reply = await event.get_reply_message()
    if not reply:
        return await eor(event, "`Reply to an Image`")
    ult = await eor(event, "`Processing...`")
    dl = await bot.download_media(reply)
    img = Image.open(dl)
    x, y = img.size
    file = {"encoded_image": (dl, open(dl, "rb"))}
    grs = requests.post(
        "https://www.google.com/searchbyimage/upload",
        files=file,
        allow_redirects=False,
    )
    loc = grs.headers.get("Location")
    response = requests.get(
        loc,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
        },
    )
    xx = bs(response.text, "html.parser")
    div = xx.find_all("div", {"class": "r5a77d"})[0]
    alls = div.find("a")
    link = alls["href"]
    text = alls.text
    await ult.edit(f"`Dimension ~ {x} : {y}`\nSauce ~ [{text}](google.com{link})")
    gi = googleimagesdownload()
    args = {
        "keywords": text,
        "limit": 2,
        "format": "jpg",
        "output_directory": "./resources/downloads/",
    }
    pth = gi.download(args)
    ok = pth[0][text]
    await event.client.send_file(
        event.chat_id,
        ok,
        album=True,
        caption="Similar Images Realted to Search",
    )
    rmtree(f"./resources/downloads/{text}/")
    os.remove(dl)


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})

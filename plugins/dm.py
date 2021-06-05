"""
✘ Commands Available -

• `{i}dm <username/id> <reply/type>`
    Direct Message the User.
"""

from . import *


@ultroid_cmd(pattern="dm ?(.*)")
async def dm(e):
    if len(e.text) > 3:
        if not e.text[3] == " ":  # weird fix
            return
    d = e.pattern_match.group(1)
    c = d.split(" ")
    try:
        chat_id = await get_user_id(c[0])
    except Exception as ex:
        return await eod(e, "`" + str(ex) + "`", time=5)
    msg = ""
    masg = await e.get_reply_message()
    if e.reply_to_msg_id:
        await ultroid_bot.send_message(chat_id, masg)
        await eod(e, "`⚜️Message Delivered!`", time=4)
    for i in c[1:]:
        msg += i + " "
    if msg == "":
        return
    try:
        await ultroid_bot.send_message(chat_id, msg)
        await eod(e, "`⚜️Message Delivered!⚜️`", time=4)
    except BaseException:
        await eod(
            e,
            "`{i}help dm`",
            time=4,
        )


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})

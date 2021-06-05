
"""
✘ Commands Available -

• `{i}save <reply message>`
    Save that replied msg to ur saved messages box.

"""
from . import *


@ultroid_cmd(pattern="save$")
async def saf(e):
    x = await e.get_reply_message()
    if not x:
        return await eod(
            e, "Reply to Any Message to save it to ur saved messages", time=5
        )
    MLA = e.sender_id
    if not MLA:
        MLA = ultroid_bot.uid
    await ultroid_bot.send_message(MLA, x)
    await eod(e, "Message saved to Your Pm/Saved Messages.", time=5)


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})

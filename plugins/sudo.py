
"""
✘ Commands Available -

• `{i}addsudo`
    Add Sudo Users by replying to user or using <space> separated userid(s)

• `{i}delsudo`
    Remove Sudo Users by replying to user or using <space> separated userid(s)

• `{i}listsudo`
    List all sudo users.
"""


from pyUltroid.misc._decorators import sed

from . import *


@ultroid_cmd(
    pattern="addsudo ?(.*)",
)
async def _(ult):
    if not ult.out and not is_fullsudo(ult.sender_id):
        return await eod(ult, "`This Command is Sudo Restricted!..`")
    inputs = ult.pattern_match.group(1)
    if BOT_MODE and ult.sender_id != int(Redis(OWNER_ID)):
        return await eod(ult, "`Sudo users can't add new sudos!`", time=10)
    ok = await eor(ult, "`Updating SUDO Users List ...`")
    if ult.reply_to_msg_id:
        replied_to = await ult.get_reply_message()
        id = await get_user_id(replied_to.sender_id)
        name = (await ult.client.get_entity(int(id))).first_name
        sed.append(id)
        mmm = ""
        if id == ultroid_bot.me.id:
            mmm += "You cant add yourself as Sudo User..."
        elif is_sudo(id):
            mmm += f"[{name}](tg://user?id={id}) `is already a SUDO User ...`"
        elif add_sudo(id):
            udB.set("SUDO", "True")
            mmm += f"**Added [{name}](tg://user?id={id}) as SUDO User**"
        else:
            mmm += "`SEEMS LIKE THIS FUNCTION CHOOSE TO BREAK ITSELF`"
        await eod(ok, mmm, time=5)

    if not inputs:
        return await eod(ok, "`Reply to a msg or add it's id/username.`", time=5)
    id = await get_user_id(inputs)
    try:
        name = (await ult.client.get_entity(int(id))).first_name
    except BaseException:
        name = ""
    sed.append(id)
    mmm = ""
    if id == ultroid_bot.me.id:
        mmm += "You cant add yourself as Sudo User..."
    elif is_sudo(id):
        mmm += (
            f"[{name}](tg://user?id={id}) `is already a SUDO User ...`"
            if name
            else f"`{id} is already a SUDO User...`"
        )

    elif add_sudo(id):
        udB.set("SUDO", "True")
        mmm += (
            f"**Added [{name}](tg://user?id={id}) as SUDO User**"
            if name != ""
            else f"**Added **`{id}`** as SUDO User**"
        )

    else:
        mmm += "`SEEMS LIKE THIS FUNCTION CHOOSE TO BREAK ITSELF`"
    await eod(ok, mmm, time=5)


@ultroid_cmd(
    pattern="delsudo ?(.*)",
)
async def _(ult):
    if not ult.out and not is_fullsudo(ult.sender_id):
        return await eod(ult, "`This Command is Sudo Restricted!..`")
    inputs = ult.pattern_match.group(1)
    if BOT_MODE and ult.sender_id != int(Redis(OWNER_ID)):
        return await eod(
            ult,
            "You are sudo user, You cant add other sudo user.",
            time=5,
        )
    ok = await eor(ult, "`Updating SUDO Users List ...`")
    if ult.reply_to_msg_id:
        replied_to = await ult.get_reply_message()
        id = await get_user_id(replied_to.sender_id)
        name = (await ult.client.get_entity(int(id))).first_name
        sed.remove(id)
        mmm = ""
        if not is_sudo(id):
            mmm += f"[{name}](tg://user?id={id}) `wasn't a SUDO User ...`"
        elif del_sudo(id):
            mmm += f"**Removed [{name}](tg://user?id={id}) from SUDO User(s)**"
        else:
            mmm += "`SEEMS LIKE THIS FUNCTION CHOOSE TO BREAK ITSELF`"
        await eod(ok, mmm, time=5)

    if inputs:
        id = await get_user_id(inputs)
        try:
            name = (await ult.client.get_entity(int(id))).first_name
        except BaseException:
            name = ""
        sed.remove(id)
        mmm = ""
        if not is_sudo(id):
            mmm += (
                f"[{name}](tg://user?id={id}) `wasn't a SUDO User ...`"
                if name
                else f"`{id} wasn't a SUDO User...`"
            )

        elif del_sudo(id):
            mmm += (
                f"**Removed [{name}](tg://user?id={id}) from SUDO User(s)**"
                if name
                else f"**Removed **`{id}`** from SUDO User(s)**"
            )

        else:
            mmm += "`SEEMS LIKE THIS FUNCTION CHOOSE TO BREAK ITSELF`"
        await eod(ok, mmm, time=5)


@ultroid_cmd(
    pattern="listsudo$",
)
async def _(ult):
    ok = await eor(ult, "`...`")
    sudos = Redis("SUDOS")
    if sudos == "" or sudos is None:
        return await eod(ult, "`No SUDO User was assigned ...`", time=5)
    sumos = sudos.split(" ")
    msg = ""
    for i in sumos:
        try:
            name = (await ult.client.get_entity(int(i))).first_name
        except BaseException:
            name = ""
        msg += (
            f"• [{name}](tg://user?id={i}) ( `{i}` )\n"
            if name
            else f"• `{i}` -> Invalid User\n"
        )

    m = udB.get("SUDO") or "False"
    if m == "False":
        m = "[False](https://telegra.ph/Awesome-Rj-06-05)"
    return await ok.edit(
        f"**SUDO MODE : {m}\n\nList of SUDO Users :**\n{msg}", link_preview=False
    )


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})

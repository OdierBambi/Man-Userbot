# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot start point """

import asyncio
import sys
from importlib import import_module
from random import randint

from pytgcalls import idle
from telethon.errors.rpcerrorlist import ChannelsTooMuchError, PhoneNumberInvalidError
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditAdminRequest,
    JoinChannelRequest,
)
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import ChatAdminRights

from userbot import ALIVE_NAME, BOT_TOKEN, BOT_VER, BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import LOGS, UPSTREAM_REPO_BRANCH, bot, call_py, tgbot
from userbot.modules import ALL_MODULES
from userbot.modules.sql_helper.globals import addgvar, gvarstatus

INVALID_PH = (
    "\nERROR: Nomor Telepon yang kamu masukkan SALAH."
    "\nTips: Gunakan Kode Negara beserta nomornya atau periksa nomor telepon Anda dan coba lagi."
)

try:
    bot.start()
    call_py.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    sys.exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info(
    f"Jika {ALIVE_NAME} Membutuhkan Bantuan, Silahkan Gabung ke Grup https://t.me/SharingUserbot"
)

LOGS.info(f"Man-Userbot ⚙️ V{BOT_VER} [🔥 BERHASIL DIAKTIFKAN! 🔥]")

def run_in_loop(bot, function):
    return bot.loop.run_until_complete(function)

async def autobot():
    if gvarstatus("BOT_TOKEN"):
        return
    if BOT_TOKEN:
        return addgvar("BOT_TOKEN", BOT_TOKEN)
    await bot.start()
    LOGS.info("MAKING A TELEGRAM BOT FOR YOU AT @BotFather, Kindly Wait")
    who = await bot.get_me()
    name = who.first_name + "'s Assistant Bot"
    if who.username:
        username = who.username + "_bot"
    else:
        username = "manuser_" + (str(who.id))[5:] + "_bot"
    bf = "@BotFather"
    await bot(UnblockRequest(bf))
    await bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await bot.send_message(bf, "/start")
    await asyncio.sleep(1)
    await bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do."):
        LOGS.info(
            "Please make a Bot from @BotFather and add it's token in BOT_TOKEN, as an env var and restart me."
        )
        sys.exit(1)
    await bot.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await bot.send_message(bf, "My Assistant Bot")
        await asyncio.sleep(1)
        isdone = (await bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            LOGS.info(
                "Please make a Bot from @BotFather and add it's token in BOT_TOKEN, as an env var and restart me."
            )
            sys.exit(1)
    await bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    await bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "manuser_" + (str(who.id))[6:] + str(ran) + "_bot"
        await bot.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            addgvar("BOT_TOKEN", f"{token}")
            addgvar("BOT_USERNAME", f"@{username}")
            await bot.send_message(bf, "/setinline")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(bf, "Search")
            LOGS.info(f"DONE YOUR TELEGRAM BOT IS CREATED SUCCESSFULLY @{username}")
        else:
            LOGS.info(
                "Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
            )
            sys.exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        addgvar("BOT_TOKEN", f"{token}")
        addgvar("BOT_USERNAME", f"@{username}")
        await bot.send_message(bf, "/setinline")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bf, "Search")
        LOGS.info(f"DONE YOUR TELEGRAM BOT IS CREATED SUCCESSFULLY @{username}")
    else:
        LOGS.info(
            "Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
        )
        sys.exit(1)


bot.loop.create_task(autobot())


async def autopilot():
    if BOTLOG_CHATID and str(BOTLOG_CHATID).startswith("-100"):
        addgvar("BOTLOG_CHATID", str(BOTLOG_CHATID))
    if gvarstatus("BOTLOG_CHATID"):
        try:
            await bot.get_entity(int(gvarstatus("BOTLOG_CHATID")))
            return
        except BaseException as er:
            LOGS.error(er)
            delgvar("BOTLOG_CHATID")
    LOGS.info("Creating a Log Userbot for You!")
    try:
        r = await bot(
            CreateChannelRequest(
                title="My Userbot Logs",
                about="My Userbot Log Group\n\n Join @SharingUserbot",
                megagroup=True,
            ),
        )
    except ChannelsTooMuchError:
        LOGS.info(
            "You Are in Too Many Channels & Groups , Leave some And Restart The Bot"
        )
        exit(1)
    except BaseException as er:
        LOGS.info(er)
        LOGS.info(
            "Something Went Wrong , Create A Group and set its id on config var BOTLOG_CHATID."
        )
        exit(1)
    chat = r.chats[0]
    chat_id = chat.id
    if not str(chat_id).startswith("-100"):
        addgvar("BOTLOG_CHATID", "-100" + str(chat_id))
    else:
        addgvar("BOTLOG_CHATID", str(chat_id))
    rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        anonymous=False,
        manage_call=True,
    )
    await bot(EditAdminRequest(chat_id, tgbot.me.username, rights, "Assistant"))


bot.run_in_loop(autopilot())


async def man_userbot_on():
    try:
        if BOTLOG_CHATID != 0:
            await bot.send_message(
                BOTLOG_CHATID,
                f"🔥 **Man-Userbot Berhasil Di Aktifkan**\n━━\n➠ **Userbot Version -** `{BOT_VER}@{UPSTREAM_REPO_BRANCH}`\n➠ **Ketik** `{cmd}alive` **untuk Mengecheck Bot**\n━━",
            )
    except Exception as e:
        LOGS.info(str(e))
    # KALO LU NGEFORK LINK CH & GRUP PUNYA GUA NYA JANGAN DI HAPUS YA GOBLOK 😡
    try:
        await bot(JoinChannelRequest("@Lunatic0de"))
        await bot(JoinChannelRequest("@SharingUserbot"))
    except BaseException:
        pass


# JANGAN DI HAPUS GOBLOK 😡 LU COPY/EDIT AJA TINGGAL TAMBAHIN PUNYA LU
# DI HAPUS GUA GBAN YA 🥴 GUA TANDAIN LU AKUN TELENYA 😡
bot.loop.create_task(man_userbot_on())
idle()
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()

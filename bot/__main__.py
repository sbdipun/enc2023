import re
import sys
import time
from datetime import datetime

from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import LOGS, Config, bot, data, list_handler, queue
from bot.database import adduser, napana
from bot.plugins.compress import mediainfo, renew, sysinfo
from bot.plugins.utils import add_task1

from .plugins.devtools import eval_message_f, exec_message_f
from .plugins.extras import (changeffmpeg, changemode, download_dir,
                             get_ffmpeg, get_type, sample, upload_dir, vshots)

START_TIME = datetime.now()


@bot.on_message(filters.incoming & filters.command(["start"]))
async def start_command(bot, message):
    await adduser(message)
    first_name = message.from_user.mention()
    uptime_str = str(datetime.now() - START_TIME).split(".")[0]
    txt = f"👋 Hi **{first_name}**, Welcome to **SvtAv1Enc**!\n\n__This is a very powerful Telegram bot.\nYou can encode video with the desired FFmpeg settings; Keeps coding even after reboot due to database.__\n\n❖ Bot Uptime: **{uptime_str}**"
    await bot.send_message(
        chat_id=message.chat.id,
        text=txt,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("DEV", url="t.me/SamXD7")]]),
        reply_to_message_id=message.id,
    )


@bot.on_message(filters.incoming & (filters.video | filters.document))
async def media_command(bot, message):
    if message.chat.id not in (Config.AUTH_USERS + Config.ADMIN +
                               Config.OWNER):
        return
    query = await message.reply_text("⏳ **Added To QUEUE.**", quote=True)
    queue.insert_one({"message": str(message)})
    await napana()
    if len(data) == 1:
        await query.delete()
        await add_task1(data[0])


@bot.on_message(filters.incoming & filters.command(["set"]))
async def set_command(bot, message):
    if message.chat.id not in (Config.AUTH_USERS + Config.ADMIN +
                               Config.OWNER):
        return await message.reply_text(
            "🚫 **You Are Not Authorized To Use This Bot. Contact: [Sam! X](https://t.me/SamXD7)**",
            disable_web_page_preview=True,
            quote=True,
        )
    await changeffmpeg(bot, message)


@bot.on_message(filters.incoming & filters.command(["uptype"]))
async def uptype_command(bot, message):
    if message.chat.id not in (Config.AUTH_USERS + Config.ADMIN +
                               Config.OWNER):
        return await message.reply_text(
            "🚫 **You Are Not Authorized To Use This Bot. Contact: [Sam! X](https://t.me/SamXD7)**",
            disable_web_page_preview=True,
            quote=True,
        )
    await changemode(bot, message)


@bot.on_message(filters.incoming & filters.command(["ffmpeg"]))
async def ffmpeg_command(bot, message):
    if message.chat.id not in (Config.AUTH_USERS + Config.ADMIN +
                               Config.OWNER):
        return await message.reply_text(
            "🚫 **You Are Not Authorized To Use This Bot. Contact: [Sam! X](https://t.me/SamXD7)**",
            disable_web_page_preview=True,
            quote=True,
        )
    await get_ffmpeg(bot, message)


@bot.on_message(filters.incoming & filters.command(["mode"]))
async def mode_command(bot, message):
    if message.chat.id not in (Config.AUTH_USERS + Config.ADMIN +
                               Config.OWNER):
        return await message.reply_text(
            "🚫 **You Are Not Authorized To Use This Bot. Contact: [Sam! X](https://t.me/SamXD7)**",
            disable_web_page_preview=True,
            quote=True,
        )
    await get_type(bot, message)


@bot.on_message(filters.incoming & filters.command(["upload"]))
async def upload_command(bot, message):
    if message.chat.id not in (Config.AUTH_USERS + Config.ADMIN +
                               Config.OWNER):
        return await message.reply_text(
            "🚫 **You Are Not Authorized To Use This Bot. Contact: [Sam! X](https://t.me/SamXD7)**",
            disable_web_page_preview=True,
            quote=True,
        )
    await upload_dir(bot, message)


@bot.on_message(filters.incoming & filters.command(["download"]))
async def download_command(bot, message):
    if message.chat.id not in (Config.AUTH_USERS + Config.ADMIN +
                               Config.OWNER):
        return await message.reply_text(
            "🚫 **You Are Not Authorized To Use This Bot. Contact: [Sam! X](https://t.me/SamXD7)**",
            disable_web_page_preview=True,
            quote=True,
        )
    await download_dir(bot, message)


@bot.on_message(filters.incoming & filters.command(["info"]))
async def info_command(bot, message):
    if message.chat.id not in (Config.AUTH_USERS + Config.ADMIN +
                               Config.OWNER):
        return await message.reply_text(
            "🚫 **You Are Not Authorized To Use This Bot. Contact: [Sam! X](https://t.me/SamXD7)**",
            disable_web_page_preview=True,
            quote=True,
        )
    await mediainfo(bot, message)


@bot.on_message(filters.incoming & filters.command(["simp"]))
async def simp_command(bot, message):
    if message.chat.id not in (Config.AUTH_USERS + Config.ADMIN +
                               Config.OWNER):
        return await message.reply_text(
            "🚫 **You Are Not Authorized To Use This Bot. Contact: [Sam! X](https://t.me/SamXD7)**",
            disable_web_page_preview=True,
            quote=True,
        )
    await sample(bot, message)


@bot.on_message(filters.incoming & filters.command(["vshot"]))
async def vshot_command(bot, message):
    if message.chat.id not in (Config.AUTH_USERS + Config.ADMIN +
                               Config.OWNER):
        return await message.reply_text(
            "🚫 **You Are Not Authorized To Use This Bot. Contact: [Sam! X](https://t.me/SamXD7)**",
            disable_web_page_preview=True,
            quote=True,
        )
    await vshots(bot, message)


@bot.on_message(filters.incoming & filters.command(["status"]))
async def status_command(bot, message):
    if message.chat.id not in (Config.AUTH_USERS + Config.ADMIN +
                               Config.OWNER):
        return await message.reply_text(
            "🚫 **You Are Not Authorized To Use This Bot. Contact: [Sam! X](https://t.me/SamXD7)**",
            disable_web_page_preview=True,
            quote=True,
        )
    await sysinfo(message)


@bot.on_message(filters.incoming & filters.command(["restart"]))
async def restart_command(bot, message):
    if message.chat.id not in (Config.ADMIN + Config.OWNER):
        return await message.reply_text("**Access Denied.** 🔒", quote=True)
    await message.reply_text("🔄 **Restarting The Bot...**", quote=True)
    time.sleep(2)
    sys.exit()


@bot.on_message(filters.incoming & filters.command(["permit"]))
async def permit_command(bot, message):
    if message.chat.id not in (Config.ADMIN + Config.OWNER):
        return await message.reply_text("**Access Denied.** 🔒", quote=True)
    command_parts = message.text.split(" ")
    if len(command_parts) == 2:
        user_id = re.findall(r"\d+", command_parts[1])
        if user_id:
            user_id = int(user_id[0])
        else:
            return await message.reply_text(
                "⚠️ **Invalid Command Format. Please Use '/permit user_id' To Add A User.**",
                quote=True,
            )
    else:
        return await message.reply_text(
            "⚠️ **Invalid Command Format. Please Use '/permit user_id' To Add A User.**",
            quote=True,
        )
    Config.AUTH_USERS.append(user_id)
    await message.reply_text(f"✅ **User `{user_id}` Has Been Added.**",
                             quote=True)


@bot.on_message(filters.incoming & filters.command(["cancelall"]))
async def cancelall_command(bot, message):
    if message.chat.id not in (Config.ADMIN + Config.OWNER):
        return await message.reply_text("**Access Denied.** 🔒", quote=True)
    await renew(message)


@bot.on_message(filters.incoming & filters.command(["clear"]))
async def clear_command(bot, message):
    if message.chat.id not in (Config.ADMIN + Config.OWNER):
        return await message.reply_text("**Access Denied.** 🔒", quote=True)
    data.clear()
    list_handler.clear()
    queue.delete_many({})
    await message.reply_text("🚮 **Cleared Queued Files!**", quote=True)


@bot.on_message(filters.incoming & filters.command(["exec"]))
async def exec_command(bot, message):
    if message.chat.id not in Config.OWNER:
        return await message.reply_text("🛑 **Error 401: Not Authorized.**",
                                        quote=True)
    await exec_message_f(bot, message)


@bot.on_message(filters.incoming & filters.command(["eval"]))
async def eval_command(bot, message):
    if message.chat.id not in Config.OWNER:
        return await message.reply_text("🛑 **Error 401: Not Authorized.**",
                                        quote=True)
    await eval_message_f(bot, message)


@bot.on_message(filters.incoming & filters.command(["logs"]))
async def logs_command(bot, message):
    if message.chat.id not in Config.OWNER:
        return await message.reply_text("🛑 **Error 401: Not Authorized.**",
                                        quote=True)
    await message.reply_document("Logs.txt", quote=True)


@bot.on_message(filters.incoming & filters.command(["shutdown"]))
async def shutdown_command(bot, message):
    if message.chat.id not in Config.OWNER:
        return await message.reply_text("🛑 **Error 401: Not Authorized.**",
                                        quote=True)
    await message.reply_text("⛔️ **Shutting Down The Bot.**", quote=True)
    time.sleep(2)
    sys.exit(1)


async def checkup():
    try:
        await napana()
        if len(data) >= 1:
            LOGS.info("adding task")
            await add_task1(data[0])
    except Exception as e:
        LOGS.info(e)


async def startup():
    await bot.start()
    LOGS.info(f"[Started]: @{(await bot.get_me()).username}")
    bot_username = (await bot.get_me()).username
    bot_link = f"https://t.me/{bot_username}"
    await bot.send_message(
        chat_id=Config.LOG_CHANNEL,
        text=f"**[🔄 Bot Has Started.]({bot_link})**",
        disable_web_page_preview=True,
    )
    LOGS.info("STARTING CHECKUP")
    await checkup()
    await idle()
    await bot.stop()


bot.loop.run_until_complete(startup())

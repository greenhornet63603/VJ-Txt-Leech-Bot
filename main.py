# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import re
import sys
import time
import asyncio
import requests

import core as helper
from vars import API_ID, API_HASH, BOT_TOKEN

from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# ---------------- START ---------------- #

@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    await m.reply_text(
        f"<b>Hello {m.from_user.mention} 👋\n\n"
        f"I Am A Bot For Download Links From Your .TXT File "
        f"And Then Upload That File On Telegram.\n\n"
        f"Use /upload To Start.\n"
        f"Use /stop to stop any ongoing task.</b>"
    )


# ---------------- STOP ---------------- #

@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped 🚦**")
    os.execl(sys.executable, sys.executable, *sys.argv)


# ---------------- LINK PARSER ---------------- #

def parse_links(content):
    links = []

    url_pattern = r'(https?://[^\s]+)'

    for line in content:
        line = line.strip()

        if not line:
            continue

        url_match = re.search(url_pattern, line)

        if not url_match:
            continue

        url = url_match.group(1).strip()

        # Remove URL from line
        name = re.sub(url_pattern, '', line)

        # Clean unwanted chars
        name = (
            name.replace("🎬", "")
                .replace("»", "")
                .replace("|", "")
                .replace(":", "")
                .replace("-", "")
                .strip()
        )

        if not name:
            name = "Untitled Video"

        links.append([name, url])

    return links


# ---------------- UPLOAD ---------------- #

@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):

    editable = await m.reply_text("**Send TXT File ⚡️**")

    input_file: Message = await bot.listen(editable.chat.id)

    x = await input_file.download()

    await input_file.delete(True)

    # ---------------- READ TXT ---------------- #

    try:
        with open(x, "r", encoding="utf-8") as f:
            content = f.readlines()

        links = parse_links(content)

        os.remove(x)

    except Exception as e:
        await m.reply_text(f"**Invalid file input.**\n\n{e}")

        if os.path.exists(x):
            os.remove(x)

        return

    if len(links) == 0:
        await m.reply_text("**No valid links found in TXT file.**")
        return

    # ---------------- START INDEX ---------------- #

    await editable.edit(
        f"**Total Links Found 🔗 : {len(links)}**\n\n"
        f"Send Starting Index\n\n"
        f"Example: 1"
    )

    input0: Message = await bot.listen(editable.chat.id)

    raw_text = input0.text

    await input0.delete(True)

    # ---------------- BATCH NAME ---------------- #

    await editable.edit("**Now Send Batch Name**")

    input1: Message = await bot.listen(editable.chat.id)

    raw_text0 = input1.text

    await input1.delete(True)

    # ---------------- QUALITY ---------------- #

    await editable.edit(
        "**Enter Resolution 📸**\n\n"
        "144 / 240 / 360 / 480 / 720 / 1080"
    )

    input2: Message = await bot.listen(editable.chat.id)

    raw_text2 = input2.text

    await input2.delete(True)

    # ---------------- CAPTION ---------------- #

    await editable.edit("**Now Send Caption**")

    input3: Message = await bot.listen(editable.chat.id)

    raw_text3 = input3.text

    await input3.delete(True)

    MR = raw_text3

    # ---------------- THUMB ---------------- #

    await editable.edit(
        "Send Thumbnail URL\n\n"
        "Or send: no"
    )

    input6: Message = await bot.listen(editable.chat.id)

    raw_text6 = input6.text

    await input6.delete(True)

    await editable.delete()

    thumb = None

    if raw_text6.startswith("http://") or raw_text6.startswith("https://"):

        getstatusoutput(f"wget '{raw_text6}' -O 'thumb.jpg'")

        thumb = "thumb.jpg"

    # ---------------- COUNT ---------------- #

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    # ---------------- LOOP ---------------- #

    try:

        for i in range(count - 1, len(links)):

            url = links[i][1]

            # Fix URLs
            url = (
                url.replace("file/d/", "uc?export=download&id=")
                .replace("www.youtube-nocookie.com/embed", "youtu.be")
                .replace("?modestbranding=1", "")
                .replace("/view?usp=sharing", "")
            )

            if not url.startswith("http"):
                url = "https://" + url

            # ---------------- Vision IAS ---------------- #

            if "visionias" in url:

                async with ClientSession() as session:

                    async with session.get(url) as resp:

                        text = await resp.text()

                        match = re.search(
                            r"(https://.*?playlist.m3u8.*?)\"",
                            text
                        )

                        if match:
                            url = match.group(1)

            # ---------------- Classplus ---------------- #

            elif "videos.classplusapp" in url:

                response = requests.get(
                    f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}'
                )

                try:
                    url = response.json()['url']
                except:
                    pass

            # ---------------- MPD ---------------- #

            elif "/master.mpd" in url:

                vid = url.split("/")[-2]

                url = f"https://d26g5bnklkwsh4.cloudfront.net/{vid}/master.m3u8"

            # ---------------- NAME ---------------- #

            name1 = (
                links[i][0]
                .replace("\t", "")
                .replace(":", "")
                .replace("/", "")
                .replace("+", "")
                .replace("#", "")
                .replace("|", "")
                .replace("@", "")
                .replace("*", "")
                .replace(".", "")
                .replace("https", "")
                .replace("http", "")
                .strip()
            )

            name = f'{str(count).zfill(3)}) {name1[:60]}'

            # ---------------- FORMAT ---------------- #

            if "youtu" in url:

                ytf = (
                    f"b[height<={raw_text2}][ext=mp4]/"
                    f"bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/"
                    f"b[ext=mp4]"
                )

            else:

                ytf = (
                    f"b[height<={raw_text2}]/"
                    f"bv[height<={raw_text2}]+ba/b/bv+ba"
                )

            # ---------------- CMD ---------------- #

            if "jw-prod" in url:

                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            else:

                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            # ---------------- CAPTION ---------------- #

            cc = (
                f'**[📽️] Vid_ID:** {str(count).zfill(3)}\n'
                f'**Title:** {name1}\n'
                f'**Batch:** {raw_text0}\n\n'
                f'{MR}'
            )

            cc1 = (
                f'**[📁] Pdf_ID:** {str(count).zfill(3)}\n'
                f'**Title:** {name1}\n'
                f'**Batch:** {raw_text0}\n\n'
                f'{MR}'
            )

            try:

                # ---------------- DRIVE ---------------- #

                if "drive" in url:

                    try:

                        ka = await helper.download(url, name)

                        await bot.send_document(
                            chat_id=m.chat.id,
                            document=ka,
                            caption=cc1
                        )

                        count += 1

                        os.remove(ka)

                        time.sleep(1)

                    except FloodWait as e:

                        await m.reply_text(str(e))

                        time.sleep(e.value)

                        continue

                # ---------------- PDF ---------------- #

                elif ".pdf" in url:

                    try:

                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'

                        download_cmd = (
                            f"{cmd} -R 25 --fragment-retries 25"
                        )

                        os.system(download_cmd)

                        await bot.send_document(
                            chat_id=m.chat.id,
                            document=f'{name}.pdf',
                            caption=cc1
                        )

                        count += 1

                        os.remove(f'{name}.pdf')

                    except FloodWait as e:

                        await m.reply_text(str(e))

                        time.sleep(e.value)

                        continue

                # ---------------- VIDEO ---------------- #

                else:

                    show = (
                        f"**Downloading ⬇️**\n\n"
                        f"**Name »** `{name}`\n"
                        f"**Quality »** `{raw_text2}`"
                    )

                    prog = await m.reply_text(show)

                    res_file = await helper.download_video(
                        url,
                        cmd,
                        name
                    )

                    filename = res_file

                    await prog.delete(True)

                    await helper.send_vid(
                        bot,
                        m,
                        cc,
                        filename,
                        thumb,
                        name,
                        prog
                    )

                    count += 1

                    time.sleep(1)

            except Exception as e:

                await m.reply_text(
                    f"**Downloading Interrupted ❌**\n\n"
                    f"**Error:** `{str(e)}`\n\n"
                    f"**Name:** `{name}`\n"
                    f"**URL:** `{url}`"
                )

                continue

    except Exception as e:

        await m.reply_text(f"**Error:**\n`{e}`")

    await m.reply_text("**Done Boss 😎**")


# ---------------- RUN ---------------- #

bot.run()

# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import re
import sys
import time
import requests

import core as helper
from vars import API_ID, API_HASH, BOT_TOKEN

from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

# ---------------- BOT ---------------- #

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
        f"I Am A TXT Link Downloader Bot.\n"
        f"Send /upload To Start.\n\n"
        f"Use /stop to stop ongoing tasks.</b>"
    )

# ---------------- STOP ---------------- #

@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped 🚦**")
    os.execl(sys.executable, sys.executable, *sys.argv)

# ---------------- LINK PARSER ---------------- #

def parse_links(content):

    links = []

    for line in content:

        line = line.strip()

        if not line:
            continue

        # Extract URL
        urls = re.findall(r'https?://[^\s]+', line)

        if not urls:
            continue

        url = urls[0].strip()

        # Skip broken encoded classplus links
        if "media-cdn.classplusapp.comL" in url:
            continue

        # Remove URL from title
        title = line.replace(url, "").strip()

        # Clean dangerous chars
        title = re.sub(r'[\\/:*?"<>|#@]+', '', title)

        # Remove emojis
        title = re.sub(r'[^\w\s.-]', '', title)

        title = title.strip()

        if not title:
            title = "Untitled"

        links.append([title, url])

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

        await m.reply_text(f"**Invalid TXT File ❌**\n\n`{e}`")

        if os.path.exists(x):
            os.remove(x)

        return

    if len(links) == 0:
        await m.reply_text("**No valid links found ❌**")
        return

    # ---------------- START INDEX ---------------- #

    await editable.edit(
        f"**Total Links Found :** `{len(links)}`\n\n"
        f"Send Start Index\n\n"
        f"Example: `1`"
    )

    input0: Message = await bot.listen(editable.chat.id)

    raw_text = input0.text

    await input0.delete(True)

    # ---------------- BATCH NAME ---------------- #

    await editable.edit("**Send Batch Name**")

    input1: Message = await bot.listen(editable.chat.id)

    raw_text0 = input1.text

    await input1.delete(True)

    # ---------------- QUALITY ---------------- #

    await editable.edit(
        "**Choose Quality 📸**\n\n"
        "144\n240\n360\n480\n720\n1080"
    )

    input2: Message = await bot.listen(editable.chat.id)

    raw_text2 = input2.text

    await input2.delete(True)

    # ---------------- CAPTION ---------------- #

    await editable.edit("**Send Caption**")

    input3: Message = await bot.listen(editable.chat.id)

    raw_text3 = input3.text

    await input3.delete(True)

    MR = raw_text3

    # ---------------- THUMB ---------------- #

    await editable.edit(
        "**Send Thumbnail URL**\n\n"
        "Or send `no`"
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

            # ---------------- FIX URLS ---------------- #

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

            elif (
                "classplusapp" in url
                or "media-cdn.classplusapp.com" in url
            ):

                try:

                    # Already signed URL
                    if "Expires=" in url or "Signature=" in url:
                        pass

                    else:

                        response = requests.get(
                            "https://api.classplusapp.com/cams/uploader/video/jw-signed-url",
                            params={"url": url},
                            timeout=20
                        )

                        data = response.json()

                        if "url" in data:
                            url = data["url"]

                except Exception as e:
                    print(e)

            # ---------------- MPD FIX ---------------- #

            elif "/master.mpd" in url:

                vid = url.split("/")[-2]

                url = f"https://d26g5bnklkwsh4.cloudfront.net/{vid}/master.m3u8"

            # ---------------- SAFE FILE NAME ---------------- #

            name1 = links[i][0]

            # Remove emojis and dangerous chars
            safe_name = re.sub(r'[^\w\s.-]', '', name1)

            safe_name = (
                safe_name
                .replace("\t", "")
                .replace(":", "")
                .replace("/", "")
                .replace("\\", "")
                .replace("|", "")
                .replace("*", "")
                .replace("?", "")
                .replace("<", "")
                .replace(">", "")
                .replace('"', "")
                .strip()
            )

            safe_name = safe_name.replace(" ", "_")

            if not safe_name:
                safe_name = "video"

            name = f'{str(count).zfill(3)}_{safe_name[:80]}'

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

            # ---------------- YT-DLP CMD ---------------- #

            cmd = (
                f'yt-dlp '
                f'--no-check-certificates '
                f'--add-header "Referer:https://web.classplusapp.com/" '
                f'--add-header "Origin:https://web.classplusapp.com" '
                f'--add-header "User-Agent:Mozilla/5.0" '
                f'--concurrent-fragments 10 '
                f'--fragment-retries 10 '
                f'--retries 10 '
                f'-f "{ytf}" '
                f'-o "{name}.mp4" "{url}"'
            )

            # ---------------- CAPTIONS ---------------- #

            cc = (
                f'**📽️ Video ID :** `{str(count).zfill(3)}`\n'
                f'**🎬 Title :** `{name1}`\n'
                f'**📚 Batch :** `{raw_text0}`\n\n'
                f'{MR}'
            )

            cc1 = (
                f'**📁 PDF ID :** `{str(count).zfill(3)}`\n'
                f'**📄 Title :** `{name1}`\n'
                f'**📚 Batch :** `{raw_text0}`\n\n'
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

                        cmd = (
                            f'yt-dlp '
                            f'--add-header "Referer:https://web.classplusapp.com/" '
                            f'-o "{name}.pdf" "{url}"'
                        )

                        os.system(cmd)

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
                        f"**⬇️ Downloading Video...**\n\n"
                        f"**📝 Name :** `{name}`\n"
                        f"**🎞 Quality :** `{raw_text2}`"
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
                    f"**❌ Download Failed**\n\n"
                    f"**Error :** `{str(e)}`\n\n"
                    f"**Name :** `{name}`\n\n"
                    f"**URL :** `{url}`"
                )

                continue

    except Exception as e:

        await m.reply_text(f"**Error ❌**\n\n`{e}`")

    await m.reply_text("**Done Boss 😎**")

# ---------------- RUN ---------------- #

bot.run()

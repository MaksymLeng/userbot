from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel
from dotenv import load_dotenv
import os
import asyncio
import json
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsRecent
from telethon.tl.custom.button import Button

# Загрузка .env
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ACCESS_HASH = int(os.getenv("ACCESS_HASH"))

client = TelegramClient("userbot", API_ID, API_HASH)
DATA_FILE = "users.json"

async def load_users():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print("⚠️ users.json пуст или повреждён — создаю заново.")
            return set()
    return set()

async def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(list(data), f)

async def send_welcome(user):
    try:
        video_path = "assets/intro.mp4"
        caption = (
            "Илтимос, ҳозироқ 5 дақиқа ичида менеджеримизга ёзинг,\n"
            "акс ҳолда аризангиз бекор қилинади.\n"
            "📌 Бу сизнинг кредитни олишингиз учун сӯнгги қадам.\n"
            "Ҳозир ёзинг! ⏳👇👇👇"
        )

        await client.send_file(
            user.id,
            video_path,
            caption=caption
        )

        await client.send_message(
            user.id,
            "📩 [Связаться с менеджером](https://t.me/manager_uzi)",
            parse_mode="markdown"
        )
    except Exception as e:
        print(f"⛔ {user.id} — ошибка отправки видео: {e}")

async def check_new():
    entity = InputPeerChannel(channel_id=CHANNEL_ID, access_hash=ACCESS_HASH)
    known = await load_users()
    updated = set(known)

    participants = await client(GetParticipantsRequest(
        channel=entity,
        filter=ChannelParticipantsRecent(),
        offset=0,
        limit=100,
        hash=0
    ))

    is_first_run = len(known) == 0

    for user in participants.users:
        if user.bot or user.deleted:
            continue
        if str(user.id) not in known:
            print(f"🔊 Новый: {user.first_name}")

            if not is_first_run:
                await send_welcome(user)

            updated.add(str(user.id))

    await save_users(updated)

async def main():
    await client.start()
    while True:
        await check_new()
        await asyncio.sleep(10)

client.loop.run_until_complete(main())

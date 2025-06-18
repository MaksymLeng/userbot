import mimetypes
import os
import json
import asyncio
from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsRecent

async def run_userbot(bot_config):
    client = TelegramClient(bot_config['session'], bot_config['api_id'], bot_config['api_hash'])
    await client.start()

    entity = InputPeerChannel(channel_id=bot_config['channel_id'], access_hash=bot_config['access_hash'])
    data_file = f"users_{bot_config['session']}.json"

    if os.path.exists(data_file):
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                known_users = set(json.load(f))
        except json.JSONDecodeError:
            print(f"⚠️ JSON повреждён для {bot_config['session']} — создаю заново.")
            known_users = set()
    else:
        known_users = set()

    async def save_users(users):
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(list(users), f, ensure_ascii=False, indent=2)

    async def send_welcome(user):
        try:
            file_path = bot_config["media"]
            caption = bot_config["text"]
            manager_link = bot_config["manager_url"]

            if not os.path.exists(file_path):
                print(f"⚠️ Файл не найден: {file_path}")
                return

            mime_type, _ = mimetypes.guess_type(file_path)
            is_video = mime_type and mime_type.startswith("video")
            is_image = mime_type and mime_type.startswith("image")

            if is_video or is_image:
                await client.send_file(user.id, file_path, caption=caption)
            else:
                await client.send_message(user.id, caption)

            await client.send_message(
                user.id,
                f"📩 [Связаться с менеджером]({manager_link})",
                parse_mode="markdown"
            )
        except Exception as e:
            print(f"⛔ {user.id} — ошибка отправки welcome-сообщения: {e}")

    async def check():
        participants = await client(GetParticipantsRequest(
            channel=entity,
            filter=ChannelParticipantsRecent(),
            offset=0,
            limit=100,
            hash=0
        ))

        is_first_run = len(known_users) == 0

        for user in participants.users:
            if user.bot or user.deleted:
                continue
            if str(user.id) not in known_users:
                print(f"🔊 Новый пользователь: {user.first_name} ({user.id})")
                if not is_first_run:
                    await send_welcome(user)
                known_users.add(str(user.id))

        await save_users(known_users)

    while True:
        await check()
        await asyncio.sleep(10)

async def main():
    with open("bots.json", "r", encoding="utf-8") as f:
        configs = json.load(f)

    tasks = [run_userbot(cfg) for cfg in configs]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

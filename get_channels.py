from telethon import TelegramClient
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION", "temp_session")

client = TelegramClient(SESSION, API_ID, API_HASH)

async def main():
    await client.start()
    dialogs = await client.get_dialogs()

    print("\n📋 Список доступных каналов/групп:\n")
    for dialog in dialogs:
        if dialog.is_channel:
            print(f"Название: {dialog.name}")
            print(f"ID: {dialog.entity.id}")
            print(f"ACCESS_HASH: {dialog.entity.access_hash}\n")

if __name__ == "__main__":
    asyncio.run(main())

import time
import zipfile
from os import getenv as env
from contextlib import asynccontextmanager
import os
import uvicorn
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from fastapi import FastAPI, Response
from pydantic import BaseModel

WEBHOOK_URL = env('WEBHOOK_URL')
print(WEBHOOK_URL)
BOT_TOKEN = os.getenv('BOT_TOKEN')
print(BOT_TOKEN)
WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
CHAT_ID = env('CHAT_ID')


class TgBot(BaseModel):
    bot_token: str

bot = Bot(
    token=TgBot(bot_token=BOT_TOKEN).bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()

# type: ignore

WEBHOOK_URL_FULL = f"{WEBHOOK_URL}{WEBHOOK_PATH}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(url=WEBHOOK_URL_FULL)
    yield
    await bot.delete_webhook()



app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)

url_path = (f"{WEBHOOK_PATH}/log/file/all" + "/{server_name}")

@app.post(url_path)
async def get_all_log_file_view(server_name: str, file_content: dict):
    file_name = f"{server_name} | {time.ctime()}"
    if file_content['content'] == "":
        return Response(status_code=400)
    with open(f'{file_name}.log', 'w') as file:
        file.write(file_content['content'])
    zip_file_name = f'{file_name}.zip'

    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(f'{file_name}.log')

    document = FSInputFile(f'{file_name}.zip')
    await bot.send_document(chat_id=CHAT_ID, document=document)
    os.remove(f'{file_name}.log')
    os.remove(f'{file_name}.zip')
    return Response(status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8392)

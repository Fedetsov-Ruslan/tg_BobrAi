import os
import asyncio
import aiohttp
import uvicorn

from app.middlewares.db import DataBaseSession
from app.database.engine import drop_db, session_maker, create_db
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.handlers.user_private import user_private_router
from app.commands.command import command
from restapi import app


load_dotenv()

bot = Bot(token=os.getenv("TG_TOKEN"))
dp = Dispatcher()
dp.include_router(user_private_router)


async def on_startup():
    # await drop_db()
    await create_db()
    dp.http_session = aiohttp.ClientSession()

async def on_shutdown():
    await dp.http_session.close()
    await bot.session.close()


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)    
    dp.update.middleware(DataBaseSession(session_poll=session_maker))

    try:
      await bot.set_my_commands(commands=command, scope=BotCommandScopeAllPrivateChats())
      await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
      dp.http_session = aiohttp.ClientSession()
    except KeyboardInterrupt:
        
        await bot.session.close()
        # await bot.close()
        print("bot dont active")


if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run(app, host="127.0.0.1", port=8000)

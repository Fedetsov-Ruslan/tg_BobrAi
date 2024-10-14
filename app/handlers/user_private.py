import os
import aiohttp
import redis
import json

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv

from app.database.orm_query import orm_save_city, orm_get_city, orm_save_logs

load_dotenv()

class MyCity(StatesGroup):
    city = State()
REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis.from_url(REDIS_URL)
WEATHER_KEY = os.getenv("WEATHER_KEY")

user_private_router = Router()


async def get_weather(city:str, message: Message, session: AsyncSession):
    """функция получения погоды и ответ пользователю"""
    response = redis_client.get(city)
    if response is None:
        params = {
            'q': city,
            'units': 'metric', 
            'lang': 'ru',       
            'appid': WEATHER_KEY    
        }
        url = "https://api.openweathermap.org/data/2.5/weather"
        async with aiohttp.ClientSession() as s:
            async with s.get(url, params=params) as resp:
                response = await resp.json()
        try:
            await message.answer(
                f'Температура - {response["main"]["temp"]}, \n'
                f'Ощущается как {response["main"]["feels_like"]}, \n'
                f'{response["weather"][0]["description"]}, \n'
                f'Влажность {response["main"]["humidity"]}%, \n'
                f'Скорость ветра {response["wind"]["speed"]} км/ч'
            )
            redis_client.set(city, json.dumps(response), ex=300)
        except KeyError:  
            await message.answer(response["message"])
        finally:
            await orm_save_logs(session=session, user_id=message.from_user.id, request=city, response=json.dumps(response))
    else:
        response = json.loads(response)
        try:
            await message.answer(
                f'Температура - {response["main"]["temp"]}, \n'
                f'Ощущается как {response["main"]["feels_like"]}, \n'
                f'{response["weather"][0]["description"]}, \n'
                f'Влажность {response["main"]["humidity"]}%, \n'
                f'Скорость ветра {response["wind"]["speed"]} км/ч'
            )
        except KeyError:  
            await message.answer(response["message"])
        finally:
            await orm_save_logs(session=session, user_id=message.from_user.id, request=city, response=json.dumps(response))
    

@user_private_router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer("Привет, это бот для компании BobrAi.")
    
    
@user_private_router.message(Command("weather"))
async def get_weather_in_city(message: Message, session: AsyncSession):
    try:
        city = message.text.split()[1].lower()
    except:
        await message.answer('Вы не указали город после команды /weather или указали вовсе не город')
    await get_weather(city, message, session)
                

@user_private_router.message(Command('save'))
async def save_city(message: Message, state: FSMContext):
    await message.answer('В каком городе хотите сохранить?')
    await state.set_state(MyCity.city)
  
  
@user_private_router.message(MyCity.city)
async def save_city(message: Message, state: FSMContext, session: AsyncSession):
    city = message.text.split()[0].lower()
    user_id = message.from_user.id
    await orm_save_city(session, city, user_id)
    await message.answer('Город сохранен')
    await state.clear() 


@user_private_router.message(Command('mycity'))
async def weather_in_my_city(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    city = await orm_get_city(session, user_id)
    if city is None:
        await message.answer('Вы еще не сохраняли город')
    else:
        await get_weather(city.city, message, session)
        
import pytest
import json
from aiogram.types import Message
from unittest.mock import AsyncMock, MagicMock

from app.handlers.user_private import get_weather_in_city

@pytest.mark.asyncio
async def test_get_weather_in_city():
    """Тестовый случай команды /weather"""
    message = MagicMock(spec=Message)
    message.text = "/weather Moscow"
    message.from_user = MagicMock()
    message.from_user.id = 12345
    message.answer = AsyncMock() 
    session = AsyncMock() 
    
    await get_weather_in_city(message, session)

    message.answer.assert_awaited()  
    args = str(message.answer.call_args)
    
    assert "температура" in args.lower()
    assert "ощущается как" in args.lower()
    assert "влажность" in args.lower()
    assert "скорость ветра" in args.lower()

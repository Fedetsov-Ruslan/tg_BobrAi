import pytest
from unittest.mock import AsyncMock, MagicMock
import json

from app.handlers.user_private import get_weather

@pytest.mark.asyncio
async def test_get_weather_with_redis():
    redis_client = MagicMock()

    city = "Moscow"
    mock_response = {
        "main": {"temp": 10, "feels_like": 8},
        "weather": [{"description": "clear sky"}],
        "wind": {"speed": 2}
    }
    redis_client.get.return_value = json.dumps(mock_response)
    message = MagicMock()
    message.answer = AsyncMock()
    session = AsyncMock() 
    
    await get_weather(city, message, session)
    
    message.answer.assert_awaited()  
    args = str(message.answer.call_args)
    
    assert "температура" in args.lower()
    assert "ощущается как" in args.lower()
    assert "влажность" in args.lower()
    assert "скорость ветра" in args.lower()

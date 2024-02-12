from unittest.mock import patch, AsyncMock
import pytest
from main import app
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_send_telegram_message() :
    with patch('telegram.Bot.send_message', new_callable=AsyncMock) as mock_send :
        async with AsyncClient(app=app, base_url="http://test") as ac :
            response = await ac.post("/orders/", json={"customer_id" : 1, "total_amount" : 100})

        assert response.status_code == 200

        mock_send.assert_called_once()

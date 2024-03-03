import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from hsbot_refac import reqRank

class TestReqRank(unittest.TestCase):
    @patch('requests.get')
    async def test_reqRank(self, mock_get):
        # Mocking the response content
        mock_get.return_value.content = BeautifulSoup('<body><p>Test</p></body>', 'html.parser').encode()

        # Mocking the status code
        mock_get.return_value.status_code = 200

        # Mocking the encoding
        mock_get.return_value.encoding = 'utf-8'

        # Test data
        data = Message(text="test")  # replace with actual Message object
        region = "us"
        leaderboardId = "STD"
        keyword = "test"

        # Call the function
        result = await reqRank(data, region, leaderboardId, keyword)

        # Check the result
        self.assertEqual(result, "Expected result")  # replace with the expected result

    @patch('requests.get')
    async def test_reqRank_bad_response(self, mock_get):
        # Mocking the response content
        mock_get.return_value.content = BeautifulSoup('<body><p>Bad</p></body>', 'html.parser').encode()

        # Mocking the status code
        mock_get.return_value.status_code = 200

        # Mocking the encoding
        mock_get.return_value.encoding = 'utf-8'

        # Test data
        data = Message(text="test")  # replace with actual Message object
        region = "us"
        leaderboardId = "STD"
        keyword = "test"

        # Call the function
        result = await reqRank(data, region, leaderboardId, keyword)

        # Check the result
        self.assertEqual(result, "Expected result")  # replace with the expected result

if __name__ == '__main__':
    unittest.main()
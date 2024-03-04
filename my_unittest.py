import unittest
from unittest.mock import patch, Mock, PropertyMock
from bs4 import BeautifulSoup
from hsbot_refac import reqRank

class TestReqRank(unittest.IsolatedAsyncioTestCase):
    @patch('requests.get')
    async def test_reqRank(self, mock_get):
        # Mocking the requests.get response
        mock_response = Mock()
        mock_get.return_value = mock_response
        mock_response.content = '<html><body>Test Body</body></html>'
        mock_response.encoding = 'utf-8'

        # Mocking the BeautifulSoup object
        mock_soup = BeautifulSoup(mock_response.content, 'html.parser')
        type(mock_soup.body).text = PropertyMock(return_value='Test Body')

        # Mocking the Message object
        mock_data = Mock()
        mock_data.text = '查美服狂野Sola'

        # Test with leaderboardId as "STD"
        result = await reqRank(mock_data, 'US', 'STD', '查美服狂野')
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
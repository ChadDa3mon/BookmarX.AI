
import sys
import os
# Run 'pytest' from within the 'apps' directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import Mock, patch
from utils import search_db, get_all_bookmarx, get_bookmarx_by_id, add_bookmark

def test_search_db():
    # Create a mock for the cursor
    cursor_mock = Mock()
    cursor_mock.fetchall.return_value = [(1, 'http://example.com', 'Example')]

    # Call the function with a test argument
    result = search_db('test', cursor=cursor_mock)

    # Check that the mock was used correctly
    cursor_mock.execute.assert_called_once_with(
        'select id,url,summary from webpages where match(raw_text) against (%s in natural language mode);',
        ('test',)
    )
    cursor_mock.fetchall.assert_called_once()

    # Check that the result is as expected
    assert result == [(1, 'http://example.com', 'Example')]




def test_get_all_bookmarx():
    # Placeholder for test
    pass

def test_get_bookmarx_by_id():
    # Placeholder for test
    pass

def test_add_bookmark():
    # Placeholder for test
    pass


import sys
import os
# This helps me to run 'pytest' from within the 'apps' directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from urllib.parse import urlparse, parse_qs, urlencode
from models import Bookmarx,Bookmark

def test_bookmark():
    # Create a Bookmark with a test input
    bookmark = Bookmark(url='http://example.com?utm_source=test')

    # Check that the Bookmark's attributes are as expected
    assert str(bookmark.url) == 'http://example.com/'

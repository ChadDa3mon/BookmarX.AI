from pydantic import BaseModel,validator, HttpUrl,root_validator,Field
import urllib.parse
from typing import ClassVar,List
from logstuff import setup_logging
from urllib.parse import urlparse, parse_qs, urlencode


logger = setup_logging()

class Bookmark(BaseModel):
    url: HttpUrl

    #tracking_params_to_remove = ['utm_source', 'utm_medium', 'utm_name', 'utm_content', 'utm_term']
    tracking_params_to_remove: ClassVar[list] = ['utm_source', 'utm_medium', 'utm_name', 'utm_content', 'utm_term']

    @validator('url', pre=True)
    def strip_utm(cls, v):
        # Parse the URL and the query string
        parsed_url = urlparse(v)
        query_params = parse_qs(parsed_url.query)

        # Remove the tracking parameters
        query_params.pop('utm_source', None)
        query_params.pop('utm_medium', None)
        query_params.pop('utm_campaign', None)

        # Construct a new query string without the tracking parameters
        new_query = urlencode(query_params, doseq=True)

        # Replace the old query string with the new one in the URL
        stripped_url = parsed_url._replace(query=new_query).geturl()
        logger.debug(f"DEBUG: Original URL: {v}")
        logger.debug(f"DEBUG: Stripped URL: {stripped_url}")
        return stripped_url


    # @validator('url', pre=True) 
    # def strip_tracking_info(cls, value):
    #     logger.info(f"Received URL {value}, checking for tracking parameters")
    #     # Parse the URL to get its components
    #     parsed_url = urllib.parse.urlparse(value)

    #     # Check if the query component of the URL contains tracking parameters
    #     query_params = urllib.parse.parse_qs(parsed_url.query)

    #     # Remove the specified tracking parameters from the query string
    #     for param in cls.tracking_params_to_remove:
    #         logger.debug(f"Removed tracking parameter '{param}'")
    #         query_params.pop(param, None)

    #     # Rebuild the query string without the removed tracking parameters
    #     new_query_string = urllib.parse.urlencode(query_params, doseq=True)

    #     # Reassemble the URL with the modified query string
    #     new_url = parsed_url._replace(query=new_query_string).geturl()
    #     # logger.debug(f"URL after stripping out tracking: {new_url}")
    #     if new_url == value:
    #         logger.debug(f"No tracking found")
    #     else:
    #         logger.debug(f"Tracking found, new URL: {new_url}")
    #     return new_url 

class BookmarxResponse(BaseModel):
    url: str
    summary: str
    raw_text: str
    markdown: str

class Bookmarx(BaseModel):
    """Bookmarx represents a single entry"""
    id: int = Field(..., description="Some description of the int", ge=0)
    url: str
    summary: str

class BookmarxListResponse(BaseModel):
    bookmarx: List[Bookmarx]

def URLAlreadyExistsError(Exception):
    pass

def WriteArticleToDBError(Exception):
    pass
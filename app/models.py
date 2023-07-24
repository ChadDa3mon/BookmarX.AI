from pydantic import BaseModel,validator, HttpUrl,root_validator
import urllib.parse
from typing import ClassVar
from logstuff import setup_logging

logger = setup_logging()

class Bookmark(BaseModel):
    url: HttpUrl

    #tracking_params_to_remove = ['utm_source', 'utm_medium', 'utm_name', 'utm_content', 'utm_term']
    tracking_params_to_remove: ClassVar[list] = ['utm_source', 'utm_medium', 'utm_name', 'utm_content', 'utm_term']


    @validator('url', pre=True) 
    def strip_tracking_info(cls, value):
        logger.info(f"Received URL {value}, checking for tracking parameters")
        # Parse the URL to get its components
        parsed_url = urllib.parse.urlparse(value)

        # Check if the query component of the URL contains tracking parameters
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # Remove the specified tracking parameters from the query string
        for param in cls.tracking_params_to_remove:
            logger.debug(f"Removed tracking parameter '{param}'")
            query_params.pop(param, None)

        # Rebuild the query string without the removed tracking parameters
        new_query_string = urllib.parse.urlencode(query_params, doseq=True)

        # Reassemble the URL with the modified query string
        new_url = parsed_url._replace(query=new_query_string).geturl()
        # logger.debug(f"URL after stripping out tracking: {new_url}")
        if new_url == value:
            logger.debug(f"No tracking found")
        else:
            logger.debug(f"Tracking found, new URL: {new_url}")
        return new_url 
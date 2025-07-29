import requests
from datetime import datetime
from typing import Union, Literal, List
from mcp.server import FastMCP
from pydantic import Field
from typing import Annotated
from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP, Context
import os
from dotenv import load_dotenv
load_dotenv()
rapid_api_key = os.getenv("RAPID_API_KEY")

__rapidapi_url__ = 'https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-web-search'

mcp = FastMCP('real-time-web-search')

@mcp.tool()
def search(q: Annotated[str, Field(description='Search query. Supports all Google Advanced Search operators (site:, inurl:, intitle:, etc).')],
           num: Annotated[Union[int, float, None], Field(description='Maximum number of results to return. Default: 10 Allowed values: 1-500 Important note: each request for 50 results will be counted as a request in quota. For example, if num=45 is considered a single request and num=140 is considered as 3 requests. Default: 10')] = None,
           start: Annotated[Union[int, float, None], Field(description='Number of results to skip (for pagination). Default: 0 Allowed values: positive integers Default: 0')] = None,
           gl: Annotated[Union[str, None], Field(description='The country / region for which to make the query. Default: us Allowed values: 2-letter country code, see ISO 3166-1 alpha-2')] = None,
           hl: Annotated[Union[str, None], Field(description="The language to use for the search (Google's hl parameter). Default: en Allowed values: 2-letter country code, see ISO 639-1 alpha-2")] = None,
           tbs: Annotated[Union[str, None], Field(description="This parameter defines advanced search parameters that aren't available using regular query parameters (to be searched).")] = None,
           location: Annotated[Union[str, None], Field(description='Where you want the search to originate from. It is recommended to specify location at the city level in order to simulate a real user’s search (e.g. London, England, United Kingdom).')] = None,
           nfpr: Annotated[Union[str, None], Field(description='Exclude results of auto-corrected query when the original query is misspelled with nfpr=1 and include them with nfpr=0 (default).')] = None) -> dict: 
    '''Get real-time organic search results from across the web with support for Google Search parameters (gl, hl, tbs, etc) and city level geo targeting. Supports all Google Advanced Search operators such (e.g. inurl:, site:, intitle:, etc).'''
    url = 'https://real-time-web-search.p.rapidapi.com/search-advanced'
    headers = {'x-rapidapi-host': 'real-time-web-search.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'q': q,
        'num': num,
        'start': start,
        'gl': gl,
        'hl': hl,
        'tbs': tbs,
        'location': location,
        'nfpr': nfpr,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def batch_search(data: Annotated[dict, Field(description='')] = None) -> dict: 
    '''Lightning fast endpoint for getting organic search results from across the web in real-time with support for up to 100 queries in a single request. Supports all Google Advanced Search operators such (e.g. inurl:, site:, intitle:, etc).'''
    url = 'https://real-time-web-search.p.rapidapi.com/search'
    headers = {'Content-Type': 'application/json', 'x-rapidapi-host': 'real-time-web-search.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    response = requests.post(url, headers=headers, json=data)
    return response.json()



if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9997
    mcp.run(transport="stdio")

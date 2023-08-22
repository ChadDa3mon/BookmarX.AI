import openai
import os
from dotenv import load_dotenv
import mysql.connector
import requests
from newspaper import Article,fulltext
import json
from datetime import date
import asyncio
from logstuff import setup_logging
from exceptions import URLAlreadyExistsError, WriteArticleToDBError
# import pymysql
# from pymysqlpool import ConnectionPool
import mysql.connector.pooling

logger = setup_logging()


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY","Error")
db_host = os.getenv("DB_HOST")
db_table = os.getenv("DB_TABLE")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")

# cnx = mysql.connector.connect(
#     host=db_host,
#     user=db_user,
#     password=db_pass,
#     database=db_name
#     )
pool = mysql.connector.pooling.MySQLConnectionPool(
    host=db_host,
    user=db_user,
    password=db_pass,
    database=db_name,
    pool_name="mypool",
    pool_size=5  # Set the desired pool size
)

# def search_db(search_term):
#     cnx = mysql.connector.connect(
#     host=db_host,
#     user=db_user,
#     password=db_pass,
#     database=db_name
#     )

#     logger.info(f"Searching for '{search_term}")
#     cursor = cnx.cursor()
#     query = "select id,url,summary from webpages where match(raw_text) against (%s in natural language mode);"
#     cursor.execute(query, (search_term,))
#     rows = cursor.fetchall()
#     cursor.close()
#     return rows

def search_db(search_term, cursor=None):
    # If no cursor is provided, create one using the connection
    if cursor is None:
        connection = pool.get_connection()
        cursor = connection.cursor()

    cursor.execute(
        'select id,url,summary from webpages where match(raw_text) against (%s in natural language mode);',
        (search_term,)
    )
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    # If a connection was created, close it
    # if cursor is None:
    #     cnx.close()

    return result


def get_all_bookmarx():
    connection = pool.get_connection()
    cursor = connection.cursor()
    query = "select id,url,summary from webpages"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    # Convert the rows tuple into a list of dictionaries
    bookmarx_list = [{"id": int(row[0]), "url": row[1], "summary": row[2]} for row in rows]
    return bookmarx_list

def get_bookmarx_by_id(id):
    logger.info(f"Retrieving results for ID: {id}")
    connection = pool.get_connection()
    cursor = connection.cursor()
    cursor = cnx.cursor()
    query = "select url,summary,raw_text,markdown from webpages where id = %s"
    cursor.execute(query,(id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if row is None: # Make sure I got something back
        logger.error(f"No results found for ID: {id}")
        return f"No match for ID: {id}"

    # row comes back as a tuple, I want to convert it to a dict so I can send it back via FastAPI as JSON
    if not isinstance(row,str): 
        logger.debug(f"Retrieved Results for ID {id}")
        bookmark_dict = {
            "url": row[0],
            "summary": row[1],
            "raw_text": row[2],
            "markdown": row[3]
        }
        return bookmark_dict
    else:
        logger.error(f"Error retrieving results for ID: {id}: {row}")
        return {"error": row}

    
    

def get_markdown(url):
    #my_url = url['URL'].tolist()[0]
    my_url_list = [url]
    #logger.info(f"Retrieving markdown for {url['URL'].tolist()[0]}")
    logger.info(f"Retrieving markdown for {url}")
    connection = pool.get_connection()
    cursor = connection.cursor()
    query = "select markdown from webpages where url = %s"
    #cursor.execute(query, (url['URL'].tolist()))
    cursor.execute(query, (my_url_list))
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if row is not None:
        # Extract the value from the tuple (assuming 'markdown' is the first column)
        markdown_text = row[0]
        return markdown_text
    else:
        logger.error(f"No markdown returned for {url}")
        # Handle the case when the query returns no results
        return False
    


async def get_tags():
    connection = pool.get_connection()
    cursor = connection.cursor()
    query = "SELECT * from tags"
    cursor.execute(query)
    rows = cursor.fetchall()
    tags_list = [row[1] for row in rows]
    cursor.close()
    connection.close()

    return tags_list

async def get_url_from_db(url):
    logger.debug(f"Checking DB for URL: {url}")
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        query = f"SELECT * from webpages where url = '{url}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        if not rows: #No results found
            logger.debug(f"URL {url} was not found in the database")
            return False
        else:
            logger.debug(f"Found URL {url} in database")
            return rows
    except Exception as e:
        logger.error(f"Error looking for URL: {url}: {e}")

async def write_article_to_db(webpage_title,webpage_summary,webpage_text,webpage_markdown,url,tags):
    logger.info(f"Writing URL: {url} to database")
    current_date = date.today().isoformat()
    tags_str = ",".join(tags)
    connection = pool.get_connection()
    cursor = connection.cursor()
    query = f"INSERT INTO {db_table} (url, title, date_added, summary, raw_text, tags, markdown) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (url, webpage_title, current_date, webpage_summary, webpage_text, tags_str, webpage_markdown)
    try:
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        logger.error(f"Error: {e} ")
        cursor.close()
        connection.close()
        return False




async def get_webpage_text(url):
    logger.info(f"Retrieving webpage text for {url}")
    article = Article(url)
    article.download()
    try:
        article.parse()
        article_title = article.title
        article_text = article.text
        logger.info(f" - parsed title: {article_title}")
    except:
        article_title = "No Title Found"
        html = requests.get(url).text
        article_text = fulltext(html)
    return article_title, article_text
        


async def query_gpt_summary(body):
    tags = await get_tags()

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages = [
        {
            "role":"system",
            "content":f"""
You are a helpful assistant who will summarize the body of a website for me. 
For the following article, you will do two things: Create a 1 paragraph summary, 
and assign any tags from my list you think are applicable. 
The list of tags I want you to consider is {tags}. Your response should be in JSON, for example:

    "tags":list_of_tags,
    "summary":webpage_summary

"""
        },
        {
            "role":"user",
            "content":body
        }
    ],
    temperature=.4,
    max_tokens=1024,
    api_key=openai_api_key 
    ) 

    return response.choices[0].message.content

async def query_gpt_markdown(body):

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages = [
        {
            "role":"system",
            "content":f"""
You are an AI assistant. I am going to give you the raw text from a website
and you will transform it into markdown syntax, then send it back to me."""
        },
        {
            "role":"user",
            "content":body
        }
    ],
    temperature=.4,
    max_tokens=1024,
    api_key=openai_api_key
    ) 

    return response.choices[0].message.content

async def add_bookmark(url):
    logger.info(f"Received request to download {url}")
    logger.info(f"Checking to see if we already have {url} in our database")

    already_exists = await get_url_from_db(url)
    if already_exists:
        msg = f"URL {url} already exists in database"
        logger.info(msg)
        raise URLAlreadyExistsError(msg)
        return msg
    
    logger.info(f"{url} not found in database, proceeding to add")
    
    webpage_title, webpage_text = await get_webpage_text(url)
    webpage_summary_payload = await query_gpt_summary(webpage_text)
    webpage_dict = json.loads(webpage_summary_payload)
    tags = webpage_dict['tags']
    webpage_summary = webpage_dict['summary']
    webpage_markdown = await query_gpt_markdown(webpage_text)
    db_update_reult = await write_article_to_db(webpage_title,webpage_summary,webpage_text,webpage_markdown,url,tags)

    if not db_update_reult:
        msg = f"Failed to add URL {url} the database"
        logger.error(msg)
        raise WriteArticleToDBError(msg)
    
    logger.info(f"URL {url} successfully added to database")
  

if __name__ == "__main__":
    url = "https://www.linkedin.com/pulse/3-ways-vector-databases-take-your-llm-use-cases-next-level-mishra"
    #add_bookmark(url)
    #results = get_bookmarx_by_id("1")
    results = get_all_bookmarx()
    print(f"Results is type {type(results)}\n{results} ")
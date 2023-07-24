# BookmarX.AI
(Still very much a work in progress, calling this an Alpha release would be generous)

I read a lot, and I come across a lot of great links. Sometimes I'm at work, but most of the time I'm on my phone. Having almost zero attention spam or working memory, I want a way to store these articles so I can find them later, if need be. 

With this new Generative AI stuff, I also wanted to utilize ChatGPT to do some work for me. 

This script will do the following when you send it a URL:
- Strip out tracking parameters in the URL
- Grab the raw text (no images right now)
- Send the text to ChatGPT along with a list of tags I want it to consider (the list of tags is a static list that covers every type of thing I care about)
- ChatGPT then:
  - Provides a summary of the page
  - Looks at the whole list of tags I care about and applies the ones it thinks are applicable
  - Takes the raw web page and converts it into Markdown
- I take all of that and then store it in a MySQL DB. This DB now has:
  - The Original URL
  - The Summary 
  - The applicable tags
  - The Markdown version

# Installation
This is my first time doing something like this so please go easy on me :)

The database structure itself is stored in `bookmarx.sql`. You should be able to create the databse with `mysql -u <username> -p <database_name> < database_structure.sql`. 

Add your tags to the 'tags' table, just one tag per row

Build the docker container with `sudo docker build -t bookmarx .`

Copy `.env-template` to `.env` and fill in the values

You should then be able to run things with this command: `sudo docker run -d -p 8332:8000 --env-file .env bookmarkx`

## Installation and deployment with Docker Compose

You can run one of the following commands to start the application with Docker Compose:

```bash
# Newer versions of Docker include compose functionality
docker compose up -d
# If docker-compose is installed as a separate package
docker-compose up -d
```

# Usage
Right now I just have the API endpoint for submitting a bookmark (I'm much more concerned with being able store things first....retrieve them later). 

Make a POST to /bookmarks/add with a simple JSON payload: `{"url":"<url you want to scrape"}`. Depending on the size of the article and how quickly ChatGPT is responding, it can take 2 or 3 minutes to go through. Your initial REST API call may time out. You can examine the logs via `docker logs` or there is a log file in the container (`/app/request.log`) to confirm if it was submitted. 

## iPhone
As the vast majority of links I come across are while I'm on my phone, sharing this from my iPhone has been my number one priority. I don't know the first thing about IOS app development, but I was able to create a Shortcut that lets me 'share' a webpage to it, and then sends the JSON payload to my server. 

# Roadmap
- Create a front end using Gradio
- Integrate all of this into a docker container and get it up on docker hub
- Figure out how to make an ios app 
- Build in some automated web scrapping via rss feeds, reddit api etc
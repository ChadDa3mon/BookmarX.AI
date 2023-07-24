# Lynx
(Yes, I need a better name)

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

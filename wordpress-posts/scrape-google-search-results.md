# Scrape Google Search Results Page

Here's a short script that will scrape the first 100 listings in the Google Organic results.

You might want to use this to find the position of your sites and track their position for certain target keyword phrases over time. That could be a very good way to determine, for example, if your SEO efforts are working. Or you could use the list of URLs as a starting point for some other web crawling activity.

As the script is written it will just dump the list of URLs to a txt file.

It uses the [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) library to help with parsing the HTML page.

Example Usage:

```bash
$ python GoogleScrape.py
$ cat links.txt
http://www.halotis.com/
http://www.halotis.com/2009/07/01/rss-twitter-bot-in-python/
http://www.blogcatalog.com/blogs/halotis.html
http://www.blogcatalog.com/topic/sqlite/
http://ieeexplore.ieee.org/iel5/10358/32956/01543043.pdf?arnumber=1543043
http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=1543043
http://doi.ieeecomputersociety.org/10.1109/DATE.2001.915065
http://rapidlibrary.com/index.php?q=hal+otis
http://www.tagza.com/Software/Video_tutorial_-_URL_re-directing_software-___HalOtis/
http://portal.acm.org/citation.cfm?id=367328
...
```

Here's the script:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2009 HalOtis Marketing
# written by Matt Warren
# http://halotis.com/

import urllib,urllib2

from BeautifulSoup import BeautifulSoup

def google_grab(query):

    address = "http://www.google.com/search?q=%s&num=100&hl=en&start=0" % (urllib.quote_plus(query))
    request = urllib2.Request(address, None, {'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'} )
    urlfile = urllib2.urlopen(request)
    page = urlfile.read(200000)
    urlfile.close()

    soup = BeautifulSoup(page)
    links = [x['href'] for x in soup.findAll('a', attrs={'class':'l'})]

    return links

if __name__=='__main__':
    # Example: Search written to file
    links = google_grab('halotis')
    open("links.txt","w+b").write("\n".join(links))
```

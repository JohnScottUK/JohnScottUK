#!/usr/bin/env python3
import feedparser
from datetime import datetime as dt
import os
import re

print("{}: Update README.md".format(os.path.basename(__file__)))

url="https://www.jsware.io/feed.xml"
filename = "{}/README.md".format(os.path.dirname(os.path.abspath(__file__)))

print("Grabbing feed '{}'...".format(url))
feed = feedparser.parse(url)
entries = [
  {
    "title": entry["title"],
    "link": entry["link"].split("#")[0],
    "published": dt.strptime(entry["published"],"%Y-%m-%dT%H:%M:%S%z")
  }
  for entry in feed["entries"]
]

print("Generating markdown...")
markdown = "\n".join(["* [{0}]({1}) <sup>{2}</sup>".format(entry["title"], entry["link"], entry["published"].strftime("%d %b %Y")) for entry in entries])

print("Reading '{}'...".format(filename))
with open(filename) as f:
  readme = f.read()

readme = re.sub("<\!-- begin blog -->(\n|.)*<\!-- end blog -->", "<!-- begin blog -->\n\n" + markdown + "\n<!-- end blog -->", readme)

print("Writing '{}'...".format(filename))
with open(filename, "w") as f:
  f.write(readme)

from urllib.request import urlopen
import re

url = "https://www.wetter.com/wetter_aktuell/wettervorhersage/7_tagesvorhersage/deutschland/ulm/DE0010708.html"
page = urlopen(url)
html = page.read().decode("utf-8")

# Search for tag with string
start_index = html.find("<title>") + len("<title>")
end_index = html.find("</title>")
title = html[start_index:end_index]
print(title)

# with regex, prepared for inconsistent coding like <TITLE >Profile: Dionysus</title  / >
pattern = "<title.*?>.*?</title.*?>"
match_results = re.search(pattern, html, re.IGNORECASE)
title = match_results.group()
title = re.sub("<.*?>", "", title) # Remove HTML tags
print(f"Content of title tag: {title}")

# This tag is about possibility of rain <span class="[ forecast-navigation-precipitation-probability ]">0 %</span>
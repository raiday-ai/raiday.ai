# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 06:50:14 2024

@author: anto
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import pandas as pd

# Fetch the webpage
url = 'https://raiday.ai/blog/ai-tool/pixcribe/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all links
links = soup.find_all('a', href=True)

# Filter external URLs without parameters and exclude specific ones
external_urls = []
for link in links:
    href = link['href']
    parsed_url = urlparse(href)
    
    # Strip parameters and query
    stripped_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
    
    if parsed_url.netloc and parsed_url.scheme and \
       'raiday' not in stripped_url and \
       'open.spotify.com' not in stripped_url and \
       'facebook.com' not in stripped_url:
        external_urls.append(stripped_url)

# Remove duplicates
external_urls = list(set(external_urls))

# Check if each URL is valid and save results to a list
data = []

for ext_url in external_urls:
    try:
        res = requests.head(ext_url, timeout=5)
        valid = 'yes' if res.status_code == 200 else 'no'
        data.append({'URL': ext_url, 'Valid': valid, 'Status Code': res.status_code})
    except requests.RequestException:
        data.append({'URL': ext_url, 'Valid': 'no', 'Status Code': 'N/A'})

# Convert data to DataFrame and save as CSV
df = pd.DataFrame(data)
csv_filename = 'external_urls_validation.csv'
df.to_csv(csv_filename, index=False)

print(f"Results saved to {csv_filename}")


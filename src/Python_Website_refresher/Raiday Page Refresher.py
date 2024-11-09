import requests
import time
from bs4 import BeautifulSoup

# Step 1: Fetch and parse the sitemap of https://raiday.ai
sitemap_url = "https://raiday.ai/sitemap.xml"
response = requests.get(sitemap_url)

if response.status_code == 200:
    sitemap_xml = response.text
    soup = BeautifulSoup(sitemap_xml, 'xml')
    urls = [loc.text for loc in soup.find_all('loc')]
    total_pages = len(urls)
    
    # Print the count of all pages
    print(f"Total pages found: {total_pages}")
    
    # User agents for desktop and mobile simulation
    headers_desktop = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    headers_mobile = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    }
    
    # Step 2: Loop through each page URL with a 1-second interval for each type of request
    for idx, url in enumerate(urls, 1):
        # Simulate desktop page request
        page_response_desktop = requests.get(url, headers=headers_desktop)
        if page_response_desktop.status_code == 200:
            print(f"Desktop request for Page {idx}/{total_pages} successful: {url}")
        else:
            print(f"Desktop request for Page {idx}/{total_pages} failed (status code {page_response_desktop.status_code}): {url}")
        
        # Display progress for desktop request
        progress_desktop = ((idx - 1 + 0.5) / total_pages) * 100
        print(f"Progress (Desktop): {progress_desktop:.2f}%")
        
        # Sleep for 1 second before next request
        time.sleep(1)
        
        # Simulate mobile page request
        page_response_mobile = requests.get(url, headers=headers_mobile)
        if page_response_mobile.status_code == 200:
            print(f"Mobile request for Page {idx}/{total_pages} successful: {url}")
        else:
            print(f"Mobile request for Page {idx}/{total_pages} failed (status code {page_response_mobile.status_code}): {url}")
        
        # Display progress for mobile request
        progress_mobile = (idx / total_pages) * 100
        print(f"Progress (Mobile): {progress_mobile:.2f}%")
        
        # Sleep for 1 second before the next request
        time.sleep(2)
else:
    print("Failed to fetch the sitemap.")

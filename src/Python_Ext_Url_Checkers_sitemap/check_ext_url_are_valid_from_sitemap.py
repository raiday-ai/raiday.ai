# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 06:50:14 2024

@author: anto
"""

import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import pandas as pd
import csv

# Step 1: Fetch and parse the sitemap of https://raiday.ai
sitemap_url = "https://raiday.ai/sitemap.xml"
response = requests.get(sitemap_url)

# Function to count zero-width spaces in the page content
def count_zwsp(text):
    zwsp_char = '\u200b'
    return text.count(zwsp_char)

# Function to count non-breaking spaces in the page content
def count_nbsp(text):
    nbsp_char = '\u00a0'
    return text.count(nbsp_char)

if response.status_code == 200:
    sitemap_xml = response.text
    soup = BeautifulSoup(sitemap_xml, 'xml')
    urls = [loc.text for loc in soup.find_all('loc')]
    total_pages = len(urls)
    
    # Print the count of all pages
    print(f"Total pages found: {total_pages}")
    
    # User agents for desktop simulation
    headers_desktop = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    
    # CSV filename
    csv_filename = 'external_urls_validation_all_pages.csv'
    
    # Create the CSV file and write the header
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Page URL', 'External URL', 'Valid', 'Status Code', 'ZWSP Count', 'NBSP Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Step 2: Loop through each page URL
        for idx, url in enumerate(urls, 1):
            # Simulate desktop page request
            page_response_desktop = requests.get(url, headers=headers_desktop)
            
            if page_response_desktop.status_code == 200:
                print(f"Desktop request for Page {idx}/{total_pages} successful: {url}")
                page_soup = BeautifulSoup(page_response_desktop.text, 'html.parser')
                
                # Count zero-width spaces and non-breaking spaces in the page content
                zwsp_count = count_zwsp(page_response_desktop.text)
                nbsp_count = count_nbsp(page_response_desktop.text)
                
                # Print the counts for the current URL
                print(f"Page URL: {url}")
                print(f"  ZWSP Count: {zwsp_count}")
                print(f"  NBSP Count: {nbsp_count}")
                
                # Extract all links from the page
                links = page_soup.find_all('a', href=True)
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
                
                if external_urls:
                    for ext_url in external_urls:
                        print(f"Testing external URL: {ext_url}")  # Print the URL being tested
                        try:
                            res = requests.head(ext_url, timeout=5)
                            valid = 'yes' if res.status_code == 200 else 'no'
                            writer.writerow({'Page URL': url, 'External URL': ext_url, 'Valid': valid, 'Status Code': res.status_code, 'ZWSP Count': zwsp_count, 'NBSP Count': nbsp_count})
                        except requests.RequestException:
                            writer.writerow({'Page URL': url, 'External URL': ext_url, 'Valid': 'no', 'Status Code': 'N/A', 'ZWSP Count': zwsp_count, 'NBSP Count': nbsp_count})
                else:
                    # Write page details even if no external URLs found
                    writer.writerow({'Page URL': url, 'External URL': 'N/A', 'Valid': 'N/A', 'Status Code': 'N/A', 'ZWSP Count': zwsp_count, 'NBSP Count': nbsp_count})
                    
                    # Sleep for 1 second only if no external URLs were found
                    time.sleep(1)
            
            else:
                print(f"Desktop request for Page {idx}/{total_pages} failed (status code {page_response_desktop.status_code}): {url}")
            
            # Display progress for desktop request
            progress_desktop = (idx / total_pages) * 100
            print(f"Progress (Desktop): {progress_desktop:.2f}%")
    
    print(f"Results saved to {csv_filename}")
else:
    print("Failed to fetch the sitemap.")


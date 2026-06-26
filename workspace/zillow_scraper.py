#!/usr/bin/env python3
import requests
import re
import json
import os
from urllib.parse import urljoin
import time

def fetch_zillow_page(url):
    """Fetch Zillow page with proper headers"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

def extract_image_urls(html_content):
    """Extract image URLs from Zillow page HTML"""
    image_urls = []
    
    # Pattern for Zillow image URLs - they often contain /photos/
    patterns = [
        r'https://photos\.zillowstatic\.com/fp/[^\s"\']+',
        r'https://www\.zillowstatic\.com/[^\s"\']+\.(jpg|jpeg|png|webp)',
        r'"url":"([^"]+\.(jpg|jpeg|png|webp)[^"]*)"',
        r'https://photos\.zillowstatic\.com/[^\s"\']+\.(jpg|jpeg|png|webp)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                url = match[0]
            else:
                url = match
            if url not in image_urls:
                image_urls.append(url)
    
    # Also look for JSON data that might contain images
    json_patterns = [
        r'__NEXT_DATA__\s*=\s*({.+?});',
        r'<script[^>]*id="__NEXT_DATA__"[^>]*>({.+?})</script>',
        r'"media":\s*\[({.+?})\]',
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, html_content, re.DOTALL)
        for match in matches:
            try:
                data = json.loads(match)
                # Try to extract images from JSON structure
                images = extract_from_json(data)
                for img in images:
                    if img not in image_urls:
                        image_urls.append(img)
            except:
                pass
    
    return image_urls

def extract_from_json(data):
    """Recursively extract image URLs from JSON data"""
    images = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            if key in ['url', 'imageUrl', 'photoUrl', 'src', 'href'] and isinstance(value, str):
                if value.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    images.append(value)
            elif isinstance(value, (dict, list)):
                images.extend(extract_from_json(value))
    elif isinstance(data, list):
        for item in data:
            images.extend(extract_from_json(item))
    
    return images

def main():
    url = "https://www.zillow.com/homedetails/916-NW-3rd-Ave-Fort-Lauderdale-FL-33311/2113660399_zpid/?utm_campaign=iosappmessage&utm_medium=referral&utm_source=txtshare"
    
    print(f"Fetching Zillow page: {url}")
    html = fetch_zillow_page(url)
    
    if not html:
        print("Failed to fetch page")
        return
    
    # Save HTML for debugging
    with open('/root/.openclaw/workspace/zillow_page.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("Extracting image URLs...")
    image_urls = extract_image_urls(html)
    
    print(f"Found {len(image_urls)} potential image URLs")
    
    # Filter and deduplicate
    unique_urls = []
    seen = set()
    for url in image_urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
    
    # Save URLs to file
    with open('/root/.openclaw/workspace/zillow_image_urls.txt', 'w') as f:
        for i, img_url in enumerate(unique_urls[:23], 1):
            f.write(f"{i}. {img_url}\n")
    
    print(f"Saved {len(unique_urls[:23])} image URLs to zillow_image_urls.txt")
    
    # Try to download first few images as test
    download_dir = '/root/.openclaw/workspace/zillow_images'
    os.makedirs(download_dir, exist_ok=True)
    
    print(f"\nAttempting to download images to {download_dir}...")
    successful_downloads = 0
    
    for i, img_url in enumerate(unique_urls[:5], 1):  # Try first 5 as test
        try:
            print(f"Downloading image {i}: {img_url[:80]}...")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            response = requests.get(img_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Try to determine file extension
                content_type = response.headers.get('content-type', '')
                if 'jpeg' in content_type or 'jpg' in content_type:
                    ext = 'jpg'
                elif 'png' in content_type:
                    ext = 'png'
                elif 'webp' in content_type:
                    ext = 'webp'
                else:
                    # Fallback from URL
                    if img_url.lower().endswith(('.jpg', '.jpeg')):
                        ext = 'jpg'
                    elif img_url.lower().endswith('.png'):
                        ext = 'png'
                    elif img_url.lower().endswith('.webp'):
                        ext = 'webp'
                    else:
                        ext = 'jpg'
                
                filename = os.path.join(download_dir, f'image_{i:02d}.{ext}')
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"  ✓ Saved as {filename}")
                successful_downloads += 1
            else:
                print(f"  ✗ Failed with status code: {response.status_code}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print(f"\nSuccessfully downloaded {successful_downloads} test images")
    print(f"Total unique image URLs found: {len(unique_urls)}")

if __name__ == "__main__":
    main()
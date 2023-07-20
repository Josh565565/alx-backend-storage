#!/usr/bin/env python3
"""
create a web cach
"""
import redis
import requests

rc = redis.Redis()

def get_page(url: str) -> str:
    cached_content = rc.get(f"cached:{url}")

    if cached_content:
        print("Cache hit!")
        return cached_content.decode('utf-8')

    print("Cache miss!")
    resp = requests.get(url)
    rc.setex(f"cached:{url}", 10, resp.text)
    rc.incr(f"count:{url}")
    return resp.text

if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com'
    html_content = get_page(url)
    print(html_content)

    # Test caching
    html_content = get_page(url)  # Should be cached and retrieved without making a request
    print(html_content)

    # Wait for the cache to expire (10 seconds) and test again
    import time
    time.sleep(11)
    html_content = get_page(url)  # Should make a new request as the cache has expired
    print(html_content)


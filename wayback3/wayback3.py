"""
Simple Python 3-safe package for accessing Wayback Machine archives
via its JSON API
"""

import datetime
import requests

FORMAT_STRING = "%Y%m%d%H%M%S"  # Looks like "20130919044612"
AVAILABILITY_URL = "http://archive.org/wayback/available?url=%s"
WAYBACK_URL_ROOT = "http://web.archive.org"


def availability(url):
    response = requests.get(AVAILABILITY_URL % (url))
    print(response)
    print(response.text)
    response_j = response.json()
    if response_j.get('archived_snapshots') == {}:
        return None
    else:
        closest = response_j.get('archived_snapshots').get('closest')
        avail = closest.get('available')
        status = int(closest.get('status'))
        timestamp = closest.get('timestamp')
        timestamp = datetime.datetime.strptime(timestamp, FORMAT_STRING)
        url = closest.get('url')
    return {'verbatim': closest, 'url': url, 'timestamp': timestamp}

def crawl(url):
    avail = availability(url)
    if avail:
        response = requests.get(avail['url'])
        return {
            'timestamp': avail['timestamp'],
            'wayback_url': avail['url'],
            'content': response.content,
        }

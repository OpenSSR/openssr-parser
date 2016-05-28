"""
Test wayback3
"""
import wayback3

test_url = "http://example.com"
avail = wayback3.availability(test_url)
assert avail['url'] == "http://web.archive.org/web/20160527151638/http://www.example.com"

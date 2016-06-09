import re

SSRN_AUTHOR_URL = "http://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=%s"
SSRN_ABSTRACT_URL_LONG = "http://papers.ssrn.com/sol3/papers.cfm?abstract_id=%s"
SSRN_ABSTRACT_URL_SHORT = "http://ssrn.com/abstract=%s"
ID_EXTRACTOR_SHORT_RE = re.compile(r"http\:\/\/(papers\.)?ssrn\.com\/abstract\=(\d+)")

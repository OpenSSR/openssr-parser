"""
Parse an SSRN abstract page
Example: http://web.archive.org/web/20160302003803/http://papers.ssrn.com/sol3/papers.cfm?abstract_id=562301
"""

# TODO:
# * Capture and save download timestamp (for WB)
# * Extract abstract ID

import sys
import re
import json
from bs4 import BeautifulSoup
from pprint import pprint
import ssrn_urls

author_id_re = re.compile(r"AbsByAuth\.cfm\?per_id=(\d+)")


def extract_paper_title(soup):
    title_div = soup.find_all(id="abstractTitle")[0]
    h1 = title_div.find_all('h1')[0]
    title = h1.string
    return title


def extract_abstract_id(soup):
    abstract_url_meta_tag = soup.find_all("meta", attrs={"name": "citation_abstract_html_url"})[0]
    abs_url = abstract_url_meta_tag.attrs.get('content')
    if abs_url is not None:
        abs_id = ssrn_urls.ID_EXTRACTOR_SHORT_RE.search(abs_url).groups()[1]
        return abs_id
    else:
        raise Exception("Didn't get an abstract url from a <meta> tag :(")


def extract_abstract_text(soup):
    try:
        abstract_div = soup.find_all(id="abstract")[0]
    except:
        print("FAILED to extract abstract!")
        return None
    else:
        # print("extract_abstract_text():\n%s" % abstract_div)
        # print()
        stuff = "\n".join(abstract_div.stripped_strings)
        # print(stuff)
        return stuff


def extract_author_id(author_link):
    """
    from, e.g.: /web/20160302003803/http://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=280597
    """
    # print(author_link)
    return author_id_re.search(author_link).groups()[0]


def extract_authors(soup):
    """
    Return an array of dictionaries about author_span
    """
    ret = []
    container = soup.find_all(id="innerWhite")[0]
    anchors = container.find_all('a')
    # pprint(anchors)
    for a in anchors:
        author_link = a.attrs['href']
        if author_link == "##":
            continue
        author_id = extract_author_id(author_link)
        author_name = "".join(a.find_all('h2')[0].stripped_strings).replace("  ", " ")  # OMG hacky
        ret.append({
            'author_name': author_name,
            'author_link': author_link,
            'author_id': author_id
            })
    return ret


def decrazify(numberish):
    s = numberish.strip()
    s = s.replace(',', '')
    return int(s)


def extract_stats(soup):
    container = soup.find_all('div', class_="statistics")[0]
    # print(container)

    labels = container.find_all(class_="statisticsText")
    # num_labels = len(labels)
    # print("* %d labels" % num_labels)
    # print(labels)
    # Only gets first 3 b/c citations are even crazier!

    spans = container.find_all(class_="statNumber")
    # Yay, gets all 5.
    numbers = [decrazify(span.string) for span in spans]
    # num_numbers = len(numbers)
    # print("* %d numbers" % num_numbers)
    # print("---")
    # print(labels)
    # print(spans)
    # print([span.string for span in spans])
    # print(numbers)
    # print("---")

    # Going to always have at least these 2 items:
    ret = {
        'abstract_views': numbers[0],
        'downloads': numbers[1]
    }

    # Add in optional ones:
    if len(numbers) >= 3:
        ret['download_rank'] = numbers[2]
    if len(numbers) >= 4:
        ret['forward_citations'] = numbers[3]
    if len(numbers) >= 5:
        ret['footnotes'] = numbers[4]

    # print("Returning:")
    # pprint(ret)

    # return {
    #     'download_rank': numbers[2],
    #     'forward_citations': numbers[3],
    #     'footnotes': numbers[4]
    #     }

    return ret


def main():
    soup = BeautifulSoup(
        open(sys.argv[1]),
        "html.parser")
    title = extract_paper_title(soup)
    abstract = extract_abstract_text(soup)
    abstract_id = extract_abstract_id(soup)
    authors = extract_authors(soup)
    stats = extract_stats(soup)

    print("Title: %s" % title)
    print("Authors: %s" %
          ["%s (%s)" % (author['author_name'], author['author_id']) for author in authors])
    print("Stats:")
    pprint(stats)

    print()

    d = {
        'title': title,
        'abstract': abstract,
        'abstract_id': abstract_id,
        'authors': authors,
        'stats': stats
        }
    pprint(d)

    f = open("abstract.json", "w")
    json.dump(d, f, indent=2)


if __name__ == '__main__':
    main()

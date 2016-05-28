import csv
import json
import os
import sys
import re
from bs4 import BeautifulSoup
import wayback3
from ssrn_urls import *

sample_dir = "sample-data"
# sample_filename = "Author Page for Anupam Chander _ SSRN.html"
sample_filename = "wb-author-275458.html"  # Copy from Wayback Machine
sample_output_filename = "chander.csv"
sample_output_filename_json = "chander.json"
sample_output_filename_tipue = "tipue.json"

paper_row_re = re.compile(r"row\_(\d)+")
title_link_re = re.compile(r"http\:\/\/ssrn\.com\/abstract\=(\d+)")


def get_author_name(soup):
    """
    Looking for: <span class="authorName"><h1>Anupam Chander</h1></span>
    """
    author_name = None
    author_span = soup.find_all(class_="authorName")[0]
    print(author_span)
    print(author_span.children)
    author_name = author_span.contents[0].string
    print("Found author name: %s" % author_name)
    return author_name

def extract_paper_id(paper_link):
    # TODO: Make it work on long links, too
    try:
        return title_link_re.search(paper_link).groups()[0]
    except:
        print("Exception during extract_paper_id()! Called on link: %s" % paper_link)
        return None

def get_papers(soup):
    papers = []

    # Find the table: it's a <table> with id="listItems"
    list_table = soup.find_all(id="listItems")

    # Find all paper rows. They have <tr id="row_1" ...>
    paper_rows = soup.find_all(id=paper_row_re)
    print("Found %d paper rows." % (len(paper_rows)))

    # Get titles:
    # <a class="textlink" href="http://ssrn.com/abstract=562301" target="_blank">The Romance of the Public Domain</a>
    for row in paper_rows:
        for row_a_tag in row.find_all(
                class_="textlink",
                target="_blank",
                href=title_link_re):

            try:
                paper_title = row_a_tag.string  # .encode('utf-8')
            except:
                paper_title = ""

            paper_link = row_a_tag.attrs['href']  # .encode('utf-8')
            print("\"%s\" at %s" % (paper_title, paper_link))

            paper_id = extract_paper_id(paper_link)

            papers.append({
                'title': paper_title,
                'link': paper_link,
                'id': paper_id
            })

    return papers


def main():
    soup = BeautifulSoup(
        open(sample_dir + os.sep + sample_filename),
        "html.parser")

    author_name = get_author_name(soup)

    papers = get_papers(soup)

    for paper in papers[:3]:
        paper_long_url = SSRN_ABSTRACT_URL_LONG % paper['id']
        wb = wayback3.crawl(paper_long_url)
        open(
            "sample-data/wb-abstract-%s.html" % paper['id'],
            "wb").write(wb['content'])

    # Set up output vars
    output_rows = []
    output_json = {'papers': [], 'author_name': author_name}
    output_tipue = {'pages': []}

    # Build outputs
    for paper in papers:
        output_rows.append([paper['title'], paper['link']])
        output_json['papers'].append(paper)
        output_tipue['pages'].append({'title': paper['title'], 'tags': 'SSRN', 'url': 'paper.html', 'text': 'Placeholder text. Replace with abstract.'})

    # Write output files
    print("Writing CSV output...")
    output_f = open(sample_output_filename, 'w')  # newline='')
    writer = csv.writer(output_f)
    writer.writerows(output_rows)
    output_f.close()
    print("Done.")

    print("Writing JSON output...")
    json_f = open(sample_output_filename_json, 'w')
    json_f.write(json.dumps(output_json))
    json_f.close()

    print("Writing JSON for Tipue Search...")
    tipue_f = open(sample_output_filename_tipue, 'w')
    tipue_f.write(json.dumps(output_tipue))
    tipue_f.close()

    print("Done.")

if __name__ == '__main__':
    main()

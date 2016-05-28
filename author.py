import csv
import json
import os
import sys
import re
from bs4 import BeautifulSoup

sample_dir = "sample-data"
sample_filename = "Author Page for Anupam Chander _ SSRN.html"
sample_output_filename = "chander.csv"
sample_output_filename_json = "chander.json"

paper_row_re = re.compile(r"row\_(\d)+")
title_link_re = re.compile(r"http\:\/\/ssrn\.com\/abstract\=(\d+)")


def main():
    author_name = "Anupam Chander"

    output_rows = []
    output_json = {'papers': [], 'author_name': author_name}

    soup = BeautifulSoup(
        open(sample_dir + os.sep + sample_filename),
        "html.parser")

    # Find the table: it's a <table> with id="listItems"
    list_table = soup.find_all(id="listItems")

    # Find all paper rows. They have <tr id="row_1" ...>
    paper_rows = soup.find_all(id=paper_row_re)
    print("Found %d paper rows." % (len(paper_rows)))

    # Get titles:
    # <a class="textlink" href="http://ssrn.com/abstract=562301" target="_blank">The Romance of the Public Domain</a>
    for row in paper_rows:
        # row_a_tag = row.find_all(class_="textlink")[0]
        # for row_a_tag in row.find_all(class_="textlink", target="_blank"):
        for row_a_tag in row.find_all(
                class_="textlink",
                target="_blank",
                href=title_link_re):

            try:
                paper_title = row_a_tag.string.encode('utf-8')
            except:
                paper_title = ""
            # print(row_a_tag.attrs)
            paper_link = row_a_tag.attrs['href'].encode('utf-8')
            print("\"%s\" at %s" % (paper_title, paper_link))

            output_rows.append([paper_title, paper_link])
            output_json['papers'].append({'title': paper_title, 'link': paper_link})

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
    print("Done.")

if __name__ == '__main__':
    main()

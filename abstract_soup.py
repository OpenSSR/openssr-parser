# import sys
from bs4 import BeautifulSoup

fn = "/Users/ajh/Code/openssr-parser/sample-data/wb-abstract-2770053.html"
soup = BeautifulSoup(
    open(fn),
    "html.parser")

print("Ready. Beautiful Soup object available as soup.")

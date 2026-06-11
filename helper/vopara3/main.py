import sys
import json
from pathlib import Path
from typing import Any
import requests
from bs4 import BeautifulSoup
import lxml
import re

# Add project root to sys.path (find the directory containing db_structs.py)
_root = Path(__file__).resolve().parent
while _root.parent != _root:
    if (_root / "db_structs.py").exists():
        if str(_root) not in sys.path:
            sys.path.append(str(_root))
        break
    _root = _root.parent

from db_structs import (
    Medium,
    Circle,
    Event,
    EventGroup,
    Source,
    ReliabilityTypes,
    OriginTypes,
    Location,
)

PATH_EVENT = Path(__file__).parent
PATH_CIRCLES_JSON = PATH_EVENT / "circles.json"
NAME = PATH_EVENT.name


def retrieve_soup_fetch_if_needed(url: str) -> BeautifulSoup:
    """Retrieve BeautifulSoup object for the given URL, fetching the content if necessary."""
    html_path = PATH_EVENT / "raw.html"
    if not html_path.exists():
        print(f"Raw HTML file not found, fetching from {url} ...")
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(
                f"Failed to retrieve data from {url}, status code: {response.status_code}"
            )
        html_path.write_bytes(response.content)
    with html_path.open("rb") as f:
        return BeautifulSoup(f, "lxml")


def sanitize_string(s: str) -> str:
    s = s.strip()
    s = re.sub(r"[\s\n\t]+", " ", s)
    return s


def main():
    """Create circles.json"""
    print(f"Retrieving circles information for {NAME} ...")
    raw_url = "https://ttc.ninja-web.net/vo-para/vo-para03_list.htm"
    
    # Parse the HTML content to extract circle information
    soup = retrieve_soup_fetch_if_needed(raw_url)
    circles = []

    # table: with border=1
    table = soup.select_one('table[border="1"]')
    if not table:
        raise Exception("Failed to find the circles table in the HTML content.")

    table_rows = table.select("tr")
    if not table_rows:
        raise Exception("No rows found in the circles table.")

    re_block_name = re.compile(r"【([^【】]*)】")
    current_block = ""  # e.g. 【ま】サークル名

    for row in table_rows:
        col_tags = row.select("td")
        if not col_tags:
            print(f"WARNING: invalid row {row=}")
            continue

        c0 = col_tags[0]
        c0text = c0.get_text(strip=True)
        if c0text.startswith("【"):  # New block
            m = re_block_name.search(c0text)
            if not m:
                print(f"WARNING: invalid row (fake new block) {row=}")
                continue
            current_block = sanitize_string(m.group(1))
        else:  #
            if len(col_tags) < 3 or len(col_tags) > 5:
                print(
                    f"WARNING: invalid row (wrong column count) {len(col_tags)}) {row=}"
                )
                continue

            circle_name = sanitize_string(c0text)
            circle_url = None
            a_tag = c0.select_one("a")
            if a_tag and a_tag.has_attr("href"):
                circle_url = a_tag["href"]
            pen_name = sanitize_string(col_tags[1].get_text(strip=True))
            booth_number = sanitize_string(col_tags[2].get_text(strip=True))

            position = f"{current_block}, {booth}"
            circle = Circle(
                aliases=[circle_name],
                pen_names=[pen_name] if pen_name else None,
                links=[circle_url] if circle_url else None,
                position=position,
            )

            circles.append(circle)

    # Save the extracted circle information to a JSON file
    with open(PATH_CIRCLES_JSON, "w", encoding="utf-8") as f:
        json.dump([c.get_json() for c in circles], f, ensure_ascii=False, indent=2)
    print(f"Saved {len(circles)} circles to {PATH_CIRCLES_JSON}")


if __name__ == "__main__":
    main()

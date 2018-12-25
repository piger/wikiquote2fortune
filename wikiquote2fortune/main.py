import os
import re
import textwrap
import click
import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


WIKIMEDIA_API_URL = "https://en.wikiquote.org/w/api.php"


def squeeze_whitespaces(text):
    return re.sub(r"\s+", " ", text)


def format_quote(season, episode, rows):
    """Reformat the text of a quote to be displayed as a fortune cookie"""

    expanded = []

    for row in rows:
        colon = row.find(":")

        if colon == -1:
            expanded.extend(textwrap.wrap(row))
            expanded.append("")
        else:
            indent = colon + 2
            expanded.extend(textwrap.wrap(row, subsequent_indent=" " * indent))

    text = "\n".join(expanded)

    season = squeeze_whitespaces(season)
    episode = squeeze_whitespaces(episode)

    q = {"season": season, "episode": episode, "text": text}
    return q


def fetch_page(name):
    """Fetch a Wikiquote page using the Wikimedia APIs"""

    params = {"action": "parse", "format": "json", "page": name}
    rv = requests.get(WIKIMEDIA_API_URL, params=params)
    if rv.status_code != 200:
        print(f"Unexpected HTTP code: {rv.status_code}\n{rv}")
        return None

    rv.encoding = "utf-8"
    data = rv.json()
    try:
        body = data["parse"]["text"]["*"]
        title = data["parse"]["title"]
    except ValueError:
        print("Something is wrong with the server response")
        raise

    return title, body


def h3_followed_by_span_headline(tag):
    if tag.name != "h3":
        return False

    if tag.next_element.name != "span":
        return False

    if tag.find("span", attrs={"class": "mw-headline"}) is None:
        return False

    return True


def parse_page(page_body):
    """Parse the HTML contents of a Wikiquote page and returns a list of quotes"""

    soup = BeautifulSoup(page_body, "lxml")
    quotes = []
    done = False

    # <h3> usually is the title of an episode
    for episode_block in soup.find_all(h3_followed_by_span_headline):
        if done:
            break

        next_element = episode_block.next_element
        if next_element.attrs["id"] == "External_links":
            break

        # <h2> is the name of the season
        season_name = episode_block.find_previous("h2").find("span").text
        episode_name = episode_block.find("span", attrs={"class": "mw-headline"}).text

        lines = []
        for element in episode_block.next_siblings:
            do_not_process = False

            # skip thumbnails
            if hasattr(element, "attrs") and "thumb" in element.get("class", []):
                do_not_process = True

            # <HR> separates quotes
            if element.name == "hr":
                quote = format_quote(season_name, episode_name, lines)
                quotes.append(quote)
                lines = []
                do_not_process = True

            # this can be ignored
            if element.string == "\n":
                do_not_process = True

            # small sections usually contain notes
            if element.find("small"):
                do_not_process = True

            if do_not_process is False and hasattr(element, "text"):
                lines.extend(element.text.split("\n"))

            ns = element.next_sibling

            # h3 is the next episode line
            if ns is None or ns.name == "h3":
                break

            # <h2> is the next episode, or another unrelated section
            if ns.name == "h2":
                # if it's followed by the "External Links" or "Cast" sections then we're done with
                # the quotes.
                next_span = ns.find(
                    "span", attrs={"id": ["Cast", "External_links"], "class": "mw-headline"}
                )
                if next_span is not None:
                    done = True

                break

        if lines:
            quote = format_quote(season_name, episode_name, lines)
            quotes.append(quote)
            lines = []

    return quotes


@click.command()
@click.option(
    "-o",
    "--output",
    type=click.File("wb"),
    metavar="FILENAME",
    default="-",
    help="Output filename",
)
@click.argument("name")
def main(output, name):
    title, content = fetch_page(name)
    quotes = parse_page(content)

    for quote in quotes:
        output.write(f"{quote['text']}\n\n".encode("utf-8"))
        output.write(
            f"\t\"{title}: {quote['episode']}, {quote['season']}\"\n".encode("utf-8")
        )
        output.write("%\n".encode("utf-8"))

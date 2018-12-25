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


def must_process(element):
    # skip thumbnails
    if hasattr(element, "attrs") and "thumb" in element.get("class", []):
        return False

    # this can be ignored
    if element.string == "\n":
        return False

    # small sections usually contain notes
    if element.find("small"):
        return False

    # finally, the element must have a ".text" attribute
    return hasattr(element, "text")


def parse_page(page_body):
    """Parse the HTML contents of a Wikiquote page and returns a list of quotes"""

    soup = BeautifulSoup(page_body, "lxml")
    quotes = []
    done = False

    # <h3> usually is the title of an episode
    for episode_block in soup.find_all(h3_followed_by_span_headline):
        # <h2> is the name of the season
        season_name = episode_block.find_previous("h2").find("span").text
        episode_name = episode_block.find("span", attrs={"class": "mw-headline"}).text
        new_quotes, stop_parsing = collect_quotes(season_name, episode_name, episode_block)
        quotes.extend(new_quotes)
        if stop_parsing:
            break

    return quotes


def collect_quotes(season_name, episode_name, episode_block):
    quotes = []
    lines = []
    stop_parsing = False

    for element in episode_block.next_siblings:
        # <HR> separates quotes
        if element.name == "hr":
            quotes.append(format_quote(season_name, episode_name, lines))
            lines = []
        else:
            if must_process(element):
                lines.extend(element.text.split("\n"))

        sib = element.next_sibling

        # h3 is the next episode line
        if sib is None or sib.name == "h3":
            break

        # <h2> is the next episode, or another unrelated section
        if sib.name == "h2":
            # if it's followed by the "External Links" or "Cast" sections then we're done with
            # the quotes.
            next_span = sib.find(
                "span", attrs={"id": ["Cast", "External_links"], "class": "mw-headline"}
            )
            if next_span is not None:
                stop_parsing = True

            break

    # Last quote of a section won't be followed by <HR> but we must still collect the quote!
    if lines:
        quotes.append(format_quote(season_name, episode_name, lines))

    return (quotes, stop_parsing)


@click.command()
@click.option(
    "-o", "--output", type=click.File("wb"), metavar="FILENAME", default="-", help="Output filename"
)
@click.argument("name")
def main(output, name):
    title, content = fetch_page(name)
    quotes = parse_page(content)

    for quote in quotes:
        output.write(f"{quote['text']}\n\n".encode("utf-8"))
        output.write(f"\t\"{title}: {quote['episode']}, {quote['season']}\"\n".encode("utf-8"))
        output.write("%\n".encode("utf-8"))

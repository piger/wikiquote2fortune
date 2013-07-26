# -*- coding: utf-8 -*-
import os
import re
import codecs
from optparse import OptionParser
import textwrap
import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


def squeeze_ws(s):
    """Squeeze two ore more whitespaces into one"""
    return re.sub(r'\s{2,}', u' ', s)

def format_quote(season, episode, rows):
    expanded = []

    for row in rows:
        colon = row.find(u':')

        if colon == -1:
            expanded.extend(textwrap.wrap(row))
            expanded.append(u"")
        else:
            indent = colon + 2
            expanded.extend(textwrap.wrap(row, subsequent_indent=u" " * indent))

    text = u'\n'.join(expanded)

    season = squeeze_ws(season)
    episode = squeeze_ws(episode)

    q = {
        'season': season,
        'episode': episode,
        'text': text,
    }
    return q

def scrape(url):
    rv = requests.get(url)
    if rv.status_code != 200:
        print "HTTP Error? %s" % rv
        return []

    rv.encoding = 'utf-8'
    soup = BeautifulSoup(rv.text)

    current_season = None
    current_episode = None
    quotes = []

    for elm in soup.body.next_elements:
        if isinstance(elm, NavigableString):
            continue

        if elm.name == 'h2':
            span = elm.find('span')
            if span:
                current_season = span.string

        elif elm.name == 'h3':
            span = elm.find('span')
            if span and u'mw-headline' in span.attrs.get('class', []):
                current_episode = u' '.join(span.strings)

        elif elm.name == 'dl':
            rows = []

            for row in elm.find_all('dd'):
                text = u' '.join(row.strings)
                text = re.sub(r'^([^:]+) :\s+', u'\\1: ', text)
                rows.append(text)

            quote = format_quote(current_season, current_episode, rows)
            quotes.append(quote)

    return quotes

def main():
    parser = OptionParser()
    parser.add_option('-u', '--url', help="WikiQuotes page URL")
    parser.add_option('-O', '--output', metavar='FILENAME', help="Output filename")
    parser.add_option('-n', '--name', help="Name of Thing")

    (opts, args) = parser.parse_args()
    if not opts.url or not opts.output or not opts.name:
        parser.error("You must specify an URL, a name and an output filename!")
        
    quotes = scrape(opts.url)
    with codecs.open(opts.output, 'w', encoding='utf-8') as fd:
        for quote in quotes:
            fd.write(u"%s\n\n" % quote['text'])
            fd.write(u"\t\"%s: %s, %s\"\n" % (opts.name, quote['episode'], quote['season']))
            fd.write(u"%\n")

if __name__ == '__main__':
    main()

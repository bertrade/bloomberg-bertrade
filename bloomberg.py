#!/usr/bin/env python2.7
import argparse
import json
import random
import sys

from bs4 import BeautifulSoup
from PyWebRunner import WebRunner


def _generate_bloomberg_json(tickers=[], filename=None, export_skipped=False):
    # Read from file
    if filename:
        with open(filename) as tickers_file:
            tickers = tickers_file.read().splitlines()
    skipped_tickers = []
    scraped_tickers = []

    random.shuffle(tickers)
    for ticker in tickers:
        wr = WebRunner(driver='Chrome')
        wr.start()
        wr.go('http://www.bloomberg.com/quote/' + ticker)
        if wr.is_text_on_page('produced no matches'):
            skipped_tickers.append(ticker)
            wr.stop()
            print 'WARNING: Skipping {}, {}.'.format(ticker, 'not found')
            continue
        # was acquired by
        # Ticker Change still gives back info so ignoring that
        if wr.is_text_on_page('Ticker Delisted'):
            skipped_tickers.append(ticker)
            wr.stop()
            print 'WARNING: Skipping {}, {}.'.format(ticker, 'ticker has been delisted')
            continue

        # Ticker found, get HTML scrape that sh*it
        html = wr.get_page_source()
        try:
            scraped_ticker = _scrape_ticker(html)
        except IndexError as error:
            skipped_tickers.append(ticker)
            wr.stop()
            print 'WARNING: Skipping {}, {}.'.format(ticker, str(error))
            continue
        if scraped_ticker:
            scraped_tickers.append(scraped_ticker)
        wr.stop()

    # Export all scraped tickers to json
    with open('/tmp/scraped_tickers.json', 'w') as json_file:
        json.dump(scraped_tickers, json_file)

    # Export skipped to txt and print
    if export_skipped:
        skipped_tickers_file = open('/tmp/skipped_tickers.txt', 'w')
        for ticker in skipped_tickers:
            skipped_tickers_file.write(ticker + '\n')
        print 'Wrote skipped tickers to /tmp/skipped_tickers.txt'
    print 'Skipped tickers: ' + ', '.join(skipped_tickers)


def _scrape_ticker(html):
    soup = BeautifulSoup(html, 'html.parser')

    ticker = soup.find_all('div', class_='ticker')[0].text.strip()
    market = soup.find_all('div', class_='exchange')[0].text.strip()
    name = soup.find_all('h1', class_='name')[0].text.strip()
    sector = soup.find_all('div', text=' Sector ')[0].findNext('div').text.strip()
    industry = soup.find_all('div', text=' Industry ')[0].findNext('div').text.strip()
    sub_industry = soup.find_all('div', text=' Sub-Industry ')[0].findNext('div').text.strip()
    profile = soup.find_all('div', text=' Profile ')[0].findNext('div').text.strip()
    board_members = []
    for board_member in soup.find_all('span', class_='management__name'):
        board_members.append(board_member.text.strip())

    # Calculated stuff like industries combined with sub industries
    industries = [sector, industry, sub_industry]

    scraped = {'ticker': ticker, 'market': market, 'name': name, 'sector': sector,
               'industry': industry, 'sub_industry': sub_industry, 'profile': profile,
               'board_members': board_members, 'industries': industries}

    print 'Scraped: ' + str(scraped)
    return scraped

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('Scrapes Bloomberg for multiple tickers and\
                                                   generates a .json file at /tmp based on a list\
                                                   of tickers.'))
    parser.add_argument('-f', '--file', help='Input text file for tickers (one per line)')
    parser.add_argument('-t', '--tickers', metavar='tickers', type=str, nargs='+',
                        help='Tickers list (eg. "ALSEA*:MM", "AC*:MM")')
    parser.add_argument('--export-skipped', dest='export_skipped', action='store_true',
                        help='Exports skipped tickers to a text file at /tmp')
    args = parser.parse_args()
    if args.file and args.tickers:
        print 'ERROR: You can only use either -f/--file or -t/--tickers, not both.'
        sys.exit(1)
    elif args.tickers:
        _generate_bloomberg_json(tickers=args.tickers, export_skipped=args.export_skipped)
    elif args.file:
        _generate_bloomberg_json(filename=args.file, export_skipped=args.export_skipped)

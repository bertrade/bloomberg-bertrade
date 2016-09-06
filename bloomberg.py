#!/usr/bin/env python2.7
import argparse
import sys

from PyWebRunner import WebRunner


def _generate_bloomberg_json(tickers=[], filename=None, export_skipped=False):
    # Read from file
    if filename:
        with open(filename) as tickers_file:
            tickers = tickers_file.read().splitlines()
    skipped_tickers = []
    for ticker in tickers:
        wr = WebRunner(driver='Chrome')
        wr.start()
        wr.go('http://www.bloomberg.com/quote/' + ticker)
        if wr.is_text_on_page('produced no matches'):
            skipped_tickers.append(ticker)
            print 'WARNING: Skipping ' + ticker + ', not found.'
            wr.stop()
            break
        if wr.is_text_on_page('has changed'):
            skipped_tickers.append(ticker)
            print 'WARNING: Skipping ' + ticker + ', ticker has changed.'
            wr.stop()
            break
        if wr.is_text_on_page('no data available'):
            skipped_tickers.append(ticker)
            print 'WARNING: Skipping ' + ticker + ', ticker exists but no data available.'
            wr.stop()
            break
        # Ticker found, get HTML scrape that sh*it
        wr.stop()
    # Export skipped to txt and print
    if export_skipped:
        skipped_tickers_file = open('/tmp/skipped_tickers.txt', 'w')
        for ticker in skipped_tickers:
            skipped_tickers_file.write(ticker + '\n')
        print 'Wrote skipped tickers to /tmp/skipped_tickers.txt'

    print 'Skipped tickers: ' + ', '.join(skipped_tickers)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('Scrapes Bloomberg and generates a .json file for\
                                                   Bertade config based on a list of tickers.'))
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

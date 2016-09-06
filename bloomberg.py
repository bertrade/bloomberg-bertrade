import argparse
import sys

from PyWebRunner import WebRunner


def _generate_bloomberg_json(tickers=[], filename=None):
    # Read from file
    if filename:
        with open(filename) as tickers_file:
            tickers = tickers_file.read().splitlines()
    tickers_not_found = []
    for ticker in tickers:
        wr = WebRunner(driver='Chrome')
        wr.start()
        wr.go('http://www.bloomberg.com/quote/' + ticker)
        if wr.is_text_on_page('produced no matches'):
            tickers_not_found.append(ticker)
            print 'WARNING: Skipping ' + ticker + ', not found.'
            wr.stop()
        # Ticker found, get HTML scrape that sh*it
        wr.stop()
    print 'Skipped tickers (not found): ' + tickers_not_found

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('Scrapes Bloomberg and generates a .json file for\
                                                   Bertade config based on a list of tickers.'))
    parser.add_argument('-f', '--file')
    parser.add_argument('-t', '--tickers', metavar='tickers', type=str, nargs='+',
                        help='The tickers (eg. ALSEA*:MM, AC*:MM)')
    args = parser.parse_args()
    if args.file and args.tickers:
        print 'ERROR: You can only use either FILE or TICKERS, not both.'
        sys.exit(1)
    elif args.tickers:
        _generate_bloomberg_json(tickers=args.tickers)
    elif args.file:
        _generate_bloomberg_json(filename=args.file)

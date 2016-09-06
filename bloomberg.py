import argparse

from PyWebRunner import WebRunner


def _generate_bloomberg_json(tickers):
    for ticker in tickers:
        print ticker
        wr = WebRunner(driver='Chrome')
        wr.start()
        wr.go('http://www.bloomberg.com/quote/' + ticker)
        wr.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('Scrapes Bloomberg and generates a .json file for\
                                                   Bertade config based on a list of tickers.'))
    parser.add_argument('tickers', metavar='tickers', type=str, nargs='+',
                        help='The tickers (eg. ALSEA*:MM, AC*:MM)')
    args = parser.parse_args()
    _generate_bloomberg_json(args.tickers)

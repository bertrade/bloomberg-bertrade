# bloomberg-bertrade

Scrapes Bloomberg and generates a .json file for Bertade config based on a list of tickers.

Setup for mac:

```
brew install chromedriver
virtualenv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python bloomberg.py
```

Example for Mexican Stock Exchange (only two stocks):

`./venv/bin/python bloomberg.py "ALSEA*:MM" "AC*:MM"`

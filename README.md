# RSS Feed Fetcher

This project is a Python script that fetches and processes RSS feeds, filters entries from the last 24 hours, and writes the results to an output file.

## Features

- Reads RSS feed URLs from a configuration file (`fetch.cfg`).
- Fetches and parses RSS feed content.
- Filters feed entries published within the last 24 hours.
- Normalizes text in feed titles to handle encoding issues.
- Cleans URLs by removing query strings (like UTM parameters).
- Outputs the filtered feed entries to a file (`fetch.out`) and prints them to the console.

## Configuration

The script reads RSS feed sources from `fetch.cfg`. Each line in this file should define a feed source in the following format:

```
[Source Name][Source URL]
```

Lines starting with `#` are treated as comments and ignored.

## Requirements

The project requires the following Python packages:

- `feedparser==6.0.11`
- `sgmllib3k==1.0.0`

## Installation

1. Clone this repository or download the script.
2. Install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
# RSS Feed Fetcher

This project is a Python script that fetches and processes RSS feeds, filters entries from the last 24 hours, and writes the results to an output file.

## Features

- Reads RSS feed URLs from a configuration file (`fetch.cfg`).
- Fetches and parses RSS feed content.
- Filters feed entries published within the last 24 hours.
- Outputs the filtered feed entries to a file (`fetch.out`).

## Requirements

The project requires the following Python packages:

- `feedparser==6.0.11`
- `sgmllib3k==1.0.0`

## Installation

1. Clone this repository or download the script.
2. Install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
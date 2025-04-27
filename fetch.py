import os
import feedparser
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlunparse
import unicodedata  # For text normalization
from IPython.display import display
from ftfy import fix_text

def normalize_text(text):
    """
    Normalizes text to fix encoding issues and ensure proper Unicode formatting.
    """
    # Use ftfy to fix encoding issues
    text = fix_text(text)

    # Normalize Unicode to NFC (Canonical Composition)
    return unicodedata.normalize('NFC', text)

def read_feeds(file_path):
    """
    Reads RSS feed names and URLs from a file in the format [source name][source url].
    """
    feeds = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):  # Ignore empty lines and comments
                    if line.startswith("[") and line.endswith("]"):
                        # Adjust parsing logic to handle space between brackets
                        parts = line.split("] [")  # Split by "] ["
                        if len(parts) == 2:
                            name = parts[0][1:]  # Remove leading "["
                            url = parts[1][:-1]  # Remove trailing "]"
                            feeds[name.strip()] = url.strip()
                        else:
                            print(f"Error: Invalid format in line: {line}")
                    else:
                        print(f"Error: Invalid format in line: {line}")
        return feeds
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return {}


def fetch_feed_content(feed_url):
    """
    Fetches and parses the content of an RSS feed.
    """
    feed = feedparser.parse(feed_url)
    if feed.bozo:
        print(f"Error parsing feed: {feed_url}")
        return None
    return feed


def filter_feed_entries(feed, time_range_start):
    """
    Filters feed entries published after the given time range start.
    """
    filtered_entries = []
    for entry in feed.entries:
        if hasattr(entry, 'published_parsed'):
            entry_time = datetime(*entry.published_parsed[:6])
        elif hasattr(entry, 'updated_parsed'):
            entry_time = datetime(*entry.updated_parsed[:6])
        else:
            continue  # Skip entries without timestamps

        if entry_time >= time_range_start:
            filtered_entries.append(entry)
    return filtered_entries


def display_feed(name, feed, output_file):
    """
    Writes the feed title and entries to the output file, filtered by the last 24 hours.
    """
    if feed:
        now = datetime.now()
        twenty_four_hours_ago = now - timedelta(hours=24)

        filtered_entries = filter_feed_entries(feed, twenty_four_hours_ago)

        if filtered_entries:
            for entry in filtered_entries:
                # Normalize the title to fix encoding issues
                normalized_title = normalize_text(entry.title)
                # Remove the query string (UTM parameters) from the link
                parsed_url = urlparse(entry.link)
                cleaned_url = urlunparse(parsed_url._replace(query=""))
                #pub_date = getattr(entry, 'pubDate', 'N/A')  # Use 'N/A' if pubDate is missing
                description = getattr(entry, 'description', 'N/A')  # Use 'N/A' if description is missing
                #write to fetch.out
                output_file.write(f"{normalized_title} | {cleaned_url}\n")
                #write to STDOUT
                #display(Markdown("[{normalized_title}]({cleaned_url})"))
                #display(Markdown("_{description}_"))
                print(f"[{normalized_title}]({cleaned_url})")
                print(f"_{description}_\n")
        else:
            output_file.write(f"No recent entries for {name}.\n")
    else:
        output_file.write(f"No feed content to display for {name}.\n")


def main():
    feeds_file = 'fetch.cfg'
    output_file_path = 'fetch.out'

    feeds = read_feeds(feeds_file)

    if not feeds:
        print("No feeds to process.")
        return

    with open(output_file_path, 'w', encoding='utf-8') as output_file: 

        for name, url in feeds.items():
            print(f"\n\nFetching feed: {name} ({url})\n")
            feed = fetch_feed_content(url)
            display_feed(name, feed, output_file)


if __name__ == "__main__":
    main()

# Scrap Law

This project scrapes a website for PDF documents and downloads them. It also includes a scheduler to run the scraping process periodically.

## Features

- Scrapes PDF links from a specified website.
- Downloads PDFs and saves them locally.
- Stores metadata about downloaded PDFs in a SQLite database.
- Schedules the scraping process to run every 7 days.

## Requirements

- Python 3.11
- `requests`
- `beautifulsoup4`
- `schedule`
- `tqdm`
- `sqlite3` (part of the Python standard library)

## Installation

1. Clone the repository:
    
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
    ```sh
    git clone git@github.com:ShahbazShaddy/Scrap-Law.git
    cd Scrap-Law
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the `main.py` script to start the scraping and scheduling process:
```sh
python main.py
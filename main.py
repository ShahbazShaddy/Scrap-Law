import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from database import is_pdf_downloaded, add_pdf_record, count_pdfs, initialize_db
from tqdm import tqdm  # Add tqdm for progress bar
import schedule
import time

BASE_URL = "https://www.pakistancode.gov.pk/english/sHyuRiF.php"
PDF_DIR = Path("PDF")

def fetch_pdf_links(section_url):
    response = requests.get(section_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the iframe containing the PDF
    iframe = soup.find('iframe')
    if iframe and 'src' in iframe.attrs:
        relative_pdf_url = iframe['src']
        # Remove "ViewerJS/#" from the path if it exists
        cleaned_pdf_url = relative_pdf_url.replace("ViewerJS/#", "").replace("../", "/")

        # Check if the URL is absolute
        if cleaned_pdf_url.startswith("http"):
            pdf_url = cleaned_pdf_url  # Use the absolute URL as-is
        else:
            pdf_url = BASE_URL + cleaned_pdf_url  # Construct the full URL for relative paths

        return pdf_url
    return None

def scrape_and_download_pdfs():
    """Scrapes the website, navigates links, and downloads new PDFs."""
    PDF_DIR.mkdir(exist_ok=True)
    downloaded_count = 0
    
    while True:
        # Fetch the base page content
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all sections
        sections = soup.select(".accordion-section-title")

        # Process each law section one by one
        for section in tqdm(sections, desc="Downloading PDFs"):
            # Locate the nested <a> tag
            link_element = section.find("a")
            if not link_element or not link_element.get("href"):
                continue

            section_url = link_element['href']
            if not section_url.startswith("http"):
                section_url = f"https://www.pakistancode.gov.pk/english/{section_url}#download"

            try:
                # Fetch the PDF link using the fetch_pdf_links function
                pdf_url = fetch_pdf_links(section_url)
                if not pdf_url:
                    continue

                pdf_name = os.path.basename(pdf_url)

                # Skip if PDF is already downloaded
                if is_pdf_downloaded(pdf_name):
                    continue

                # Download the PDF
                pdf_path = PDF_DIR / pdf_name
                pdf_content = requests.get(pdf_url).content
                with open(pdf_path, "wb") as pdf_file:
                    pdf_file.write(pdf_content)
                downloaded_count += 1

                # Add to database
                add_pdf_record(pdf_name, pdf_url)

            except requests.RequestException as e:
                continue

        break  # Exit the loop after processing all sections

    print(f"Total PDFs downloaded: {downloaded_count}")

def job():
    print("Running scheduled scraping...")
    scrape_and_download_pdfs()

def start_scheduler():
    schedule.every(7).days.do(job)
    print("Scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Call the function
if __name__ == "__main__":
    initialize_db()  # Initialize the database
    scrape_and_download_pdfs()
    start_scheduler()

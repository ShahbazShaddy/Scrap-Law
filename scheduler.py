import schedule
import time
from main import scrape_and_download_pdfs
from database import initialize_db  # Import initialize_db

def job():
    print("Running scheduled scraping...")
    scrape_and_download_pdfs()

def start_scheduler():
    initialize_db()  # Initialize the database
    schedule.every(7).days.do(job)
    print("Scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Call the function
if __name__ == "__main__":
    start_scheduler()

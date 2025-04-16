import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import datetime

# Logging setup
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def scrape_jobs():
    print("🚀 Starting scraping process...")
    url = "https://vacancymail.co.zw/jobs/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Job cards might have a different class depending on the site structure
        job_cards = soup.select(".job-listing")

        if not job_cards:
            print("❌ No job listings found.")
            logging.warning("No job listings found on the page.")
            return

        job_data = []

        for job in job_cards[:10]:  # Limit to 10 most recent jobs
            title = job.select_one(".job-listing-title")
            company = job.select_one(".job-listing-company")
            location = job.select_one(".icon-material-outline-location-on")
            expiry = job.select_one(".icon-material-outline-access-time")
            description = job.select_one(".job-listing-text")

            job_data.append({
                "Title": title.text.strip() if title else "N/A",
                "Company": company.text.strip() if company else "N/A",
                "Location": location.find_next('li').text.strip() if location else "N/A",
                "Expiry Date": expiry.find_next('li').text.strip() if expiry else "N/A",
                "Description": description.text.strip() if description else "N/A"
            })

        df = pd.DataFrame(job_data)
        df.drop_duplicates(inplace=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"scraped_data_{timestamp}.csv"
        df.to_csv(file_name, index=False)

        print(f"✅ Scraping completed! Data saved to '{file_name}'")
        logging.info(f"Scraping completed. {len(df)} jobs saved to {file_name}")

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Request error: {e}")
        print(f"❌ Request error: {e}")

    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        print(f"❌ An unexpected error occurred: {e}")

# ✅ Entry point
if __name__ == "__main__":
    scrape_jobs()



import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import logging
import random
import time

# ==========================
# LOGGING
# ==========================
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)"
]


# ==========================
# FETCH PAGE
# ==========================
def fetch_page(url):

    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }

    for attempt in range(3):

        try:

            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            logging.info(f"Success: {url}")

            return response.text

        except Exception as e:

            logging.error(
                f"Attempt {attempt+1} Failed: {e}"
            )

            time.sleep(2)

    return None


# ==========================
# PARSE HTML
# ==========================
def parse_html(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    results = []

    links = soup.find_all("a")

    for link in links:

        title = link.get_text(strip=True)
        href = link.get("href")

        if title and href:

            results.append({
                "Title": title,
                "Link": href
            })

    return results


# ==========================
# SAVE JSON
# ==========================
def save_json(data):

    with open(
        "output.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================
# SAVE CSV
# ==========================
def save_csv(data):

    df = pd.DataFrame(data)

    df.to_csv(
        "output.csv",
        index=False
    )


# ==========================
# MAIN PROGRAM
# ==========================
def main():

    url = input(
        "Enter Website URL: "
    )

    html = fetch_page(url)

    if html is None:

        print("Could not fetch website.")
        return

    data = parse_html(html)

    save_json(data)
    save_csv(data)

    print("\n========================")
    print("SCRAPING COMPLETED")
    print("========================")
    print(f"Records Found: {len(data)}")
    print("Saved: output.json")
    print("Saved: output.csv")
    print("Log File: scraper.log")


if __name__ == "__main__":
    main()
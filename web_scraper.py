
import requests
from bs4 import BeautifulSoup
import csv
import schedule
import time


URL = "http://quotes.toscrape.com"


def scrape_quotes():
    print("Scraping website...")

    response = requests.get(URL)

    if response.status_code != 200:
        print("Failed to retrieve website")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")

    data = []

    for q, a in zip(quotes, authors):
        quote = q.text
        author = a.text
        data.append([quote, author])

    save_to_csv(data)

    print("Scraping completed!")


def save_to_csv(data):
    file_name = "quotes_data.csv"

    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Quote", "Author"])

        writer.writerows(data)

    print("Data saved to CSV file.")


def job():
    scrape_quotes()


def main():
    print("Starting Automated Web Scraper")

    # run immediately
    scrape_quotes()

    # schedule every 1 minute (for demo)
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
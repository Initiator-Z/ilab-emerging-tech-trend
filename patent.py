import requests
from bs4 import BeautifulSoup
import pandas as pd
import feedparser
from urllib.parse import urljoin
from datetime import datetime
from dateutil import parser as date_parser

def extract_category_name(a_tag):
    return a_tag.get_text(strip=True).split(maxsplit=1)[1]

def prepare_patent_data(rss_feed_url, category_names, start_date=None, end_date=None):
    feed = feedparser.parse(rss_feed_url)

    titles = []
    descriptions = []
    pub_dates = []
    categories = []
    links = []

    if start_date:
        start_date = datetime.strptime(str(start_date), "%Y-%m-%d")
    if end_date:
        end_date = datetime.strptime(str(end_date), "%Y-%m-%d")

    for entry in feed.entries:
        entry_date = date_parser.parse(entry.published)

        if (not start_date or entry_date >= start_date) and (not end_date or entry_date <= end_date):
            if entry.description:
                titles.append(entry.title)
                descriptions.append(entry.description)
                pub_dates.append(entry.published)
                categories.append(category_names)
                links.append(entry.link)

    data = {
        "title": titles,
        "description": descriptions,
        "publish_date": pub_dates,
        "category": categories,
        "link": links
    }
    df = pd.DataFrame(data)
    return df

def get_available_categories():
    rss_feed_list_url = "https://www.freepatentsonline.com/rssfeed.html"
    response = requests.get(rss_feed_list_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        span_element = soup.find('span', text="Complete List of all RSS Feeds by Class")

        if span_element:
            container = span_element.find_parent('div', class_='container_white')

            if container:
                rss_links = container.find_all('a')

                available_categories = []

                for index, link in enumerate(rss_links, start=1):
                    category_name = extract_category_name(link)
                    available_categories.append((index, category_name))

                return available_categories
            else:
                print("No container with class 'container_white' found on the page.")
        else:
            print("No span element with text 'Complete List of all RSS Feeds by Class' found on the page.")
    else:
        print("Failed to retrieve the RSS feed list.")

def get_patent_data(start_date, end_date, selected_categories):
    rss_feed_list_url = "https://www.freepatentsonline.com/rssfeed.html"
    response = requests.get(rss_feed_list_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        span_element = soup.find('span', text="Complete List of all RSS Feeds by Class")

        if span_element:
            container = span_element.find_parent('div', class_='container_white')

            if container:
                rss_links = container.find_all('a')

                base_url = "https://www.freepatentsonline.com/"
                available_categories = get_available_categories()

                selected_category_indices = [int(index) - 1 for index in selected_categories.split(',')]

                combined_df = pd.DataFrame()

                for index in selected_category_indices:
                    if 0 <= index < len(rss_links):
                        relative_rss_feed_url = rss_links[index]['href']
                        rss_feed_url = urljoin(base_url, relative_rss_feed_url)
                        category_name = extract_category_name(rss_links[index])

                        df = prepare_patent_data(rss_feed_url, category_name, start_date, end_date)
                        combined_df = pd.concat([combined_df, df], ignore_index=True)

                return combined_df
            else:
                print("No container with class 'container_white' found on the page.")
        else:
            print("No span element with text 'Complete List of all RSS Feeds by Class' found on the page.")
    else:
        print("Failed to retrieve the RSS feed list.")

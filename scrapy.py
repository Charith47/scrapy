from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient

# DATABASE CONNECTION STRING
CONNECTION_STRING = (
    "mongodb+srv://loki:cwdcwd123@cluster0.x7kb8.mongodb.net/scrapy-storage"
)

# URL TO BE SCRAPED
URL = "http://sinhala.adaderana.lk/"


def load_website(url):
    browser = webdriver.Firefox()
    browser.get(url)
    markup = browser.page_source
    browser.quit()
    return markup


def scrape_data(markup):
    # news list
    news_list = []

    # tag check
    whitelist = ["p"]
    soup = BeautifulSoup(markup, "html.parser")

    # itr through markup
    for story in soup.find_all("div", {"class": "story-text"}):
        title = " ".join(str(story.h3.get_text()).split())

        raw_summary = " ".join(
            [p for p in story.find_all(text=True) if p.parent.name in whitelist]
        )

        stripped_summary = " ".join(raw_summary.split())
        # 0 summary length
        if len(stripped_summary) == 0:
            stripped_summary = None

        # get thumbnail of  the story
        # if no image available, set link to None
        thumbnail = story.find("img")
        if not (thumbnail == None):
            # catch exception if src tag does not exist
            try:
                thumbnail_link = thumbnail["src"]
            except:
                thumbnail_link = None
        else:
            thumbnail_link = None

        # get the link for full article
        # if no article, set link to None
        article = story.find("a")
        if not (article == None):
            # catch exception if href tag does not exist
            try:
                article_link = str(article["href"])
                # if it is an embedded link, append site url first
                if article_link.startswith("news", 0, 4):
                    article_link = f"http://sinhala.adaderana.lk/{article_link}"
            except:
                article_link = None
        else:
            article_link = None

        news_list.append(
            {
                "title": title,
                "summary": stripped_summary,
                "thumbnail": thumbnail_link,
                "article": article_link,
            }
        )

    return news_list


def push_to_database(news_list):
    db_client = MongoClient(CONNECTION_STRING)
    db = db_client["scrapy-storage"]
    db_collection = db["scrapy-news"]
    db_collection.insert_many(news_list)


if __name__ == "__main__":
    push_to_database(scrape_data(load_website(URL)))

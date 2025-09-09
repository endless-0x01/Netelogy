from re import A
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout, ReadTimeout, ConnectionError
from fake_headers import Headers
import os
import json

KEYWORDS = ["дизайн", "фото", "web", "python"]
BASE_URS = "https://habr.com/ru/articles/"


def init_session() -> requests.Session:
    session = requests.Session()
    headers = Headers(browser="chrome", os="win", headers=True)
    session.headers.update(headers.generate())
    return session


def get_page(session: requests.Session, url: str) -> requests.Response | None:
    try:
        response = session.get(url)
        response.raise_for_status()
        return response
    except (Timeout, ReadTimeout) as e:
        print(f"Ошибка таймаута: {e}")
        return None
    except ConnectionError as e:
        print(f"Ошбика соединения: {e}")
        return None
    except RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


def checker_keywords_in_text(text: str, keywords=KEYWORDS):
    return any(keyword.lower() in text.lower() for keyword in keywords)


def check_keywords_in_paragraph(article: BeautifulSoup) -> bool:
    if article is None:
        return False
    paragraphs = article.select("p")
    for paragraph in paragraphs:
        if paragraph and checker_keywords_in_text(paragraph.get_text()):
            return True
    return False


def check_keywords_in_title(title: BeautifulSoup) -> bool:
    if title is None:
        return False
    for link in title.select(".tm-publication-hub__link-container"):
        text = link.select_one("span").get_text()
        if checker_keywords_in_text(text):
            return True

    return False


def get_all_links_for_pasrsing(html) -> list:
    soup = BeautifulSoup(html, features="lxml")
    blocks = soup.select(".tm-articles-list__item")
    articles_data = list()
    for block in blocks:
        article = block.select_one(
            ".article-formatted-body.article-formatted-body.article-formatted-body_version-2"
        )
        topic = block.select_one(".tm-title__link span")
        title = block.select_one(".tm-publication-hubs")

        if date := block.select_one("time"):
            title_data = date.get("title")

        if (
            check_keywords_in_paragraph(article)
            or checker_keywords_in_text(topic.get_text())
            or check_keywords_in_title(title)
        ):
            if (link_element := block.select_one(".tm-title__link")) and (
                href := link_element.get("href")
            ):
                articles_data.append(
                    {
                        "time": title_data,
                        "href": "https://habr.com/" + href,
                        "topic": topic.get_text().strip() if topic else "Заголовка нет",
                    }
                )

    return articles_data


def output_in_console(results: list):
    for i, result in enumerate(results, 1):
        print(f"Статья номер {i}")
        print(f"{result['time']}\n{result['href']}\n{result['topic']}")
        print(f"{'*' * 15}\n")


def main():
    session = init_session()

    response = get_page(session, BASE_URS)
    if response:
        print("Страница загружена...")
        if results := get_all_links_for_pasrsing(response.text):

            output_in_console(results)

            script_dir = os.path.dirname(__file__)
            output_path = os.path.join(script_dir, "haber_articles.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

    else:
        print("Ошибка загрузки странницы")


if __name__ == "__main__":
    main()

import random

from bs4 import BeautifulSoup
import requests

from app.utils.cache import Cache

NEWS_KEY_CACHE = "NEWS"
POSTS_KEY_CACHE = "POSTS"
PERM_URL = "https://perm-300.ru"
LINK_POST = "https://vk.com/wall-209972058_"
ACCESS_TOKEN = "19ffc37619ffc37619ffc376641aebb053119ff19ffc3767d7cde9d241d1cac05b960e7"
VERSION = "5.131"
TTL = 10800
ch = Cache()


def get_news() -> list:
    response_news = ch.get(NEWS_KEY_CACHE)
    if response_news is None:
        response_news = parse_news()
        ch.set(NEWS_KEY_CACHE, response_news, TTL)
        return response_news
    return response_news


def get_posts() -> list:
    response_posts = ch.get(POSTS_KEY_CACHE)
    if response_posts is None:
        response_posts = parse_posts()
        ch.set(POSTS_KEY_CACHE, response_posts, TTL)
        return response_posts
    return response_posts


def parse_news() -> list:
    response_news = []
    html_website = requests.get("https://perm-300.ru/afisha/")

    soup = BeautifulSoup(html_website.text, 'lxml')
    a = soup.find_all("a", class_="event eventshadow")[:5]
    for i, value in enumerate(a):
        image = value.find('div', class_='eventimg').get('style').strip('background - image: url').strip('(').strip(')').strip("'")
        response_news.append({
            "link": f"{PERM_URL}{value.get('href')}",
            "date": value.find("div", class_="eventdate").text,
            "title": value.find("div", class_="eventtitle").text.strip(),
            "image": f"{PERM_URL}/{image}",
            "description": value.find("div", class_="shadow").text if value.find("div", class_="shadow") is not None else ""
        })
    return response_news


def parse_posts() -> list:
    posts = []
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': ACCESS_TOKEN,
                                'v': VERSION,
                                'owner_id': -209972058,
                                'offset': 0,
                                'count': random.randint(8, 9),
                                'filter': str('owner')
                            })
    response = response.json()['response']['items'][1:]
    for i, value in enumerate(response):
        if value.get('copy_history', None) is None:
            attachments = [i for i in value['attachments'] if i['type'] == 'photo']
            posts.append({
                'link': f"{LINK_POST}{value.get('id')}",
                'title': value['text'],
                'image': attachments[0]['photo']['sizes'][-1]['url'] if attachments else 'https://sun87-2.userapi.com/impg/gSRrDZqCu0Z5-G-hgoq7ZtWlkeaY5JzsmWlemA/a39zlhKjz0c.jpg?size=640x640&quality=95&sign=59bee6272674ef54dbadce9b81b7442e&type=album',
            })
    return posts


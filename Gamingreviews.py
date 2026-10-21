"""Collect 200 public Ask HN story posts (not comments).

Install: pip install requests beautifulsoup4
Run:     python collect_ask_hn.py
"""
from __future__ import annotations

import csv
import json
import logging
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TARGET_POSTS = 200
MIN_BODY_WORDS = 15  # Set to 0 to include title-only or very short posts.
PAGE_SIZE = 100
MAX_PAGES = 30
REQUEST_DELAY_SECONDS = 0.15
OUTPUT_DIR = Path('ask_hn_data')

ALGOLIA_URL = 'https://hn.algolia.com/api/v1/search_by_date'
HN_ITEM_URL = 'https://hacker-news.firebaseio.com/v0/item/{item_id}.json'

FIELDS = [
    'id', 'title', 'text', 'full_text', 'author', 'score',
    'num_comments', 'created_at', 'word_count', 'url', 'raw_html'
]


def make_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=4,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=['GET'],
        respect_retry_after_header=True,
    )
    session.mount('https://', HTTPAdapter(max_retries=retry))
    session.headers.update({'User-Agent': 'AskHNHomeworkCollector/1.0 (public data, educational)'})
    return session


def get_json(session: requests.Session, url: str, params: dict | None = None) -> Any:
    response = session.get(url, params=params, timeout=20)
    response.raise_for_status()
    return response.json()


def clean_html(value: str | None) -> str:
    if not value:
        return ''
    soup = BeautifulSoup(value, 'html.parser')
    for tag in soup(['script', 'style']):
        tag.decompose()
    text = soup.get_text(separator=' ', strip=True)
    return re.sub(r'\s+', ' ', text).strip()


def count_words(text: str) -> int:
    return len(text.split())


def parse_post(item: dict | None) -> dict | None:
    if not item or item.get('type') != 'story':
        return None
    if item.get('deleted') or item.get('dead'):
        return None

    title = clean_html(item.get('title'))
    # Independently validate Ask HN, rather than trusting the search index alone.
    if not title.casefold().startswith('ask hn:'):
        return None

    raw_html = item.get('text') or ''
    body = clean_html(raw_html)
    if not title or count_words(body) < MIN_BODY_WORDS:
        return None

    item_id = item.get('id')
    timestamp = item.get('time')
    if not isinstance(item_id, int) or not isinstance(timestamp, (int, float)):
        return None

    return {
        'id': item_id,
        'title': title,
        'text': body,
        'full_text': f'{title}\n\n{body}',
        'author': item.get('by', ''),
        'score': item.get('score', 0),
        'num_comments': item.get('descendants', 0),
        'created_at': datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat(),
        'word_count': count_words(body),
        'url': f'https://news.ycombinator.com/item?id={item_id}',
        'raw_html': raw_html,
    }


def collect(session: requests.Session) -> list[dict]:
    posts: list[dict] = []
    seen_ids: set[int] = set()
    seen_texts: set[str] = set()

    for page in range(MAX_PAGES):
        logging.info('Searching page %s ...', page + 1)
        try:
            result = get_json(session, ALGOLIA_URL, {
                'tags': 'ask_hn',
                'hitsPerPage': PAGE_SIZE,
                'page': page,
            })
        except requests.RequestException as exc:
            logging.warning('Could not load search page %s: %s', page, exc)
            continue

        hits = result.get('hits', [])
        if not hits:
            break

        for hit in hits:
            try:
                item_id = int(hit['objectID'])
            except (KeyError, ValueError, TypeError):
                continue
            if item_id in seen_ids:
                continue
            seen_ids.add(item_id)

            try:
                item = get_json(session, HN_ITEM_URL.format(item_id=item_id))
            except (requests.RequestException, ValueError) as exc:
                logging.warning('Skipping item %s: %s', item_id, exc)
                continue

            post = parse_post(item)
            if not post:
                continue

            # Deduplicate identical titles and bodies too.
            normalized = re.sub(r'\s+', ' ', post['full_text']).casefold()
            if normalized in seen_texts:
                continue
            seen_texts.add(normalized)
            posts.append(post)
            if len(posts) % 25 == 0:
                logging.info('Collected %s/%s valid posts', len(posts), TARGET_POSTS)
            if len(posts) >= TARGET_POSTS:
                return posts
            time.sleep(REQUEST_DELAY_SECONDS)

        time.sleep(REQUEST_DELAY_SECONDS)
    return posts


def save(posts: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / 'ask_hn_200_posts.csv'
    json_path = OUTPUT_DIR / 'ask_hn_200_posts.json'

    with csv_path.open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(posts)

    with json_path.open('w', encoding='utf-8') as file:
        json.dump(posts, file, ensure_ascii=False, indent=2)

    logging.info('Saved %d posts to %s and %s', len(posts), csv_path, json_path)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    session = make_session()
    posts = collect(session)
    save(posts)
    if len(posts) < TARGET_POSTS:
        logging.warning('Only %d eligible posts found. Try decreasing MIN_BODY_WORDS or increasing MAX_PAGES.', len(posts))
    else:
        logging.info('Success: collected exactly %d original Ask HN posts.', TARGET_POSTS)


if __name__ == '__main__':
    main()

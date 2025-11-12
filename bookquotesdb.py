import requests
from dotenv import load_dotenv
import os
import re
import difflib
import time

load_dotenv()
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')
file_path = os.getenv('FILE_PATH')


headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

def query_database_for_page(book_name):
    data = {}
    response = requests.post(f'https://api.notion.com/v1/databases/{DATABASE_ID}/query', headers=headers, json=data)
    results = response.json().get('results', [])
    page_titles = [page['properties']['Name']['title'][0]['text']['content'] for page in results if page['properties']['Name']['title']]
    # Find best match
    matches = difflib.get_close_matches(book_name, page_titles, n=1, cutoff=0.6)  # Adjust cutoff for similarity
    if matches:
        for page in results:
            if page['properties']['Name']['title'][0]['text']['content'] == matches[0]:
                return page['id']
    return None

    if results:
        return results[0]['id']  # Return page ID
    return None


def append_quote_to_page(page_id, headline, quote_text):
    children = [
        {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": headline}}]}}
    ]
    # Split quote_text into 2000-char chunks
    for i in range(0, len(quote_text), 2000):
        chunk = quote_text[i:i+2000]
        children.append({
            "object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": chunk}}]}
        })
    data = {"children": children}
    response = requests.patch(f'https://api.notion.com/v1/blocks/{page_id}/children', headers=headers, json=data)
    if response.status_code == 200:
        return True
    else:
        print(f"Error appending: {response.json()}")
        return False

def parse_quotes_md(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    # Split by "--------" and parse each section
    sections = re.split(r'--------', content)
    quotes = []
    for section in sections[1:]:  # Skip first empty
        lines = section.strip().split('\n')
        if len(lines) >= 3:
            book_line = lines[0]
            headline_line = lines[1]
            quote_text = '\n'.join(lines[2:])
            book_name = book_line.replace('Book Name: ', '').strip()
            headline = headline_line.replace('Headline: ', '').strip()
            quotes.append((book_name, headline, quote_text))
    return quotes


def headline_exists(page_id, headline):
    start_cursor = None
    while True:
        params = {'page_size': 100}
        if start_cursor:
            params['start_cursor'] = start_cursor
        response = requests.get(f'https://api.notion.com/v1/blocks/{page_id}/children', headers=headers, params=params)
        if response.status_code != 200:
            return False
        data = response.json()
        blocks = data.get('results', [])
        for block in blocks:
            if block.get('type') == 'heading_3':
                text = block['heading_3']['rich_text']
                if text and text[0]['text']['content'] == headline:
                    return True
        if not data.get('has_more'):
            break
        start_cursor = data.get('next_cursor')
    return False

def main():
    quotes = parse_quotes_md(file_path)
    for book_name, headline, quote_text in quotes:
        page_id = query_database_for_page(book_name)
        if page_id:
            if headline_exists(page_id, headline):
                print(f"Headline '{headline}' already exists for {book_name}, skipping.")
                continue
            if append_quote_to_page(page_id, headline, quote_text):
                print(f"Appended to {book_name}")
            else:
                print(f"Failed to append to {book_name}")
        else:
            print(f"Page not found for {book_name}")
        time.sleep(3)  # Delay to avoid rate limits

if __name__ == "__main__":
    main()

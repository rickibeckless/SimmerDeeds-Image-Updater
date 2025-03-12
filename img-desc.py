import requests
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def update_img(data, new_img_href):
    channel_name = data["channel_name"]
    channel_link = data["channel_link"]
    response = supabase.table("simmers").select("*").eq("url", channel_link).execute()
    
    if response.data:
        row_id = response.data[0]["id"]
        update_response = supabase.table("simmers").update({"image_url": new_img_href}).eq("id", row_id).execute()

        if update_response:
            print(f"'{channel_name}' Image updated successfully.")
    else:
        print("No data found.")

def get_new_img_src(data):
    channel_link = data["channel_link"]

    result = requests.get(channel_link, timeout=10)
    soup = BeautifulSoup(result.text, 'html.parser')
    img_rel = "image_src"
    img = soup.find("link", rel=img_rel)

    if img:
        new_img_href = img.get("href")
        update_img(data, new_img_href)
    else:
        print("No image found with the specified rel attribute.")

def validate_url(card_data):
    for data in card_data:
        img_src = data["img_src"]
        channel_name = data["channel_name"]
        
        try:
            response = requests.get(img_src, timeout=5)
            if response.status_code == 200:
                print(f"'{channel_name}' image exists!")
            else:
                print(f"'{channel_name}' image does not exist or is unreachable.")
                get_new_img_src(data)
        except requests.RequestException:
            print(f"'{channel_name}' image does not exist or is unreachable.")
            get_new_img_src(data)
        print()

def get_dynamic_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        content = page.content()
        browser.close()
        return content

url = "https://simmerdeeds.netlify.app"
html_content = get_dynamic_content(url)

soup = BeautifulSoup(html_content, "html.parser")

card_id = "simmer-card"
cards = soup.find_all("div", id=card_id)
card_data = []

for card in cards:
    img_class = "simmer-card-img"
    link_id = "simmer-card-url"
    header_id = "simmer-card-header"
    name_class = "simmer-card-link"

    img = card.find("img", class_=img_class)
    header = card.find("h2", id=header_id)
    name = header.find("a", id=name_class)
    link = card.find("a", id=link_id)

    img_src = img.get("src", "No src")
    img_alt = img.get("alt", "No alt text")
    channel_name = header.text if header else "No header text"
    channel_link = link.get("href", "No href")

    card_data.append({
        "img_src": img_src,
        "img_alt": img_alt,
        "channel_name": channel_name,
        "channel_link": channel_link
    })

validate_url(card_data)
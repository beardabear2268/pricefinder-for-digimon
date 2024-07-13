  GNU nano 8.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 price.py                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          import requests
from bs4 import BeautifulSoup
import urllib.parse
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO

def get_ebay_search_url(card_id, condition):
    base_url = "https://www.ebay.com/sch/i.html"
    query_params = {
        "_nkw": f"Digimon {card_id} card",
        "rt": "nc"
    }
    if condition:
        query_params["LH_ItemCondition"] = condition
    query = urllib.parse.urlencode(query_params)
    return f"{base_url}?{query}"

def scrape_ebay_prices(card_id, condition):
    url = get_ebay_search_url(card_id, condition)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    prices = []
    images = []

    for item in soup.find_all('div', {'class': 's-item__info'}):
        price_span = item.find('span', {'class': 's-item__price'})
        if price_span:
            price_text = price_span.get_text(strip=True)
            price = price_text.replace('$', '').replace(',', '').split(' ')[0]
            try:
                prices.append(float(price))
            except ValueError:
                continue

        img_tag = item.find('img', {'class': 's-item__image-img'})
        if img_tag and img_tag['src']:
            images.append(img_tag['src'])

    return prices, images

def get_amazon_search_url(card_id):
    base_url = "https://www.amazon.com/s"
    query_params = {"k": f"Digimon {card_id} card"}
    query = urllib.parse.urlencode(query_params)
    return f"{base_url}?{query}"

def scrape_amazon_prices(card_id):
    url = get_amazon_search_url(card_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    prices = []
    images = []

    for item in soup.find_all('span', {'class': 'a-price-whole'}):
        price_text = item.get_text(strip=True)
        price = price_text.replace(',', '').split(' ')[0]
        try:
            prices.append(float(price))
        except ValueError:
            continue

        img_tag = item.find_previous('img')
        if img_tag and img_tag['src']:
            images.append(img_tag['src'])

    return prices, images

def get_tcgplayer_search_url(card_id):
    base_url = "https://www.tcgplayer.com/search"
    query_params = {"q": f"Digimon {card_id}"}
    query = urllib.parse.urlencode(query_params)
    return f"{base_url}?{query}"

def scrape_tcgplayer_prices(card_id):
    url = get_tcgplayer_search_url(card_id)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    prices = []
    images = []

    for item in soup.find_all('span', {'class': 'price'}):
        price_text = item.get_text(strip=True)
        price = price_text.replace('$', '').replace(',', '').split(' ')[0]
        try:
            prices.append(float(price))
        except ValueError:
            continue

        img_tag = item.find_previous('img')
        if img_tag and img_tag['src']:
            images.append(img_tag['src'])

    return prices, images

def calculate_average(prices):
    if prices:
        return sum(prices) / len(prices)
    return 0

def search_prices():
    card_id = card_id_entry.get()
    condition = condition_var.get()

    ebay_prices, ebay_images = scrape_ebay_prices(card_id, condition)
    amazon_prices, amazon_images = scrape_amazon_prices(card_id)
    tcgplayer_prices, tcgplayer_images = scrape_tcgplayer_prices(card_id)

    all_prices = ebay_prices + amazon_prices + tcgplayer_prices
    average_price = calculate_average(all_prices)
    all_images = ebay_images + amazon_images + tcgplayer_images

    result_text.delete(1.0, tk.END)
    if all_prices:
        result_text.insert(tk.END, f"Prices for {card_id}:\n")
        for i, price in enumerate(all_prices):
            result_text.insert(tk.END, f"{i+1}: ${price:.2f}\n")
        result_text.insert(tk.END, f"\nAverage Price: ${average_price:.2f}")
    else:
        result_text.insert(tk.END, f"No prices found for card ID: {card_id}")

    if all_images:
        image_url = all_images[0]
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((200, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        card_image_label.configure(image=img)
        card_image_label.image = img
    else:
        card_image_label.configure(image='')
        card_image_label.image = None

# Set up the GUI
root = tk.Tk()
root.title("Digimon Card Price Finder")

# Card ID entry
tk.Label(root, text="Card ID:").grid(row=0, column=0, sticky=tk.W)
card_id_entry = tk.Entry(root)
card_id_entry.grid(row=0, column=1, padx=10, pady=5)

# Condition dropdown
tk.Label(root, text="Condition:").grid(row=1, column=0, sticky=tk.W)
condition_var = tk.StringVar()
condition_dropdown = ttk.Combobox(root, textvariable=condition_var)
condition_dropdown['values'] = ('', 'New', 'Used')
condition_dropdown.grid(row=1, column=1, padx=10, pady=5)

# Search button
search_button = tk.Button(root, text="Search", command=search_prices)
search_button.grid(row=2, column=0, columnspan=2, pady=10)

# Result text box
result_text = tk.Text(root, height=15, width=50)
result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Card image label
card_image_label = tk.Label(root)
card_image_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()











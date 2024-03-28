import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
  
]

headers = {
    'User-Agent': random.choice(user_agents),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.amazon.in/',
    'Connection': 'keep-alive',
}

scraping_configs =  [

     {#22
        'base_url':  'https://www.amazon.in/s?k=bedding+set&page=3',
        'div_class':'s-image',
        'output_file': 'rehan.xlsx'
    },




    ]

def get_with_retry(url, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException as e:
            pass
        time.sleep(random.uniform(1, 3))
        retries += 1
    return None

for config in scraping_configs:
    base_url = config['base_url']
    div_class = config['div_class']  # Get the specific div class for image elements
    output_file = config['output_file']

    page_number = 1
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Title', 'Image Link'])  # Store title and image links

    while page_number <= 5:  # You can adjust the number of pages to scrape
        try:
            url = base_url + str(page_number)
            print("Scraping page", page_number)

            response = get_with_retry(url)
            print(response)

            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                image_elements = soup.find_all('img', class_=div_class)  # Use the specified div class
                title_elements = soup.find_all('span', class_='a-text-normal')  # Add title elements

                if not image_elements or not title_elements:
                    print(f'No image links or title found on page number {page_number}')
                    break

                for image_element, title_element in zip(image_elements, title_elements):
                    image_link = image_element.get('src')
                    title = title_element.get_text(strip=True)
                    if image_link and title:
                        ws.append([title, image_link])

                headers['User-Agent'] = random.choice(user_agents)
                time.sleep(random.uniform(1, 3))

                page_number += 1
            else:
                print(f'Failed to retrieve page {page_number}.')
                break
        except Exception as e:
            print(e)
            continue

    wb.save(output_file)
    print(f'Data saved to {output_file}')

print("Scraping completed.")

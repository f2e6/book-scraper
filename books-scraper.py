import requests
from bs4 import BeautifulSoup
import os

query = input("Enter a book title: ")
response = requests.get("https://www.gutenberg.org/ebooks/search/?query=" + query)

soup = BeautifulSoup(response.text, "html.parser")

book_titles = soup.find_all("span", class_="title")

book_links = soup.find_all("a", class_="link")

# book_titles = book_titles[4:]
# book_links = book_links[4:]

for i, book_title in enumerate(book_titles):
    print(str(i+1) + ". " + book_title.text)

selected_book = int(input("Enter the number of the book you want to open: "))

if selected_book < 1 or selected_book > len(book_links):
    print("Invalid input")
else:
    selected_url = book_links[selected_book - 1]["href"]
    selected_url = f"https://www.gutenberg.org{selected_url}"
    # use BeautifulSoup to extract the link from the selected URL
    response = requests.get(selected_url)
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find("td", class_="noscreen").text
    file = link.replace(".html.images", ".epub3.images")
   
    response = requests.get(file)
    file = file.replace("3.images", "")
    with open("/tmp/" + file.split("/")[-1], "wb") as f:
        f.write(response.content)

    os.system(f"zathura /tmp/{file.split('/')[-1]}")
    os.remove("/tmp/" + file.split("/")[-1])

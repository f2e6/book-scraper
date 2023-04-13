import requests, os; from bs4 import BeautifulSoup

def get_book_links(query):
    response = requests.get(f"https://www.gutenberg.org/ebooks/search/?query={query}")
    soup = BeautifulSoup(response.text, "html.parser")
    book_links = soup.select(".booklink > a")
    return [(link.select_one(".title").text.strip(), f"https://www.gutenberg.org{link['href']}") for link in book_links]

def download_book(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, "html.parser")
    download_link = soup.select_one(".epub > a")
    if not download_link:
        raise ValueError("The book does not have an EPUB download link.")
    epub_url = download_link["href"].replace(".html.images", ".epub.images")
    epub_filename = epub_url.split("/")[-1]
    response = requests.get(epub_url)
    with open(os.path.join("/tmp", epub_filename), "wb") as f:
        f.write(response.content)
    return epub_filename

def main():
    try:
        query = input("Enter a book title: ")
        book_links = get_book_links(query)
        if not book_links:
            print("No results found.")
            return
        for i, (title, _) in enumerate(book_links, 1):
            print(f"{i}. {title}")
        selected_index = int(input(f"Enter a number between 1 and {len(book_links)} to select a book: "))
        selected_title, selected_url = book_links[selected_index - 1]
        epub_filename = download_book(selected_url)
        os.system(f"zathura /tmp/{epub_filename}")
        os.remove(os.path.join("/tmp", epub_filename))
    except (ValueError, requests.exceptions.RequestException) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

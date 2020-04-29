# To download all the springer books automatically
from subprocess import run
from typing import Optional, List
import os
try:
    import pandas as pd
except ImportError:
    run(['pip', 'install', 'pandas', 'xlrd'])
    import pandas as pd

def download(link: str, title: str, books : set) -> None:
    """
    runs a curl command on a given link
    """
    if title not in books:
        title = title.capitalize()
        print(f"Downloading {title}")
        run(["curl", link, "--ssl-no-revoke", "--output", f"{title}.pdf"])
    return

def get_excel(file : str = "Free+English+textbooks.xlsx", directory : str = "books/") -> Optional[pd.DataFrame]:
    try:
        file = pd.read_excel(directory+file)
        return file
    except FileNotFoundError:
        print("Downloading excel source file")
        run(["curl", "https://resource-cms.springernature.com/springer-cms/rest/v1/content/17858272/data/v4",
            "--ssl-no-revoke", "--output", f"{directory+file}"])
    return pd.read_excel(directory+file)

def get_interest() -> str:
    interests = input("Enter your interests: (separate words with a space)\n").lstrip().split()
    if any(len(string) < 4 for string in interests) or not interests:
        print("Please enter more than 3 chars otherwise I will match too many items")
        return get_interest()
    return "|".join(interests)

def make_dir(dir_name: str = "books") -> str:
    print("Creating a directory for downloaded books")
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    return dir_name

def filter_books(books : pd.DataFrame) -> Optional[List]:
    BASE = r'https://link.springer.com/content/pdf/10.1007%2F'
    books = books[['Book Title', 'DOI URL']]
    books_found = []
    interests = get_interest()
    books_found = books[books['Book Title'].str.lower().str.contains(interests.lower())]
    book_urls = books_found['DOI URL'].apply(lambda string : BASE + string.split('/')[-1]).tolist()
    book_titles = books_found['Book Title'].str.lower().tolist()
    if book_titles:
        print(f"Found {len(book_urls)} books with name containing your subject of interest!")
        [print("\t",book) for book in book_titles]
        return book_urls, book_titles
    print(f"Found 0 book with your interest. Do you want to retry ? (y/n)")
    answer = input()
    if answer in ('n', 'no', 'NO','No'):
        return None, None
    return filter_books(books)

def sneak_peek(books : pd.DataFrame, answer :str = "No") -> None:
    ans = input("Do you want a sneak peek of what titles you can find in the db ? \n")
    if ans in ("y", "yes", "Y", "Yes"):
        print(books.sample(frac=1)["Book Title"].head())
        return sneak_peek(books,answer="y")
    return None

if __name__ == "__main__":
    book_dir = make_dir()
    books = get_excel()
    sneak_peek(books)
    book_urls, book_titles = filter_books(books)
    os.chdir(book_dir)
    already_downloaded = set(os.listdir())
    if book_urls:
        [download(url, title, already_downloaded) for url, title in zip(book_urls, book_titles)]

# To download all the springer books automatically
import pandas as pd
from subprocess import run
from typing import Optional, List, Callable
from multiprocessing import Pool, cpu_count
import os

def download(link: str, title: str) -> None:
    """
    runs a curl command on a given link
    """
    run(["curl", link, "--ssl-no-revoke", "--output", f"{title}.pdf"])
    return

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

def filter_books(excel_file : str = "Free+English+textbooks.xlsx") -> Optional[List]:
    BASE = r'https://link.springer.com/content/pdf/10.1007%2F'
    books = pd.read_excel(excel_file)
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
    print(f"Found 0 book with your interest. Do you want to retry ? (y/n)\n")
    answer = input()
    if answer in ('n', 'no', 'NO','No'):
        return None
    return filter_books()

def sneak_peek(excel_file : str = "Free+English+textbooks.xlsx", answer :str = "No") -> None:
    books = pd.read_excel(excel_file)
    ans = input("Do you want a sneak peek of what titles you can find in the db ? \n")
    if ans in ("y", "yes", "Y", "Yes"):
        print(books.sample(frac=1)["Book Title"].head())
        return sneak_peek(answer="y")
    return None

if __name__ == "__main__":
    book_dir = make_dir()
    sneak_peek()
    book_urls, book_titles = filter_books()
    os.chdir(book_dir)
    if book_urls:
        list(map(download, book_urls, book_titles))

# me likey
# python logic math econ dynamic mechanic quant data linear game bayes robot deep neural stat program relativity equation
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    f = open(filename)
    file = f.read() 
    soup = BeautifulSoup(file, "html.parser")
    books = soup.find_all('tr', itemtype ='http://schema.org/Book' ) # is this right? make sure it encompasses the author
    l=[]
    for book in books:
        title = book.find('a').get('title')
        author = book.find('a', class_="authorName").text
        l.append((title,author))
    return l


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".
    

    """
    url = 'https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    urls = soup.find_all('a', class_ = 'bookTitle')
    urls = urls.get('href', None)[:10]

    urls2 =[]
    for url in urls:
        urls2.append("https://www.goodreads.com"+url)
    print(urls)
    return urls2


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    r = requests.get(book_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find('h1',class_ = "gr-h1 gr-h1--serif" ).text 
    title = title.strip()
    author = soup.find('a', class_ = 'authorName').text
    pagenums= soup.find('a', itemprop= 'numberOfPages').text
    pagenums=int(pagenums.strip(" pages"))
    return (title,author,pagenums)


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    f = open(filepath, 'r')
    file = f.read() 
    soup = BeautifulSoup(file, 'html.parser')
    bestbooks = soup.find_all('div', class_="category clearFix")
    tuplelist=[]
    for book in bestbooks:
        category = book.find('h4', class_ = 'category_copy').text
        title = book.find('img', class_ = alt)
        url = book.find('a',class_='href')
        tuplelist.append((category, title, url))

    return tuplelist


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......
    This function should not return anything.
    """
    headers = "Book title", "Author Name"
    with open(filename,'w') as file:
            csv_writer = csv.writer(file, delimiter=',', quotechar = '"')
            csv_writer.writerow(headers) 
            for row in data:
                csv_writer.writerow(row)


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    self.search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titles = get_titles_from_search_results('search_results.htm')
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles), 20)
        # check that the variable you saved after calling the function is a list
        self.assertTrue(type(titles)== list)
        # check that each item in the list is a tuple
        for title in titles:
                self.assertTrue(type(title) == tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(titles[0], ("Harry Potter and the Deathly Hallows", 'J.K. Rowling')
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(titles[-1][0], 'Harry Potter: The Prequel')
   
   def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertTrue(type(self.search_urls)== list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertTrue(len(self.search_urls)== 10)
        # check that each URL in the TestCases.search_urls is a string
        for url in self.search_urls:
            self.assertTrue(type(url)==str)
            self.assertTrue("https://www.goodreads.com/book/show/" in url)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/



    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []
        # for each URL in TestCases.search_urls (should be a list of tuples)
        for url in self.search_urls:
            result = get_book_summary(url)
            summaries.append(result)
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries),10)
            # check that each item in the list is a tuple
        for summary in summaries:
            self.assertTrue(type(summary)==tuple)
            # check that each tuple has 3 elements
            self.assertTrue(len(summary)==3)
            # check that the first two elements in the tuple are string
            self.assertTrue(type(summary[0])=type(summary[1])==str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertTrue(type(summary[2])==int)
            # check that the first book in the search has 337 pages
        self.assertTrue(summaries[0][2], 337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        bestbooks = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(bestbooks), 20)
            # assert each item in the list of best books is a tuple
        for book in bestbooks:
            self.assertTrue(type(book)== tuple)
            # check that each tuple has a length of 3
            self.assertTrue(len(book)==3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(bestbooks[0]==('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020') )
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(bestbooks[-1] ==('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        titles = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        csvdata = write_csv(titles, 'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        csv_lines = csvdata.realines()

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0],"Book title,Author Name" )
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        line = 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1],line)
        last_line = 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1], last_line)


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)




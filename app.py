from flask import Flask, render_template
import requests
import random

app = Flask(__name__)

@app.route("/books")
def books():

    # the app randomly chooses between swedish or english
    random_language = random.choice(["en", "sv"])
    
    # the app is reaching all books in the chosen language 
    api_url = f"https://gutendex.com/books?languages={random_language}"
    response = requests.get(api_url)

    # if the api is responsive
    if response.status_code == 200:

        #getting the full response from a webpage
        books = response.json()

        #we are extracting the amount of books in a certain language.
        book_amount = books.get('count')

        #we are choosing a random index 
        random_index = random.randint(0, book_amount)
        print(random_index)

        '''there are 32 books on each page, so we are calculating what page to land on.
        this could be seen as an overkill, as we could have hard-coded the page numbers.
        but this makes the app more versitile - we could add more languages on the top of the page
        without having to change any code.'''
        page=random_index//32

        #accessing the new url
        api_url = f"https://gutendex.com/books?languages={random_language}&page={page-1}"
        response = requests.get(api_url)
        books = response.json()

        #creating a random index
        random_number = random.randint(0, 32)

        #accessing a book of that index 
        random_book = books['results'][random_number]
        
        #getting the info about a book
        title = random_book['title']
        author = random_book['authors'][0]['name']
        downloads_number = random_book['download_count']
        read_link = random_book['formats']['text/html']
        cover = random_book['formats']['image/jpeg']

        

    else:
        title = "Boken misslyckades med att laddas!"

    return render_template('books.html', title=title, author=author, downloads_number=downloads_number, read_link=read_link, cover=cover)

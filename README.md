# Book Scraper

*This project was completed as part of my Python Application Developer training at OpenClassrooms.*  
*Project 2/13.* 

This is a Python script that scrapes book data from the website [books.toscrape.com](http://books.toscrape.com/).  
It allows the user to choose between scraping a single book, a category of books, or the entire website.  
The script provides feedback in the console to indicate the start and end of the scraping process, as well as the time taken to complete the task.


## Installation

To use this script, you will need to have Python 3 installed on your system.  
Then you will have to clone this repository where you want on your system:
 ```
 git clone https://github.com/Arnaud-Goguelin/OCPy_Projet2_Scraping.git
 ```
 Enter 'OCPy_Projet2_Scraping' folder, then 'repo' folder.
 Create your virtual environnement:
 ```python
     python -m venv my_env
 ```
 And activate it:
 ```python
 # On Windows
 my_env\\scripts\\activate.bat

 # On macOS and Linux
 source my_env/bin/activate
 ```
You will also need to install the following dependencies:

- beautifulsoup4
- black
- requests
- wget

You can use the followwing command in your virtual environnement to install them with the same versions:
```python
pip install -r requirements.txt
```

## Usage

To run the script, simply execute the `main.py` file with the following command:
```python
python main.py
```
You will be prompted to choose between scraping a single book, a category of books, or the entire website
If you choose to scrape a single book or a category, you will be prompted to enter the URL of the book or category.

The script will then begin scraping the data and provide feedback in the console. Once the scraping process is complete, the data will be exported to a CSV file:
- 'one_book.csv' for a single book scraping
- 'books_from_category.csv' for a single category scraping
- 'books_from_website.csv' for the entire website scraping

Images will be download and register as follow:
```
    |-- repo  
        |-- images  
            |-- category_name  
                |-- x_book_title.jpg : where x is the index of the book in the category  
```
Only the first 25 characters are used to create the name of the file.

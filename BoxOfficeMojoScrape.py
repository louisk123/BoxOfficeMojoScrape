"""This file contains
License: The MIT License (MIT)
Copyright (c) 2015 Brian Eujin Kim (http://briank.im)

Dependencies:
Must have BeautifulSoup4 installed
For use with Python 2.7 (untested in Python 3)
"""

import urllib2
from bs4 import BeautifulSoup
import string
from datetime import datetime
import re


def get_all_movies():
    """ returns all the movie urls from boxofficemojo.com in a list"""

    # Alphabet loop for how movies are indexed including
    # movies that start with a special character or number
    index = ["NUM"] + list(string.ascii_uppercase)

    # List of movie urls
    movies_list = []

    # Loop through the pages for each letter
    for letter in index:

        # Loop through the pages within each letter
        for num in range(1, 20):
            url = ("http://www.boxofficemojo.com/movies/alphabetical.htm?"
                   "letter=" + letter + "&page=" + str(num))
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
            rows = soup.find(id="body").find("table").find("table").find_all("table")[1].find_all("tr")

            # skip index row
            if len(rows) > 1:
                counter = 1
                for row in rows:

                    # skip index row
                    if counter > 1:
                        link = row.td.font.a['href']

                        # don't add duplicates
                        if link not in movies_list:
                            movies_list.append(link)

                    counter += 1

    return movies_list


def get_genres(soup):
    """ returns all genres from specific movie page at boxofficemojo.com"""
    genres_list = []
    try:
        genres = soup.find(id="body").find(text=re.compile("Genres"))
        genres = genres.findParent().findNextSibling().find_all('tr')
        genre_count = 0
        for genre in genres:
            if genre_count > 0:
                genres_list.append(genre.td.font.a.text)
            genre_count += 1
    except LookupError:
        try:
            genres = soup.find(id="body").find(text=re.compile("Genre"))
            genres = genres.findNextSibling().text
            genres_list.append(genres)
        except:
            genres_list.append("N/A")
    return genres_list


def get_title(soup):
    """returns title from specific movie page at boxofficemojo.com"""
    try:
        title = soup.find("title").text.rsplit('(', 1)[0].strip()
    except LookupError:
        title = "N/A"
    return title


def get_release_date(soup):
    """returns datetime value of release date from specific movie
    page at boxofficemojo.com
    """
    try:
        date = soup.find(id="body").find(text=re.compile("Release Date"))
        date = date.findNextSibling().text
        date = datetime.strptime(date, "%B %d, %Y")
        return date
    except LookupError:
        return "N/A"


def get_distributor(soup):
    """returns movie distributor from specific movie page at boxofficemojo.com"""
    try:
        distributor = soup.find(id="body").find(text=re.compile("Distributor"))
        distributor = distributor.findNextSibling().text
        return distributor
    except LookupError:
        return "N/A"


def get_rating(soup):
    """returns MPAA Rating from specific movie page at boxofficemojo.com"""
    try:
        rating = soup.find(id="body").find(text=re.compile("MPAA Rating"))
        rating = rating.findNextSibling().text
        return rating
    except LookupError:
        return "N/A"


def get_runtime(soup):
    """returns integer value of runtime from specific movie page at boxofficemojo.com"""
    try:
        runtime = soup.find(id="body").find(text=re.compile("Runtime"))
        runtime = runtime.findNextSibling().text
        time_splits = runtime.split("hrs.")
        try:
            hrs = int(time_splits[0]) * 60
        except LookupError:
            hrs = 0
        mins = int(time_splits[1].split(" min.")[0].strip())
        total = hrs + mins
        return total
    except LookupError:
        return "N/A"


def get_budget(soup):
    """returns movie budget from specific movie page at boxofficemojo.com"""
    try:
        budget = soup.find(id="body").find(text=re.compile("Production Budget"))
        budget = budget.findNextSibling().text
        if budget != "N/A":
            budget = int(budget.split("million")[0].split("$")[1].strip()) * 1000000
        return budget
    except LookupError:
        return "N/A"


def get_domestic_gross(soup):
    """returns integer value of domestic gross from specific movie page at boxofficemojo.com"""
    try:
        gross = soup.find(id="body").find(text=re.compile("Domestic Total Gross: "))
        gross = gross.findNextSibling().text
        gross = int(gross.replace("$", "").replace(",", ""))
        return gross
    except LookupError:
        try:
            gross = soup.find(id="body").find(tex=re.compile("Domestic:"))
            gross = gross.findParent().findNextSibling().text
            return gross
        except:
            return "N/A"


def scrape_movie_data(movie_list, start=0, end=20000):
    """returns dictionary of movies and relevant data from boxofficemojo.com:
    genres(as a list), release date, distributor, runtime, MPAA rating,
    budget, gross domestic revenue
    """
    movie_data_list = {}
    counter = 0
    for movie in movie_list:
        if start < counter < end and counter < len(movie_list):
            url = "http://www.boxofficemojo.com/" + movie
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
            movie_data_list[get_title(soup)] = [
                get_genres(soup), get_release_date(soup),
                get_distributor(soup), get_runtime(soup),
                get_rating(soup), get_budget(soup), get_domestic_gross(soup)
            ]
        counter += 1
    return movie_data_list


def main():
    pass

if __name__ == "__main__":
    main()
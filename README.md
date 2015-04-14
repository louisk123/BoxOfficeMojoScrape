# BoxOfficeMojoScrape
Module to scrape boxofficemojo.com

This module basically does a simple scrape of movies at boxofficemojo.com.

The function get_all_movies() will return a list of all the unique url slugs for all the movies on the site.

The function scrape_movie_data(list_of_movies, starting_point, ending_point) will return a dictionary where they keys are movie names and the values are the relevant data which include: genres(as a list), release date, distributor, runtime, MPAA rating, budget, and gross domestic revenue. The function takes 3 variables but only requires the first one. If you don't need the full set of data, you can specify what range of movies you want to use. If starting_point or ending_point are not defined, it will scrape the whole list.

An update will be added shortly that will let you specify a list of the top movies to scrape.

*Updated on April 14th, 2015

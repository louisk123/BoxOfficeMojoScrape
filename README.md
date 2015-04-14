# BoxOfficeMojoScrape
Module to scrape boxofficemojo.com

This module basically does a simple scrape of movies at boxofficemojo.com.

The function get_all_movies() will return a list of all the unique url slugs for all the movies on the site.

The function scrape_movie_data() will return a dictionary where they keys are movie names and the values are the relevant data which include: genres(as a list), release date, distributor, runtime, MPAA rating, budget, and gross domestic revenue.

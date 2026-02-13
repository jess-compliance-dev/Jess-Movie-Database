# 🎥 Jess' Movie Database

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Features](#features)
* [Project Purpose](#project-purpose)
* [Setup](#setup)


## General info
🎥 A Python application for managing and displaying a personal movie database. You can add, delete, search, and sort movies by rating. The program connects to the OMDb API (movie database) and can also generate a simple website showcasing all movies.

## Technologies
Project is created with:
* Python version: 3.14
*[SQLite](https://www.sqlite.org/) (built into Python)
- Python packages:
  - `sqlalchemy`
  - `requests`
  - `python-dotenv`

## Features
* List all movies with detailed info (title, rating, year, director, actors)
* Add and delete, 
* Search movies 
* View statistics: average, median, highest, lowest ratings, best/worst movies
* Get a random movie recommendation
* Filter movies by minimum rating, start year, and end year
* Sort movies by rating
* Color-coded console output for readability
* Generating a website of database

## Project Purpose
This project is designed as a learning tool for Python developers to practice:
- CRD operations (Create, Read, Delete)
- Handling local data storage
- Working with console-based user interfaces
- Implementing menu-driven programs
- Managing program state and data validation
- Practicing modular Python coding and clean structure


## Setup
Clone the repository and ensure Python is installed:

```bash
$ git clone https://github.com/yourusername/movie-database.git
$ cd my-movie-database
````

Check Python version:
```bash
$ python --version
Python 3.14
````

Intall dependencies
```bash
pip install sqlalchemy requests python-dotenv
```

Create a .env file in the project root and add your OMDb API key
```bash
OMDB_API_KEY=your_api_key_here
```

Run the program:
```bash
$ python main.py

Choose an option from the menu:
0 – Exit
1 – List movies
2 – Add movie
3 – Delete movie
4 – Statistics
5 – Random movie
6 – Search movie
7 – Movies sorted by rating
8 – Filter movies
9 – Generating website


Example: Adding a movie

Enter movie title: Inception
Enter movie rating (0-10, leave empty if unknown): 8.8
Enter release year (leave empty if unknown): 2010
Enter director (leave empty if unknown): Christopher Nolan
Enter main actors (leave empty if unknown): Leonardo DiCaprio, Joseph Gordon-Levitt
Movie 'Inception' successfully added.
```



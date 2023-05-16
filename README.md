# HeelFuel Backend

## Background

- HeelFuel Backend is the complete backend of the HeelFuel Application. As UNC's dining hall didn't have any data on the nutritional factors of each food, we developed our program to web scrape and gathered the data neatly, which we then uploaded to a database to create a custom API. This program uses selenium, BeautifulSoup, multithreading, and Firebase.


## Description

- This backend scrapes data from UNC's dining hall website by launching each item into a new page, then web scraping that page in the background before closing it. The program utilizes multithreading, which reduces the time it takes to scrape the data. However, it uses a lot of memory due to using Chrome, so avoid running it in parallel with other memory-intensive programs.


## How to run

- To use the HeelFuel Backend, clone the GitHub repo into a Python IDE and use the provided functions.

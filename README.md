# Saxion - Web Scraping Project Architecture
This is a Web Scraping Project Architecture.
This will help to setup and start a web scraping project, using Python and DRF.

# Preliminaries
`pip install -r requirements.txt`

# Tips
After editing code, go back at the root of the project and run `black .`
This will format the code.

# Run the server
Go at the root of the project.<br>
Run `cd ScrapingProject/`<br>
Run `python manage.py migrate`<br>
Run `python manage.py createsuperuser`<br>
Run `python manage.py runserver`

Address to use : `http://localhost:8000`

# Understand how the project work
It's easy, there is just 3 folders.<br>
`config` / `Scraping` / `ScrapyScraper`<br>

`config` is the folder where all the configuration for the django project are.<br>
`Scraping` is the folder where all the files to setup and adjust the web interface to manage data are.<br>
`ScrapyScraper` is the folder where all the files to setup the scraper (Programs that are collecting data on website) are.
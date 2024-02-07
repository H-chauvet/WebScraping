# ScrapyScraper Documentation

## Create a spider
Go to the folder `ScrapySpider` <br>
Run `scrapy genspider <name of your spider> <url of the website>`

## Configurate the spider
To be able to run the spider with `python manage.py crawl <spider_name>`, you need to do this : <br>
Go to your created spider file. You will have this : <br>
```python
import scrapy


class TemplateSpider(scrapy.Spider):
    name = "template"
    allowed_domains = ["www.google.com"]
    start_urls = ["https://www.google.com"]

    def parse(self, response):
        pass

```

Adjust the `name` as you want. <br>
Then, go at `Scraping/management/commands/crawl.py` and add this line : <br>
`TemplateSpider.name: TemplateSpider,`, Spider.name is the name setup before and Spider is the name of the class of your Spider (Here, TemplateSpider) <br>
This line need to be INSIDE the dict named `SPIDERS`
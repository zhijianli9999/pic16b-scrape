# to run
# scrapy crawl imdb_spider -o movies.csv

import scrapy


class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    # starting show: The Shawshank Redemption
    start_urls = ['https://www.imdb.com/title/tt0111161/']

    def parse(self, response):
        """
        from a movie page, navigate to the Cast & Crew page
        then call parse_full_credits(self,response) on the credits
        """
        credit_url = response.url + "fullcredits"
        yield scrapy.Request(credit_url, callback=self.parse_full_credits)

    def parse_full_credits(self, response):
        """
        from Cast & Crew page, yield a scrapy.Request for the
        page of each actor with parse_actor_page(self, response)
        """
        actor_list = ["https://imdb.com" + a.attrib["href"]
                      for a in response.css("td.primary_photo a")]
        for actor_url in actor_list:
            yield scrapy.Request(actor_url, callback=self.parse_actor_page)

    def parse_actor_page(self, response):
        """
        for each movie/show on the actor page, return a dictionary
        of the form {"actor" : actor_name, "movie_or_TV_name" :
        movie_or_TV_name}.
        """
        n = response.css("div.article.name-overview span.itemprop::text").get()
        if n is None:
            n = response.url
        all_films = response.css("div.filmo-row")
        films = [f.css('b a::text').get()
                 for f in all_films if f.attrib['id'].split('-')[0] == 'actor']
        for film in films:
            yield {"actor": n, "movie_or_TV_name": film}

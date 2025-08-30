import scrapy, re

def parse_price(t: str) -> float:
    if not t:
        return 0.0
    t = t.replace("’","").replace("'","").replace(".–","").replace("CHF","").replace(" ", "")
    m = re.findall(r"\d{2,5}", t)
    return float(m[0]) if m else 0.0

class RicardoSpider(scrapy.Spider):
    name = "ricardo"
    allowed_domains = ["ricardo.ch"]
    start_urls = [
        "https://www.ricardo.ch/fr/s?search=macbook%20m1%20m2%20m3%20m4&priceFrom=300&priceTo=3000&sort=newest"
    ]

    def parse(self, response):
        for it in response.css("[data-testid='srp-card']"):
            title = (it.css("h3::text, h2::text").get() or "").strip()
            price_text = (it.css("[data-testid='srp-card-price']::text").get() or "").strip()
            url = it.css("a::attr(href)").get() or ""
            if url.startswith("/"):
                url = response.urljoin(url)
            loc = (it.css("[data-testid='srp-card-location']::text").get() or "").strip()
            when_text = (it.css("[data-testid='srp-card-time']::text").get() or "").strip()

            yield {
                "source": "ricardo",
                "title": title,
                "price": parse_price(price_text),
                "url": url,
                "location": loc,
                "when": when_text,
            }

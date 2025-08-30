import scrapy, re

def parse_price(t: str) -> float:
    if not t:
        return 0.0
    t = t.replace("’","").replace("'","").replace(".–","").replace("CHF","").replace(" ", "")
    m = re.findall(r"\d{2,5}", t)
    return float(m[0]) if m else 0.0

class TuttiSpider(scrapy.Spider):
    name = "tutti"
    allowed_domains = ["tutti.ch"]
    start_urls = [
        "https://www.tutti.ch/de/li/ganze-schweiz/computer-telefon/notebooks?r=10&prc=300%2C3000&q=macbook"
    ]

    def parse(self, response):
        sel = response.css("a[data-testid='item-link'], article[data-testid='item-card']")
        for it in sel:
            title = (it.css("h2::text, h3::text, span::text").get() or "").strip()
            price_text = (it.css("span:contains('CHF')::text, div:contains('CHF')::text").get() or "").strip()
            url = it.attrib.get("href") or (it.css("a::attr(href)").get() or "")
            if url and url.startswith("/"):
                url = response.urljoin(url)
            loc = (it.css("span:has(svg)::text, div:has(svg)::text").get() or "").strip()

            yield {
                "source": "tutti",
                "title": title,
                "price": parse_price(price_text),
                "url": url,
                "location": loc,
            }

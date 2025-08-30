import scrapy, re

def parse_price(t: str) -> float:
    if not t:
        return 0.0
    t = t.replace("’","").replace("'","").replace(".–","").replace("CHF","").replace(" ", "")
    m = re.findall(r"\d{2,5}", t)
    return float(m[0]) if m else 0.0

class AnibisSpider(scrapy.Spider):
    name = "anibis"
    allowed_domains = ["anibis.ch"]
    start_urls = [
        "https://www.anibis.ch/de/c/computer-software-2/notebooks-204?pr=300-3000&fc=ct&vei=macbook"
    ]

    def parse(self, response):
        sel = response.css("article[data-testid='listing-card'], div[class*='adCard']")
        for it in sel:
            title = (it.css("h2::text, h3::text").get() or "").strip()
            price_text = (it.css("span:contains('CHF')::text, div:contains('CHF')::text").get() or "").strip()
            url = it.css("a::attr(href)").get() or ""
            if url and url.startswith("/"):
                url = response.urljoin(url)
            loc = (it.css("span:has(svg)::text, div:has(svg)::text").get() or "").strip()

            yield {
                "source": "anibis",
                "title": title,
                "price": parse_price(price_text),
                "url": url,
                "location": loc,
            }

BOT_NAME = "finder"

SPIDER_MODULES = ["finder.spiders"]
NEWSPIDER_MODULE = "finder.spiders"

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 0.5

DEFAULT_REQUEST_HEADERS = {
    "Accept-Language": "de-CH,de;q=0.9,fr-CH,fr;q=0.8,it-CH,it;q=0.7,en;q=0.6",
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0.6367.201 Safari/537.36"),
}

FEEDS = {
    "items.json": {"format": "json", "overwrite": True},
}

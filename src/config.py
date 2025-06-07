from datetime import timedelta

PARSERS = [
  {
    "site_url": "https://kuban24.tv/news",
    "article_selector": "div.news-card",
    "title_selector": "a.news-card-title::text",
    "url_selector": "a.news-card-title::attr(href)",
    "date_selector": "div.news-card-head div.news-card-date::text",
    "content_selector": "div[itemprop=\"description\"] > p::text",
    "stop_words": [],
    "parse_interval_sec": 10.0,
    "articles_buffer_size": 30
  },
  {
    "site_url": "https://www.livekuban.ru/news",
    "article_selector": "div.node--news",
    "title_selector": "div.node--description span::text",
    "url_selector": "div.node--description a::attr(href)",
    "date_selector": "div.date::text",
    "content_selector": "div.article-content > p::text",
    "stop_words": [],
    "parse_interval_sec": 10.0,
    "articles_buffer_size": 30
  }
]

MAX_DF = 0.7
MIN_DF = 1
EPS = 1.17
MIN_SAMPLES = 1

CLUSTER_TTL = timedelta(days=10)

PARSING_INTERVAL = 3600
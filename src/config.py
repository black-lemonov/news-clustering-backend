from datetime import timedelta

PARSERS = [
  {
    "site_url": "https://kuban24.tv/news",
    "article_selector": "div.news-card",
    "title_selector": "a.news-card-title::text",
    "url_selector": "a.news-card-title::attr(href)",
    "date_selector": "div.news-card-head div.news-card-date::text",
    "content_selector": "div[itemprop=\"description\"] > p::text",
    "stop_words": [
        "ТОП", "Гороскоп", "Успейте воспользоваться",
        "выгодными условиями", "Подробности по телефону"
    ],
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
    "stop_words": [
        "ТОП", "Гороскоп", "пока вы", "Сроки действия акции", "акции",
        "Успейте воспользоваться",  "выгодными условиями",
        "Подробности по телефону", "По вопросам публикаций обращайтесь"
    ],
    "parse_interval_sec": 10.0,
    "articles_buffer_size": 30
  }
]

MAX_DF = 0.7
MIN_DF = 1
EPS = 1.17
MIN_SAMPLES = 1

CLUSTER_TTL = timedelta(seconds=10)

PARSING_INTERVAL = 3600

SUMMARY_SIZE = 3

LOG_LEVEL = "DEBUG"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default_console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["default_console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["default_console"],
        "level": "WARNING",
    },
}

SUMM_MODELS_FILEPATHS = {
    "dt": "ml_models/best_dt.joblib",
    "rf": "ml_models/best_rf.joblib",
    "xgb": "ml_models/best_xgb.json",
    "lgbm": "ml_models/best_lgbm.joblib",
    "text-rank": ""
}

SELECTED_MODEL = "lgbm"

# -*- coding: utf-8 -*-

# Scrapy settings for scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'webCrawler_scrapy'  # 与自己实现的爬虫类中的name属性一致

SPIDER_MODULES = ['webCrawler_scrapy.spiders']
NEWSPIDER_MODULE = 'webCrawler_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'scrapy (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3   # 重试次数
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     # 'Accept-Language': 'en',
#     "Referer": "https://i.autohome.com.cn",
#     "Host": "i.autohome.com.cn",
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'scrapy.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'scrapy.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'scrapy.pipelines.SomePipeline': 300,
# }
ITEM_PIPELINES = {  # 'webCrawler_scrapy.pipelines.WebcrawlerScrapyPipeline': 300,  # 保存到mysql数据库
    # 'webCrawler_scrapy.pipelines.ExcelBossPipeline': 300,  # 保存到Excel
    'webCrawler_scrapy.pipelines.ScrapyMySQLPipeline': 300,  # 保存到MySQL
    'webCrawler_scrapy.pipelines.JsonWithEncodingPipeline': 300,  # 保存到文件中
}

    # Enable and configure the AutoThrottle extension (disabled by default)
    # See http://doc.scrapy.org/en/latest/topics/autothrottle.html
    # AUTOTHROTTLE_ENABLED = True
    # The initial download delay
    # AUTOTHROTTLE_START_DELAY = 5
    # The maximum download delay to be set in case of high latencies
    # AUTOTHROTTLE_MAX_DELAY = 60
    # The average number of requests Scrapy should be sending in parallel to
    # each remote server
    # AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
    # Enable showing throttling stats for every response received:
    # AUTOTHROTTLE_DEBUG = False

    # Enable and configure HTTP caching (disabled by default)
    # See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
    # HTTPCACHE_ENABLED = True
    # HTTPCACHE_EXPIRATION_SECS = 0
    # HTTPCACHE_DIR = 'httpcache'
    # HTTPCACHE_IGNORE_HTTP_CODES = []
    # HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

    # SPIDER_MIDDLEWARES = {
    #     'scrapy_deltafetch.DeltaFetch': 100
    # }
    # DELTAFETCH_ENABLED = True

# Mysql数据库的配置信息
# MYSQL_HOST = '123.56.242.12'
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'cars'  # 数据库名字
MYSQL_USER = 'root'  # 数据库账号
MYSQL_PASSWD = 'root'  # 数据库密码

MYSQL_PORT = 3306  # 数据库端口，在dbhelper中使用
# LOG_LEVEL = 'ERROR'  # 设置日志等级
# LOG_FILE = '../logs/log.txt'  # 设置日志路径
REDIRECT_ENABLED = True
HTTPERROR_ALLOWED_CODES = [302, 500, 400]
CONCURRENT_REQUESTS = 50
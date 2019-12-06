# -*- coding: utf-8 -*-

# Scrapy settings for XiaoHua project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'XiaoHua'

SPIDER_MODULES = ['XiaoHua.spiders']
NEWSPIDER_MODULE = 'XiaoHua.spiders'

LOG_FILE = "mySpider.log"
LOG_LEVEL = 'WARNING'  # 日志级别

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 配置Scrapy执行的最大并发请求（默认值：16）
CONCURRENT_REQUESTS = 32

# 为同一网站的请求配置延迟（默认值：0）
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# 另请参见autothrottle设置和文档
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    # 'cookie': '_zap=d62a474a-43dc-450a-bdcc-cb807357f4ab; _xsrf=3999fea2-0356-42e7-8d2a-ac968d594c86; d_c0="AEDkV8GlCw-PTjUrBeB6hDjqwntD_bakBL8=|1551259687";q_c1=7d117a8c0f564a3ea2a20d02f83e3bb1|1551259688000|1551259688000; tgw_l7_route=66cb16bc7f45da64562a077714739c11'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'XiaoHua.middlewares.XiaohuaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'XiaoHua.middlewares.XiaohuaDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'XiaoHua.pipelines.SavePipeline': 300,
    'XiaoHua.pipelines.SaveVideoPipeline':301,
}
IMAGES_STORE = 'images'
IMAGES_URLS_FIELD='image'

FILES_STORE = 'video'
FILES_URLS_FIELD = 'video'
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

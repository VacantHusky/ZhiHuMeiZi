# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageItem(scrapy.Item):
    title = scrapy.Field()  # 标题（问题的标题）
    love = scrapy.Field()  # 点赞数量
    comment = scrapy.Field()  # 评论数量
    image = scrapy.Field()  # 图片链接（列表）
    video = scrapy.Field()  # 视频id
    v_id = scrapy.Field()

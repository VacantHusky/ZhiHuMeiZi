# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
import uuid
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
import six

from XiaoHua.settings import IMAGES_STORE, FILES_STORE

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
from PIL import Image

class SavePipeline(ImagesPipeline):
    min_w_h = 200000

    # 设置requests
    def get_media_requests(self, item, info):
        li = []
        for i in range(len(item['image'])):
            li.append(scrapy.Request(url=item['image'][i], meta={'item': item, 'count': i}))
        return li

    # 文件路径
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        count = request.meta['count']
        image_name = item['image'][count].split('/')[-1]
        score = int(item['love']) + int(item['comment']) * 10
        path = item['title'] + '/' + "{:08d}".format(score) + '-' + image_name
        if os.path.exists(IMAGES_STORE + '/' + path):
            # path = item['title'] + '/' + "{:08d}".format(score) + '-' + uuid.uuid4()
            print('文件已存在！！！！！！！！！！！！！！！！！！！！！！')
        return path

    # 获取图片
    def get_images(self, response, request, info):
        path = self.file_path(request, response=response, info=info)
        orig_image = Image.open(BytesIO(response.body))
        if orig_image.mode == "P":
            orig_image = orig_image.convert('RGB')

        image, buf = self.convert_image(orig_image)

        width, height = orig_image.size
        if width * height < self.min_w_h:
            too_small_path = '/' + path.split('/')[0] + '【小图】/'
            score = path.split('/')[1]
            if not os.path.exists(IMAGES_STORE+'/'+too_small_path):
                os.makedirs(IMAGES_STORE+'/'+too_small_path)
            path = '{}/{}'.format(too_small_path, score)
            print("====图片太小 (%dx%d=%d < %d)" % (width, height, width * height, self.min_w_h))

        yield path, image, buf

        for thumb_id, size in six.iteritems(self.thumbs):
            thumb_path = self.thumb_path(request, thumb_id, response=response, info=info)
            thumb_image, thumb_buf = self.convert_image(image, size)
            yield thumb_path, thumb_image, thumb_buf


class SaveVideoPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        li = []
        for i in range(len(item['video'])):
            li.append(scrapy.Request(url=item['video'][i], meta={'item': item, 'count': i}))
        return li

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        video_name = item['v_id']
        score = int(item['love']) + int(item['comment']) * 10
        path = "{}/{:08d}-{}.mp4".format(item['title'],score,video_name)
        if os.path.exists(FILES_STORE + '/' + path):
            # path = "{}/{:08d}-{}.mp4".format(item['title'],score,uuid.uuid4())
            print('视频文件已存在！！！！！！！！！！！！！！！！！！！！！！')

        return path

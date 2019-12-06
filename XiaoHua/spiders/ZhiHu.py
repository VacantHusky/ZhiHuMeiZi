# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request
from pyquery import PyQuery

from XiaoHua.items import ImageItem

# 下载视频的最大大小（单位：MB）
MAX_VIDEO = 150

zhihu_url = 'https://www.zhihu.com/api/v4/questions/{}/answers?' \
            'include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward' \
            '_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%' \
            '2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2' \
            'Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cv' \
            'oteup_count%2Creshipment_settings%2Ccomment_permission%2Ccrea' \
            'ted_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquest' \
            'ion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoti' \
            'ng%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mar' \
            'k_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2C' \
            'badge%5B%2A%5D.topics&limit={}&offset={}&platform=desktop&sort_by={}'

zhihu_video_url = 'https://lens.zhihu.com/api/v4/videos/{}'

TITLE = '未找到标题'

class ZhihuSpider(scrapy.Spider):
    name = 'ZhiHu'

    def __init__(self, id_, offset, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_ = id_
        self.offset = offset
        self.page_ = 0
        self.img_n = 0
        self.video_n = 0

    def start_requests(self):
        sort = 'updated'
        limit = 20
        url = zhihu_url.format(self.id_, limit, self.offset, sort)
        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        if data.get("data"):
            for i, data_ in enumerate(data['data']):
                try:
                    content = PyQuery(data_['content'])
                except:
                    continue
                if data_.get('question') and data_['question'].get('title'):
                    title = data_['question'].get('title')
                else:
                    title = TITLE
                for x in ['+', '*', '/', '?', '“', '<', '>', '|', ' ']:
                    title = title.replace(x, '')
                imgUrls = content.find('noscript img').items()
                item = ImageItem()
                item['title'] = title
                item['image'] = []
                item['video'] = []
                item['comment'] = data_['comment_count']
                item['love'] = data_['voteup_count']
                for imgTag in imgUrls:
                    src = imgTag.attr("data-original")
                    if not src:
                        src = imgTag.attr("src")
                    item['image'].append(src)
                    self.img_n += 1
                yield item
                videos = content.find('.video-box').items()
                for video in videos:
                    v_id = video.attr('data-lens-id')
                    if not v_id or v_id=='':
                        continue
                    self.video_n+=1
                    yield Request(
                        url=zhihu_video_url.format(v_id),
                        callback=self.video_parse,
                        meta={'title':title,'comment':item['comment'],'love':item['love']},
                        dont_filter=True)
        if data.get("paging"):
            assert 'is_end' in data['paging'].keys()
            assert 'next' in data['paging'].keys()
            if not data['paging']['is_end']:
                print('第{}页完成===下一页：{}'.format(self.page_, data['paging']['next']))
                print('爬取了{}张图片,{}个视频。'.format(self.img_n,self.video_n))
                self.page_ += 1
                yield Request(url=data['paging']['next'], callback=self.parse, dont_filter=True)
            else:
                print('没有下一页了，正常退出。共计{}页，{}张图。'.format(self.page_, self.img_n))
        else:
            print('!!!!!!!!!非正常结束！！！！！！！')
            print(data)

    def video_parse(self,response):
        url = response.request.url
        title = response.meta['title']
        comment = response.meta['comment']
        love = response.meta['love']
        data = json.loads(response.text)
        if data.get('playlist'):
            playlist = data.get('playlist')
            if playlist.get('HD'):
                qx = 'HD'
            elif playlist.get('SD'):
                qx = 'SD'
            elif playlist.get('LD'):
                qx = 'LD'
            else:
                qx = ''
            if qx != '':
                play_url = playlist.get(qx).get('play_url')
                size = playlist.get(qx).get('size')
                if int(size) > 1024*1024*MAX_VIDEO:
                    print('视频太大')
                    with open('too_big_video.txt','a',encoding='utf-8') as f:
                        f.write('{}\t{}\n'.format(title,play_url))
                    return
                item = ImageItem()
                item['title'] = title
                item['image'] = []
                item['comment'] = comment
                item['love'] = love
                item['video'] = [play_url]
                item['v_id'] = url.split('/')[-1]
                yield item
            else:
                print('==error==\n找不到清晰度url:{}'.format(url))
        else:
            print('==error==\nurl:{}\n中没有找到playlist'.format(url))

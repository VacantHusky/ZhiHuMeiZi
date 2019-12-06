# 爬取知乎上的小姐姐

## 介绍
知乎上的东西质量都很好，有些问题下会有很多很好的回答，其中就有些关于图片的。
比如：
* [你见过最漂亮的女生长什么样？](https://www.zhihu.com/question/34243513)
* [平常人可以漂亮到什么程度？](https://www.zhihu.com/question/50426133)
* [有没有第一次见就让人震惊的手机壁纸？](https://www.zhihu.com/question/309298287)
* [有哪些图片适合做电脑桌面？](https://www.zhihu.com/question/21180335)

图片有了，那么...
![我全都要](https://img-blog.csdnimg.cn/20191105155117607.jpg)

所以我写了个爬虫，把它们都爬下来了。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20191105155541824.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM3OTYzNjE1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191105163252977.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM3OTYzNjE1,size_16,color_FFFFFF,t_70)
 1. 找到api
 
 虽然可以通过直接爬html来获取，但是通过api可以获取html所没有的信息。
 ```python
 zhihu_url = 'https://www.zhihu.com/api/v4/questions/{问题id}/answers?' \
 		'include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward' \
        '_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%' \
        '2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2' \
        'Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cv' \
        'oteup_count%2Creshipment_settings%2Ccomment_permission%2Ccrea' \
        'ted_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquest' \
        'ion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoti' \
        'ng%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mar' \
        'k_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2C' \
        'badge%5B%2A%5D.topics&limit={一页条目数}' \
        '&offset={偏移量}&platform=desktop' \
        '&sort_by={排序方式}'
```
问题id在url中可以找到，比如https://www.zhihu.com/question/34243513，34243513就是它的id。
一页条目数当然越大越好，不过最大只能取20。
偏移量就是这一页第一条的序号，比如第一页是0，第二页是20（假设一页条目数为20）。
排放方式我们用“updated”，按时间排序。

所以任意一页的url我们就知道了，但是我们不知道有多少页。

 2. 获取json数据
 请求该url就可以获取json数据，其结构如下：
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20191105162355704.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM3OTYzNjE1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191105162408285.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM3OTYzNjE1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191105162422850.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM3OTYzNjE1,size_16,color_FFFFFF,t_70)

可以看到，每请求一页就可以知道是不是最后一页和获取下一页的地址。

## 2.项目介绍
本项目使用scrapy框架。
项目根目录下有一个run.py文件。
在该目录下使用命令行输入：
```shell
pyton3 run.py -i <知乎id> -p <起始页码>
# 例如：
pyton3 run.py -i 34243513 -p 0
# 或省略掉-p
```

---


懒得介绍了，有什么问题可以私信我。


作者：TigerWang
邮箱：conan1015@foxmail.com

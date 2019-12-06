from scrapy import cmdline
import argparse
import time

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-i','--id', type=str, default='60199335',help="知乎问题id")
parser.add_argument('-p','--page', type=int, default=0,help='从哪一页开始，默认0')
args = parser.parse_args()

id_ = args.id
start = args.page * 20
if not id_:
    exit(0)

cmdline.execute("scrapy crawl ZhiHu -a id_={} -a offset={}".format(id_,start).split())
time.sleep(6)

# coding: utf-8
import os
import random
import sys
from datetime import datetime
from logging import DEBUG, INFO, getLogger

from PictureGathering.Crawler import Crawler

logger = getLogger("root")
logger.setLevel(INFO)


class FavCrawler(Crawler):
    def __init__(self):
        super().__init__()
        try:
            self.save_path = os.path.abspath(self.config["save_directory"]["save_fav_path"])
        except KeyError:
            logger.exception("save_directory/save_fav_path is invalid.")
            exit(-1)
        self.type = "Fav"

    def FavTweetsGet(self, page):
        kind_of_api = self.config["tweet_timeline"]["kind_of_timeline"]
        if kind_of_api == "favorite":
            url = "https://api.twitter.com/1.1/favorites/list.json"
            params = {
                "screen_name": self.user_name,
                "page": page,
                "count": self.count,
                "include_entities": 1,  # ツイートのメタデータ取得。これしないと複数枚の画像に対応できない。
                "tweet_mode": "extended"
            }
        elif kind_of_api == "home":
            url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
            params = {
                "count": self.count,
                "include_entities": 1,
                "tweet_mode": "extended"
            }
        else:
            logger.error("kind_of_api is invalid.")
            return None

        return self.TwitterAPIRequest(url, params)

    def UpdateDBExistMark(self, add_img_filename):
        # 存在マーキングを更新する
        self.db_cont.DBFavFlagClear()
        self.db_cont.DBFavFlagUpdate(add_img_filename, 1)

    def GetVideoURL(self, filename):
        # 'https://video.twimg.com/ext_tw_video/1139678486296031232/pu/vid/640x720/b0ZDq8zG_HppFWb6.mp4?tag=10'
        response = self.db_cont.DBFavVideoURLSelect(filename)
        url = response[0]["url"] if len(response) == 1 else ""
        return url

    def MakeDoneMessage(self):
        now_str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        done_msg = "Fav PictureGathering run.\n"
        done_msg += now_str
        done_msg += " Process Done !!\n"
        done_msg += "add {0} new images. ".format(self.add_cnt)
        done_msg += "delete {0} old images.".format(self.del_cnt)
        done_msg += "\n"

        # 画像URLをランダムにピックアップする
        random_pickup = True
        if random_pickup:
            pickup_url_list = random.sample(self.add_url_list, min(4, len(self.add_url_list)))
            for pickup_url in pickup_url_list:
                pickup_url = str(pickup_url).replace(":orig", "")
                done_msg += pickup_url + "\n"

        return done_msg

    def Crawl(self):
        logger.info("Fav Crawler run.")
        # count * fav_get_max_loop だけツイートをさかのぼる。
        fav_get_max_loop = int(self.config["tweet_timeline"]["fav_get_max_loop"]) + 1
        for i in range(1, fav_get_max_loop):
            tweets = self.FavTweetsGet(i)
            self.InterpretTweets(tweets)
        self.ShrinkFolder(int(self.config["holding"]["holding_file_num"]))
        self.EndOfProcess()
        return 0


if __name__ == "__main__":
    c = FavCrawler()

    # クロール前に保存場所から指定枚数削除しておく
    # c.ShrinkFolder(int(c.config["holding"]["holding_file_num"]) - 10)
    # c.del_cnt = 0
    # c.del_url_list = []

    c.Crawl()

# coding: utf-8
import configparser
import random
import shutil
import sys
import unittest
import warnings
from contextlib import ExitStack
from logging import WARNING, getLogger
from mock import MagicMock, PropertyMock, mock_open, patch
from pathlib import Path
from time import sleep
from typing import List

from PictureGathering import LinkSearchBase


logger = getLogger("root")
logger.setLevel(WARNING)


class TestLinkSearchBase(unittest.TestCase):
    """外部リンク探索処理テストメインクラス
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_LinkSearchBase(self):
        """外部リンク探索処理クラス初期状態チェック
        """
        ls_cont = LinkSearchBase.LinkSearchBase()
        self.assertEqual([], ls_cont.processer_list)

    def test_Register(self):
        """担当者登録機能をチェック
        """
        ls_cont = LinkSearchBase.LinkSearchBase()

        # 正常系
        # 具体的な担当者を登録
        lsc = LinkSearchBase.LSConcrete_0()
        res0 = ls_cont.Register(lsc)
        lsc = LinkSearchBase.LSConcrete_1()
        res1 = ls_cont.Register(lsc)
        lsc = LinkSearchBase.LSConcrete_2()
        res2 = ls_cont.Register(lsc)
        self.assertEqual(0, res0)
        self.assertEqual(0, res1)
        self.assertEqual(0, res2)

        # 異常系
        # LinkSearchBaseの派生クラスでないクラスを登録しようとする
        class LSFake():
            def __init__(self):
                pass
        lsc = LSFake()
        res = ls_cont.Register(lsc)
        self.assertEqual(-1, res)

        # 異常系？
        # THINK::LinkSearchBaseの派生クラスでないがインターフェイスは整っている
        # 処理もできるので一応OKとする
        class LSImitation():
            def __init__(self):
                pass

            def IsTargetUrl(self, url: str) -> bool:
                return False

            def Process(self, url: str) -> int:
                return 0
        lsc = LSImitation()
        res = ls_cont.Register(lsc)
        self.assertEqual(0, res)

    def test_IsTargetUrl(self):
        """自分（担当者）が処理できるurlかどうか判定する機能をチェック
        """
        ls_cont = LinkSearchBase.LinkSearchBase()
        url = "https://www.google.co.jp/"
        self.assertEqual(False, ls_cont.IsTargetUrl(url))  # 基底クラスなので常にFalse


if __name__ == "__main__":
    if sys.argv:
        del sys.argv[1:]
    unittest.main()

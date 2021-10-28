import unittest
from pagerank_iterativ2 import Page
import pagerank_iterativ2

class PageTest(unittest.TestCase):
    def setUp(self):
        self.page = Page('test')

    def test_incoming_links(self):
        self.assertTrue(len(self.page.incoming_links)==0)

class PagerankTest(unittest.TestCase):
    def setUp(self):
        self.demo1 = pagerank_iterativ2.demo1()

    def test_calc(self):
        pagerank_iterativ2.calc_pr(self.demo1, 0.85, 80)
        for p in self.demo1:
            if p.name == 'a': self.assertTrue(0.14 < p.pr < 0.16)
            elif p.name == 'b': self.assertTrue(0.213 < p.pr < 0.215)
            elif p.name == 'c': self.assertTrue(0.394 < p.pr < 0.396)
            else: assert False

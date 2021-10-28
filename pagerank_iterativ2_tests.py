import unittest
from pagerank_iterativ2 import Page, calc_pr
import pagerank_iterativ2

class PageTest(unittest.TestCase):
    def setUp(self):
        self.page = Page('test')

    def test_incoming_links(self):
        self.assertEqual(len(self.page.incoming_links), 0)
        self.assertEqual(len(self.page.outgoing_links), 0)
        self.assertEqual(self.page.number_outgoing_links(), 0)


class PagerankTest(unittest.TestCase):
    def setUp(self):
        self.demo1 = pagerank_iterativ2.demo1()
        self.demo2 = pagerank_iterativ2.demo2()

    def test_calc_demo1(self):
        calc_pr(self.demo1, 0.85, 80)
        for p in self.demo1:
            if p.name == 'a': self.assertTrue(0.14 < p.pr < 0.16)
            elif p.name == 'b': self.assertTrue(0.213 < p.pr < 0.215)
            elif p.name == 'c': self.assertTrue(0.394 < p.pr < 0.396)
            else: assert False

    def test_calc_demo2(self):
        calc_pr(self.demo2, 0.5, 80)
        for p in self.demo2:
            if p.name == 'a': self.assertTrue(1.07692 < p.pr < 1.07693)
            elif p.name == 'b': self.assertTrue(0.7692 < p.pr < 0.7693)
            elif p.name == 'c': self.assertTrue(1.153 < p.pr < 1.154)
            else: assert False

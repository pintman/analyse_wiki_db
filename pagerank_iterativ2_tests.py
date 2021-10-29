import unittest
from pagerank_iterativ2 import Page, calc_pr, wikipages
import pagerank_iterativ2

# Results: https://github.com/pintman/analyse_wiki_db/actions

class PageTest(unittest.TestCase):
    def setUp(self):
        self.page = Page('test')

    def test_incoming_links(self):
        self.assertEqual(len(self.page.incoming_links), 0)
        self.assertEqual(len(self.page.outgoing_links), 0)
        self.assertEqual(self.page.number_outgoing_links(), 0)


class PagerankTest(unittest.TestCase):
    def setUp(self):
        '''
        c <- a -> b
        ^--------/
        '''
        a = Page('a')
        b = Page('b')
        c = Page('c')

        a.outgoing_links = [b, c]
        b.outgoing_links = [c]
        b.incoming_links = [a]
        c.incoming_links = [a, b]
        self.demo1 = [a, b, c]

        '''
        b <- a <-> c
        \---------^
        '''
        a = Page('a')
        b = Page('b')
        c = Page('c')

        a.outgoing_links = [b, c]
        a.incoming_links = [c]
        b.outgoing_links = [c]
        b.incoming_links = [a]
        c.outgoing_links = [a]
        c.incoming_links = [a, b]
        self.demo2 = [a, b, c]       

    def test_calc_demo1(self):
        calc_pr(self.demo1, 0.85, 80)
        for p in self.demo1:
            if p.name == 'a': self.assertTrue(0.14 < p.pr < 0.16)
            elif p.name == 'b': self.assertTrue(0.213 < p.pr < 0.215)
            elif p.name == 'c': self.assertTrue(0.394 < p.pr < 0.396)
            else: self.assertFalse()

    def test_calc_demo2(self):
        calc_pr(self.demo2, 0.5, 80)
        for p in self.demo2:
            if p.name == 'a': self.assertTrue(1.07692 < p.pr < 1.07693)
            elif p.name == 'b': self.assertTrue(0.7692 < p.pr < 0.7693)
            elif p.name == 'c': self.assertTrue(1.153 < p.pr < 1.154)
            else: self.assertFalse()

    def test_wiki_pages(self):
        ps = wikipages("", "", "wiki_ITF19a.sqlite", "page", "pagelinks")
        self.assertEqual(len(ps), 39)
        calc_pr(ps, d=0.85, iterations=20, debug=False)
        ps.sort(reverse=True)
        top5 = [('Mause', 3.806), ('Maus', 3.385), ('Bildschirm', 3.381), ('Hardware', 1.186), ('Software', 1.1)]
        for soll, ist in zip(top5, ps[:5]):
            self.assertEqual(soll[0], ist.name)
            self.assertEqual(round(soll[1], 2), round(ist.pr, 2))
            
        bottom3 =  [('Schreiber', 0.15), ('Localhost', 0.15), ('Flowchart.png', 0.15)]
        for soll, ist in zip(bottom3, ps[-3:]):
            self.assertEqual(soll[0], ist.name)
            self.assertEqual(soll[1], 0.15)

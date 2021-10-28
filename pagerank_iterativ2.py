# Version 2: Mit Klasse Page

import unittest

# create a graph from edges: (source,target)
graph1 = [('a','b'), ('b','a')]
graph2 = [('a','c'), ('c','b'), ('b','a')]
graph3 = [('a','b'), ('a','c'), ('b','a'), ('b', 'c'), ]
graph4 = [('a','b'), ('b','c')]
graph = graph3


class Page:
    def __init__(self, name: str, inlinks=None, outlinks=None):
        self.pr = 1
        self.name = name
        if inlinks is None:
            self.incoming_links = []
        else:
            self.incoming_links = inlinks
        if outlinks is None:
            self.outgoing_links = []
        else:
            self.outgoing_links = outlinks

    def number_outgoing_links(self) -> int:
        return len(self.outgoing_links)

    def get_incoming_links(self) -> list:
        return self.incoming_links

    def __lt__(self, other):
        return self.pr < other.pr

    def __str__(self):
        return self.name + " " + str(self.pr)



def calc_pr(pages: list, d: float, iterations: int, debug=False):
    for i in range(iterations):
        if debug:
            print("iteration", i)
        for p in pages:
            pr_sum = 0
            for pin in p.get_incoming_links():
                pr_sum += pin.pr / pin.number_outgoing_links()
            p.pr = 1 - d + d * pr_sum

        # debug output
        if debug:
            print(i, ': ', end='')
            for p in pages:
                print(p.name, p.pr, end='  ')
            print()


def demo1():
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
    return [a, b, c]

def test_demo1():
    pages = demo1()

    calc_pr(pages, 0.85, 80)
    for p in pages:
        if p.name == 'a': assert 0.14 < p.pr < 0.16
        elif p.name == 'b': assert 0.213 < p.pr < 0.215
        elif p.name == 'c': assert 0.394 < p.pr < 0.396
        else: assert False

def demo2():
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
    return [a, b, c]

def test_demo2():
    pages = demo2()

    calc_pr(pages, 0.5, 80)
    for p in pages:
        if p.name == 'a': assert 1.07692 < p.pr < 1.07693
        elif p.name == 'b': assert 0.7692 < p.pr < 0.7693
        elif p.name == 'c': assert 1.153 < p.pr < 1.154
        else: assert False

def wikipages(user:str, password:str, database:str, pagetable:str, pagelinkstable:str):
    if 'sqlite' in database:
        import sqlite3
        query = f"""
            SELECT page_id, 
                page_title AS page_von, 
                pl_title AS page_nach
            FROM {pagetable}
            LEFT JOIN {pagelinkstable} ON pl_from=page_id
            ORDER BY page_id
        """
        conn = sqlite3.connect(database)

    else:
        import mysql.connector
        # cast needed since page_title and pl_title are varbinary
        query = f"""
            SELECT page_id, 
                cast(page_title AS CHAR) AS page_von, 
                cast(pl_title AS CHAR) AS page_nach
            FROM {pagetable}
            LEFT JOIN {pagelinkstable} ON pl_from=page_id
            ORDER BY page_id
        """
        conn = mysql.connector.connect(
            user=user, password=password, host="localhost", database=database)

    c = conn.cursor()
    c.execute(query)
    pages = {}
    for _page_id, page_von, page_nach in c:
        if page_von not in pages:
            pages[page_von] = Page(page_von)
        if page_nach is None:
            continue
        if page_nach not in pages:
            pages[page_nach] = Page(page_nach)

        pvon = pages[page_von]
        pnach = pages[page_nach]

        if pnach not in pvon.outgoing_links:
            pvon.outgoing_links.append(pnach)
        if pvon not in pnach.incoming_links:
            pnach.incoming_links.append(pvon)

    conn.close()
    return list(pages.values())

def save_dot(pages, filename):
    'Save pages to dotfile that can be rendered by graphviz: dot -o a.pdf -T pdf a.dot'
    with open(filename, 'wt') as f:
        f.write('digraph G{\n')
        for p in pages:
            for pout in p.outgoing_links:
                num_p_outs = len(p.outgoing_links)
                num_pout_outs = len(pout.outgoing_links)
                f.write(f'"{p.name} #{num_p_outs}\\n{round(p.pr,3)}" -> "{pout.name} #{num_pout_outs}\\n{round(pout.pr,3)}";\n')
                #f.write(f'"{p.name}" -> "{pout.name}";\n')

        f.write('}\n')

def print_pages(pagelist):
    for p in pagelist:
        print(p.name, "->", [pnach.name for pnach in p.outgoing_links])

def main():
    #ps = wikipages("root", "", "dewikiquote", "page", "pagelinks")
    #ps = wikipages("root", "", "wikiitf14a", "wikipage", "wikipagelinks")
    #ps = wikipages("root", "", "wikiitf17a", "page", "pagelinks")
    #ps = wikipages("root", "", "wiki_itf18a", "page", "pagelinks")
    ps = wikipages("", "", "wiki_ITF19a.sqlite", "page", "pagelinks")
    print("read pages", len(ps))
    print_pages(ps)
    calc_pr(ps, d=0.85, iterations=15, debug=False)
    ps.sort(reverse=True)
    print("RESULT\n", 
        [(p.name, round(p.pr, 3)) for p in ps[:5]], 
        "\n ...\n",
        [(p.name, round(p.pr, 3)) for p in ps[-3:]])
    print("SUM-PR", sum([p.pr for p in ps]))  

    save_dot(ps, 'itf19a.dot')

    """
    ITF19a:
    read pages 39
    [('Mause', 3.806), ('Maus', 3.385), ('Bildschirm', 3.381), ('Hardware', 1.186), ('Software', 1.1)] 
    ...
    [('Schreiber', 0.15), ('Localhost', 0.15), ('Flowchart.png', 0.15)]
    SUM-PR 21.94321975734223
    """

    return ps


if __name__ == "__main__":
    ps = main()

    #import cProfile
    #import pstats
    #cProfile.run("main()", sort=pstats.SortKey.TIME)
    # An welcher Stelle wird am meisten Zeit verbraucht? - fetch_row
    # Zeilen werden einzeln aus der DB geholt. -> cursor.fetchall() verwendet
    # 
    # Running Profiler and saving statistics. Can be viewed with
    # python -m pstats pagerank.pstats
    #cProfile.run("main()", filename="pagerank.pstats")

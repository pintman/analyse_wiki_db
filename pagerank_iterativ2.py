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


def main():
    ps = wikipages("", "", "wiki_ITF19a.sqlite", "page", "pagelinks")
    print("read pages", len(ps))
    calc_pr(ps, d=0.85, iterations=15, debug=False)
    ps.sort(reverse=True)
    print("RESULT\n", 
        [(p.name, round(p.pr, 3)) for p in ps[:5]], 
        "\n ...\n",
        [(p.name, round(p.pr, 3)) for p in ps[-3:]])
    print("SUM-PR", sum([p.pr for p in ps]))  

    return ps


if __name__ == "__main__":
    ps = main()

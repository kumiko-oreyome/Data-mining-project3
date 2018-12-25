from load import load_graph_from_txt,load_graph_from_transaction
from algo import Graph,HITS,PageRank,SimRank
def hits_main(filepath,tr=False,bi=False):
    if tr:
        graph = load_graph_from_transaction(filepath,bi)
    else:
        graph = load_graph_from_txt(filepath)   
    hits = HITS(graph)
    hits.iterate()
    hits.print_res()
    #hits.rank_by_auth()
    #hits.rank_by_hub()

def pagerank_main(filepath,tr=False,bi=False):
    if tr:
        graph = load_graph_from_transaction(filepath,bi)
    else:
        graph = load_graph_from_txt(filepath)

    pr = PageRank(graph)
    pr.iterate()
    pr.print_res()
    
def simrank_main(filepath,tr=False,bi=False):
    if tr:
        graph = load_graph_from_transaction(filepath,bi)
    else:
        graph = load_graph_from_txt(filepath)   
    pr = SimRank(graph)
    pr.iterate()
    pr.print_res()
#hits_main("transcation.txt",True,True)
#load_graph_from_transaction("transcation.txt",False)
#hits_main("transcation.txt",True,True)
#hits_main("graph_6.txt")
#pagerank_main("transcation.txt",True,True)
#hits_main("hub1.txt")
#hits_main("aut1.txt")
#hits_main("aut2.txt")
#print('page rank')
#pagerank_main("pagerank_1.txt")
#pagerank_main("pagerank_2.txt")
simrank_main('graph_5.txt')


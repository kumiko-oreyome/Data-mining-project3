from algo import Graph,HITS
def load_graph_from_txt(path):
    graph = Graph()
    with open(path,'r',encoding="utf-8") as f:
        edges = []
        for line in f:
            src,tar= line.rstrip().split(",")
            edges.append((int(src),int(tar)))
        graph.spawn(edges)
    return graph

def load_graph_from_transaction(path,bi):
    graph = Graph()
    with open(path,'r',encoding="utf-8") as f:
        edges = []
        for line in f:
            ids = line.rstrip().split(",")
            for nid1 in ids:
                for nid2 in ids:
                    if  nid1 < nid2:
                        continue
                    if bi:
                        edges.append((int(nid1),int(nid2)) )
                    else:
                        edges.append((int(nid2),int(nid1)))
        graph.spawn(edges)
    return graph 


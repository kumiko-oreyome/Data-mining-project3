import math
class Node():
    def __init__(self,id):
        self.id = id
        self.parents = []
        self.children = []

    def add_child(self,node):
        self.assert_id_not_exist(node.id,self.children)
        self.children.append(node)
    
    def add_parent(self,node):
        #self.assert_id_not_exist(node.id,self.parents)
        if node.id not in map(lambda x:x.id,self.parents):
            self.parents.append(node)
        

    def assert_id_not_exist(self,id,l):
        #assert id not in map(lambda x:x.id,l)
        pass


class Graph():
    def __init__(self):
        self._id_map = {}
    

    def get_nodes(self):
        return list(self._id_map.values())

    def get_childern(self,id):
        return self._id_map[id].children

    def get_parents(self,id):
        return self._id_map[id].parents

    def spawn(self,list_of_edges):
        for src_id,tar_id in list_of_edges:
            self.add_edge(src_id,tar_id)
            
    def add_edge(self,src_id,tar_id):
        src_node = self._get_default_node(src_id)
        tar_node = self._get_default_node(tar_id)
        src_node.add_child(tar_node)
        tar_node.add_parent(src_node)

    def _get_default_node(self,nid):
        if nid not in self._id_map:
            self._id_map[nid] = Node(nid)
        return self._id_map[nid]


class PageRank():
    def __init__(self,graph,dampling_factor=0.1,eps=0.01):
        self.graph = graph
        self.dampling_factor = dampling_factor
        self.eps = 0.01
        self._rank_map = {}
        self._init()

    def _init(self):
        nodes = self.graph.get_nodes()
        n = len(nodes)
        for node in nodes:
            self._rank_map[node.id] = 1/n

    def iterate(self):
        nodes = self.graph.get_nodes()
        n = len(nodes)
        while True:
            new_rank = {}
            for node in nodes:
                rank =  self.dampling_factor/n + (1-self.dampling_factor)*\
                            sum(map(lambda node: self._rank_map[node.id]/len(node.children),node.parents)) 
                new_rank[node.id] = rank
            diff  = {k:self._rank_map[k]-new_rank[k] for k in self._rank_map}
            self._rank_map = new_rank
            #self.print_res()
            if self.norm(diff.values())<self.eps:
                break

    def norm(self,x):
        return sum(map(lambda t :abs(t),x))
        

    def print_res(self,sort=True):
        if sort:
            items = sorted(self._rank_map.items(),key=lambda x:-1*x[1]) 
        else:
            items = self._rank_map.items()
        print('result:')
        for k,v in items:
            print("node %s --> (%.5f)"%(str(k),v))
        print('- '*50)




class HITS():
    def __init__(self,graph,eps=0.01):
        self.eps = eps
        self.graph = graph
        self._aut_map = {}
        self._hub_map = {}
        self._init()

    def _init(self):
        for node in self.graph.get_nodes():
            #print(node.id)
            self._aut_map[node.id] = 1
            self._hub_map[node.id] = 1

    def iterate(self):
        cnt = 0
        while True:
            #print('iterate %d'%(cnt))
            #self.print_res()
            diff_norm_auth,diff_norm_hub = 0,0
            new_aut_map = {}
            new_hub_map = {}
            for node in self.graph.get_nodes():
                new_auth = sum(map(lambda node: self._hub_map[node.id],node.parents)) 
                new_hub =  sum(map(lambda node: self._aut_map[node.id],node.children))
                new_aut_map[node.id] = new_auth
                new_hub_map[node.id] = new_hub
                #diff_norm_auth += (new_auth-self._aut_map[node.id])**2
                #diff_norm_hub += (new_hub-self._hub_map[node.id])**2
                #self._hub_map[node.id],self._aut_map[node.id] = new_hub,new_auth
            norm_aut = self.norm(new_aut_map.values())
            norm_hub = self.norm(new_hub_map.values())
            
            for k,v in new_aut_map.items():
                new_aut_map[k] = new_aut_map[k]/norm_aut
                new_hub_map[k] = new_hub_map[k]/norm_hub

            for k in new_aut_map:
                diff_norm_auth = (new_aut_map[k]-self._aut_map[k])**2
                diff_norm_hub =  (new_hub_map[k]-self._hub_map[k])**2

            self._aut_map,self._hub_map = new_aut_map,new_hub_map

            cnt+=1
            if math.sqrt(diff_norm_auth)+math.sqrt(diff_norm_hub) < self.eps:
                break


    def norm(self,values,t=1):
        if t == 1:
            return sum(map(lambda x:x,values))
        return sum(map(lambda x:x*x,values))

    def rank_by_auth(self):
        for k,v in sorted(self._aut_map.items(),key=lambda x:-1*x[1]):
            self.print_node(k)

    def rank_by_hub(self):
        for k,v in sorted(self._hub_map.items(),key=lambda x:-1*x[1]):
            self.print_node(k)

    def print_res(self):
        print('result:')
        for k in sorted(self._aut_map.keys()):
            self.print_node(k)
        print('- '*50)
    
    def print_node(self,k):
        print("node %s --> (%.3f,%.3f)"%(str(k),self._aut_map[k],self._hub_map[k]))
        
    


class SimRank():
    def __init__(self,graph,C=0.5):
        self.graph = graph
        self.C = C
        self.sim_matrix = {}
        self._init()
    
    def _init(self):
        nodes = self.graph.get_nodes()
        for node1 in nodes:
            for node2 in nodes:
                if node1.id == node2.id:
                    self.sim_matrix[(node1.id,node2.id)] = 1
                else:
                    self.sim_matrix[(node1.id,node2.id)] = 0
    
    def iterate(self,k=100):
        nodes = self.graph.get_nodes()
        for i in range(k):
            for node1 in nodes:
                for node2 in nodes:
                    self.sim_matrix[(node1.id,node2.id)] = self._sim_func(node1,node2)     



    def print_res(self):
        nodes = sorted(self.graph.get_nodes(),key=lambda x:x.id) 
        print('similarity result , C = %.5f'%(self.C))
        for node1 in nodes:
            for node2 in nodes:
                if node2.id >= node1.id and self.sim_matrix[(node1.id,node2.id)]>0:
                    print('%s,%s -->%.5f'%(str(node1.id),str(node2.id),self.sim_matrix[(node1.id,node2.id)]))
               


    def _sim_func(self,node1,node2):
        if node1.id == node2.id:
            return 1.0
        parents1 = node1.parents
        parents2 = node2.parents
        if len(parents1)*len(parents2) == 0:
            return 0
        sim_sum = 0.0
        for p1 in parents1:
            for p2 in parents2:
                sim_sum+= self.sim_matrix[(p1.id,p2.id)]
        sim_sum= self.C*sim_sum/(len(parents1)*len(parents2))
        return sim_sum

    
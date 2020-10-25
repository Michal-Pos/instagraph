from igraph import *
from neo4j_module import user_graph_data


# Zwraca listę wierzchołków danego grafu
def get_vertex_list(g):
    vertex_list = [v['name'] for v in g.vs]
    return vertex_list


# Zwraca listę krawędzi danego grafu
def get_edge_list(g):
    vertecies = get_vertex_list(g)
    edges = g.get_edgelist()
    out_edges = []
    for item in edges:
        out_edges.append((vertecies[item[0]], vertecies[item[1]]))

    return out_edges


# Dla danego grafu, funkcja filtruje te wierzchołki których
# stopień wchodzący jest zgodny z podanym zakresem(start, stop).
# Jeśli stop jest zostawiony domyślnie to przyjmuje wartość największego możliwego stopienia wchodzącego.
def indegree_filter(g, start=0, stop=0):
    g.as_directed()
    if stop == 0:
        stop = g.maxdegree()
    vertices = get_vertex_list(g)

    for item in vertices:
        if g.indegree(item) not in range(start, stop):
            g.delete_vertices(item)
    return g


# Dla danego grafu, funkcja filtruje te wierzchołki których stopień wchodzący
# jest zgodny z podanym zakresem(start, stop).
# Jeśli stop jest zostawiony domyślnie to przyjmujewartość największego możliwego stopnia wychodzącego.
def outdegree_filter(g, start=0, stop=0):
    g.as_directed()
    if stop == 0:
        stop = g.maxdegree()
    vertices = get_vertex_list(g)

    for item in vertices:
        if g.outdegree(item) not in range(start, stop):
            g.delete_vertices(item)
    return g


# Funkcja przyjmuje graf i z danego grafu zwraca listę tupli
# składających się z wierzchołków należących do tego samej społeczności
# wykrytej za pomocą algorytmu Girvan'a–Newman'a
def newman(g):
    g = g.as_undirected()
    vertex = get_vertex_list(g)

    # wytworzenie dendogramu
    d = g.community_edge_betweenness()
    p = d.as_clustering()

    out_clusters = []
    for cluster in p:
        lista = []
        for item in cluster:
            lista.append(vertex[item])
        output_tuple = tuple(lista)
        out_clusters.append(output_tuple)

    return out_clusters


def final_graph(username):
    edges = user_graph_data(username)
    # print(edges)
    vertecies = list(set([item for t in edges for item in t]))
    g = Graph(directed=True)
    g.add_vertices(vertecies)
    g.add_edges(edges)

    return g

# Dla danego grafu, funkcja zwraca zagnieżdżoną listę tupli:
# [[(lista wierzchołków, przyporządkowanie do społeczności)],[(krawędzie)]]
def final_social_data(g):
    out_edges = get_edge_list(g)
    out_vertex = []
    cluster_index = 1
    for tuple in newman(g):
        for item in tuple:
            out_vertex.append((item, cluster_index))
        cluster_index += 1

    return [out_vertex, out_edges]


import networkx as nx
from networkx.algorithms import community as nxcom
import matplotlib.pyplot as plt
import pandas as pd
import os


edges_path = r'C:\Users\micha\PycharmProjects\instagraph 3.0\data\edges\\'

main_list=['mikeshehad', 'nawrocenie','_kubawilk_', 'rzibi', 'wervel', 'zuciezaleczka']


def creating_dataframe(list):
    base_df = {'Source':[], 'Target':[]}
    base_df = pd.DataFrame(base_df, index=None)
    for item in list:
        if os.path.exists(edges_path + item + '_edges.csv'):
            df = pd.read_csv(edges_path + item + '_edges.csv')
            base_df = pd.concat([base_df, df], ignore_index=True)
    return (base_df)
    #base_df.to_csv('nice.csv')


G = nx.from_pandas_edgelist(creating_dataframe(main_list), 'Source', 'Target', create_using=nx.DiGraph())


print(G.out_degree())

def d_out_filter(G, x,y):
    main_list = [node for node, degree in dict(G.out_degree()).items() if degree not in range(x, y)]
    G.remove_nodes_from(main_list)
    return G


def d_in_filter(G, x,y):
    main_list = [node for node, degree in dict(G.in_degree()).items() if degree not in range(x, y)]
    G.remove_nodes_from(main_list)
    return G


def d_filter(G, x,y):
    main_list = [node for node, degree in dict(G.degree()).items() if degree not in range(x, y)]
    G.remove_nodes_from(main_list)
    return G

d_out_filter(G, 3, 10000)
for n1,n2,attr in G.edges(data=True):
    print (n1,n2,attr)
# m = sum([d.get('weight', 1) for u, v, d in G.edges(data=True)])
# print(m)

print(G.nodes())


communities = sorted(nxcom.greedy_modularity_communities(G), key=len, reverse=True)

print(communities)
# Author: Surinder Matharu
# Date Last Modified: 09-Nov-2026
# Purpose: 

import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 

def MyMinimumSpannigTree(Graph) -> nx.Graph:
    mst = nx.Graph()
    mst.add_nodes_from(Graph.nodes())
    route_history = [mst.copy()]

    parent = {node: node for node in Graph.nodes}
    rank = {node: 0 for node in Graph.nodes}

    def find (node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    for i, j, data in sorted (
        Graph.edges(data=True), key=lambda edge: edge[2].get('weight', 1)
    ):
        r_i, r_j = find(i), find (j)
        if r_i != r_j:
            mst.add_edge(i, j, **data)
            route_history.append(mst.copy())
            if rank[r_i] < rank[r_j]:
                parent[r_i] = r_j
            elif rank[r_i] > rank[r_j]:
                parent[r_j] = r_i 
            else:
                parent[r_j] = r_i
                rank[r_i] += 1

    return route_history

if __name__ == '__main__':
    def exampleMST1():
    # Produce empty graph
        mst_1 = nx.Graph()
        mst_1.add_nodes_from(['A','B','C','D', 'E', 'F'])
        mst_1.add_weighted_edges_from([
            ('A','B', 2), ('A','D', 3), ('A','E', 4), 
            ('B','C', 1), ('B','E', 2), ('B','F', 5),
            ('C','F', 6), ('C','E', 4),
            ('D','B', 3), ('D','E', 4), 
            ('E','F', 7)])

        return mst_1
    #pass # return networkx graph
   
    # def exampleMST2():
    #     # Produce empty graph
    #     mst_2 = nx.Graph()
    #     mst_2.add_nodes_from(['A','B','C','D', 'E'])
    #     mst_2.add_weighted_edges_from([
    #         ('A','B', 1), ('A','D', 4), ('A','E', 3), 
    #         ('B','C', 5), ('B','E', 6), 
    #         ('C','E', 2),
    #         ('D','B', 2), ('D','E', 7),])
            
    #     return mst_2    

    # def exampleMST3():
    #     mst_3 = nx.Graph()
    #     mst_3.add_nodes_from(['A','B','C','D', 'E'])
    #     mst_3.add_weighted_edges_from([
    #         ('A','B', 3), ('A','D',4), 
    #         ('B','C', 5), ('B','D',1), ('B','E',8),
    #         ('D','C', 7), ('D','E',6),
    #         ('C','E', 2)])
        
    #     return mst_3    

    mst_flow = MyMinimumSpannigTree(exampleMST1())  # Only call one at a time
    print('Edges present in the MST:')
    for edge in mst_flow[-1].edges(data=True):
        print(edge)

    fig, ax = plt.subplots(figsize=(8,8))
    graph = exampleMST1()
    mst_1 = mst_flow[-1]
    pos_1 = nx.circular_layout(graph)

    # Animate over the edges of the graph
    mst_edges = list(mst_1.edges())
    edge_labels = nx.get_edge_attributes(mst_1, 'weight')

    def update(frame):
        ax.clear()
        nx.draw(mst_1, pos_1, with_labels=True, ax=ax, node_color='lightgray', edge_color='lightgray', node_size=1000)
        nx.draw_networkx_edge_labels(mst_1, pos_1, ax=ax, edge_labels=edge_labels, bbox=dict(boxstyle='round,pad=0.3', ec='gray', fc='white', alpha=0.8))

        current_mst = mst_flow[frame]
        current_edge_labels =nx.get_edge_attributes(current_mst, 'weight')

        nx.draw(mst_1, pos_1, with_labels=True, ax=ax, node_color='lightgray', edge_color='lightgray', node_size=500)
        nx.draw_networkx_edge_labels(current_mst, pos_1, ax=ax, edge_labels=current_edge_labels)
        ax.set_title(f'Kruskal {frame + 1} of {len(mst_flow)}')

    animation = FuncAnimation(
        fig,
        update,
        frames=len(mst_flow),
        interval=1000,
        repeat=False,
    )
    # Animation frames are saved as a GIF within the kruskal_graphs folder.
    dir_save = os.path.join("kruskal_graphs")
    os.makedirs(dir_save, exist_ok=True) 
    filename = os.path.join(dir_save, "kruskal_mst.gif")
    print(f"Saving {len(mst_flow)} frames as GIF may take a while. Please be patient...")
    animation.save(filename, writer='pillow', fps=20)
    print(f'Kruskal Minimum Spanning Tree saved to: {filename}')
    plt.show()

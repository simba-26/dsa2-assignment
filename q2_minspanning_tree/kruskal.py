# Author: Surinder Matharu
# Date Last Modified: 12-Nov-2026
# Purpose: 
# References: 

import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 

# Implementation of the Kruskal Algorithm
def MyMinimumSpannigTree(Graph) -> nx.Graph:
    # Foundation block: This lays the groundwork for constructing the MSTs. 
    #                   Intially, it creates a blank slate by creating an empty nx graph.
    #                   It then extracts all nodes from the original graph inputs (i.e. exampleMST1, 2 or 3) and copies them into the mst variable.                     
    mst = nx.Graph()
    mst.add_nodes_from(Graph.nodes(data=True))
    route_history = []

   # In Kruskal's algorithm, a disjoint-set union/union by rank structure helps effciently detect cycles. 
   # parent = nx supports flexible lables (e.g. A, B, C - as illustrated in below mst examples, so a dictionary lets each node serve as its own key.
   # rank = tree height. Initally set to zero, it ensures smaller trees attach below the tall ones when sets merge, keeping trees flat.
    parent = {node: node for node in Graph.nodes}
    rank = {node: 0 for node in Graph.nodes}

    # Path compression: Checks current node, if it does not equal parent node it recursively travels up the path to find parent. 
    #                   It then points each node along the path directly to it, flattening the tree and speeding up futurenlookups.
    def find (node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    # Critical step in Kruskal's greedy algorithm. This sorts the graph edges by weight in ascending order. The lambda function extracts each tuple's third
    # element as its weight, defaulting to 1 if missing to prevent errors. A for loop was used to process the sorted edges one by one. 
    for i, j, data in sorted (
        Graph.edges(data=True), key=lambda edge: edge[2].get('weight', 1)
    ):
        r_i, r_j = find(i), find (j)
        if r_i != r_j:                       # Checking cycles: Connecting nodes with different parents so no cycles are created.
            mst.add_edge(i, j, **data)
            route_history.append(mst.copy()) # At each step, this prompts the algorithm to capture snapshots of the graph as it is constructed.
            if rank[r_i] < rank[r_j]:
                parent[r_i] = r_j
            elif rank[r_i] > rank[r_j]:      # ELIF: Rank union: If tree i is taller than tree j, attach j beneath i as its child.
                parent[r_j] = r_i 
            else:                            # ELSE: Equal union: If i and j have the same height, either can be attached under the other. Increment tree i's height by 1. 
                parent[r_j] = r_i
                rank[r_i] += 1

    # Returns history list after each loop has completed.
    return route_history

# This ensures the tests blocks, animation, print statements run when the script is executed manually.
if __name__ == '__main__':

    # Example 1: 6 nodes and 11 edges
    def exampleMST1():
        mst_1 = nx.Graph() # Produce empty graph
        mst_1.add_nodes_from(['A','B','C','D', 'E', 'F']) # Creating 6 nodes from A-F
        mst_1.add_weighted_edges_from([                   # Creating 11 weighted edges
            ('A','B', 2), ('A','D', 3), ('A','E', 4), 
            ('B','C', 1), ('B','E', 2), ('B','F', 5),
            ('C','F', 6), ('C','E', 4),
            ('D','B', 3), ('D','E', 4), 
            ('E','F', 7)])
    
        return mst_1

   # Example 2: 5 Nodes and 8 Edges
    def exampleMST2():
        mst_2 = nx.Graph()
        mst_2.add_nodes_from(['A','B','C','D', 'E'])
        mst_2.add_weighted_edges_from([
           ('A','B', 1), ('A','D', 4), ('A','E', 3), 
           ('B','C', 5), ('B','E', 6), 
           ('C','E', 2),
           ('D','B', 2), ('D','E', 7),])
            
        return mst_2    
    
    # Example 3: 5 Nodes and 8 Edges
    def exampleMST3():
        mst_3 = nx.Graph()
        mst_3.add_nodes_from(['A','B','C','D', 'E'])
        mst_3.add_weighted_edges_from([
             ('A','B', 3), ('A','D',4), 
             ('B','C', 5), ('B','D',1), ('B','E',8),
             ('D','C', 7), ('D','E',6),
             ('C','E', 2)])
        
        return mst_3

    # This runs the tests automatically, one after the other.
    graph_tests = {
            'kruskal_mst_1': exampleMST1(),
            'kruskal_mst_2': exampleMST2(),
            'kruskal_mst_3': exampleMST3()
        }

    # For loop through graph tests and print: 
    #   The test case name in terminal.
    #   The edges in the final MSTs after running the Kruskal algorithm
    for name, graph in graph_tests.items():
        print(f'RUNNING {name}')
        route_history = MyMinimumSpannigTree(graph)

        print('Edges present in the MST:')
        for edge in route_history[-1].edges(data=True): 
            print(edge)

        # Relies on plt and nx to generate graphs and animation display
        fig, ax = plt.subplots(figsize=(8,8))
        graph = graph.copy()
        mst_graph = route_history[-1]
        pos = nx.circular_layout(graph) # Circular layout is fixed for all nodes

        # Animate over the edges of the graph
        mst_edges = list(mst_graph.edges())
        edge_labels = nx.get_edge_attributes(mst_graph, 'weight')

        def update(frame):
            ax.clear()
            # Sketches the nodes in lightgray circles.
            nx.draw(mst_graph, pos, with_labels=True, ax=ax, node_color='lightgray', edge_color='lightgray', node_size=1000)
            nx.draw_networkx_labels (graph, pos, ax=ax, font_weight='bold')
            
            # Sketch out the orginal edges with dashed lines
            nx.draw_networkx_edges(graph, pos, ax=ax, edge_color='lightgray', width=1.5, style='dashed')

            # Accumulates total MST state up to current frame (snapshot)
            current_mst = route_history[frame]

            # Incrementally draws labels and edges - The selected Kruskal edges are sketched in black with weights illustarted in boxes.
            if current_mst.edges():
                nx.draw_networkx_edges(current_mst, pos, ax=ax, width=2, edge_color='black')
                current_edge_labels = nx.get_edge_attributes(current_mst, 'weight')
                nx.draw_networkx_edge_labels(current_mst, pos, ax=ax, edge_labels=current_edge_labels, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='black'))
                
                # Sets frame titles 
                ax.set_title(f'Kruskal {frame} of {len(route_history) -1}')

        # Intialises animation sequence
        animation = FuncAnimation(
            fig,
            update,
            frames=len(route_history),
            interval=1000,
            repeat=False,
        )
        # Animation frames are saved as a GIF within the kruskal_graphs folder.
        dir_save = os.path.join("kruskal_graphs")
        os.makedirs(dir_save, exist_ok=True) 
        filename = os.path.join(dir_save, f"{name}.gif")
        print(f"Saving {len(route_history)} frames as GIF may take a while. Please be patient...")
        animation.save(filename, writer='pillow', fps=20)
        print(f'Kruskal Minimum Spanning Tree saved to: {filename}')
        plt.show()


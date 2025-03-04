import matplotlib.pyplot as plt
import numpy as np
from collections import deque

# Define the graph structure
graph = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'E'],
    'C': ['A', 'F', 'K'],
    'D': ['A', 'J'],
    'E': ['B', 'G', 'K'],
    'F': ['C', 'I'],
    'G': ['E', 'H'],
    'H': ['G', 'K'],
    'I': ['F', 'J', 'K'],
    'J': ['D', 'I'],
    'K': ['C', 'E', 'H', 'I']
}

# Node positions for visualization
node_positions = {
    'A': (5, 10),
    'B': (2, 7),
    'C': (5, 7),
    'D': (8, 7),
    'E': (3.5, 4),
    'F': (6.5, 4),
    'G': (2, 1),
    'H': (4, 1),
    'I': (6, 1),
    'J': (8, 1),
    'K': (5, 0)
}

def draw_graph():
    """Draw the graph with matplotlib"""
    plt.figure(figsize=(10, 8))
    
    # Draw edges
    for node, neighbors in graph.items():
        x1, y1 = node_positions[node]
        for neighbor in neighbors:
            x2, y2 = node_positions[neighbor]
            plt.plot([x1, x2], [y1, y2], 'k-', zorder=1)
    
    # Draw nodes
    for node, (x, y) in node_positions.items():
        plt.plot(x, y, 'o', markersize=30, color='white', markeredgecolor='black', zorder=2)
        plt.text(x, y, node, fontsize=14, ha='center', va='center', zorder=3)
    
    plt.title('Graph Visualization')
    plt.axis('off')
    plt.tight_layout()
    return plt.gcf()

def find_all_paths(start, end, path=[]):
    """Find all paths from start to end node using DFS"""
    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for neighbor in graph[start]:
        if neighbor not in path:
            new_paths = find_all_paths(neighbor, end, path)
            paths.extend(new_paths)
    return paths

def find_all_cycles(start):
    """Find all cycles that start and end at the given node"""
    cycles = []
    queue = deque([(start, [start])])
    
    while queue:
        node, path = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor == start and len(path) > 2:
                cycles.append(path + [start])
            elif neighbor not in path:
                queue.append((neighbor, path + [neighbor]))
    
    return cycles

def find_shortest_circuit(start, end):
    """Find the shortest circuit from start to end and back to start"""
    paths = find_all_paths(start, end)
    if not paths:
        return None
    
    circuits = []
    for path in paths:
        # Check if end can connect back to start (completing the circuit)
        if start in graph[end]:
            circuits.append(path + [start])
    
    if not circuits:
        return None
    
    # Return the shortest circuit
    return min(circuits, key=len)

def find_longest_circuit(start, end):
    """Find the longest circuit from start to end and back to start"""
    paths = find_all_paths(start, end)
    if not paths:
        return None
    
    circuits = []
    for path in paths:
        # Check if end can connect back to start (completing the circuit)
        if start in graph[end]:
            circuits.append(path + [start])
    
    if not circuits:
        return None
    
    # Return the longest circuit
    return max(circuits, key=len)

def visualize_path(path, title):
    """Visualize a path on the graph"""
    plt.figure(figsize=(10, 8))
    
    # Draw all edges in light gray
    for node, neighbors in graph.items():
        x1, y1 = node_positions[node]
        for neighbor in neighbors:
            x2, y2 = node_positions[neighbor]
            plt.plot([x1, x2], [y1, y2], 'lightgray', zorder=1)
    
    # Draw path edges in red and thicker
    for i in range(len(path) - 1):
        x1, y1 = node_positions[path[i]]
        x2, y2 = node_positions[path[i+1]]
        plt.plot([x1, x2], [y1, y2], 'r-', linewidth=3, zorder=2)
    
    # Draw nodes
    for node, (x, y) in node_positions.items():
        if node in path:
            color = 'lightblue' if node == path[0] or node == path[-1] else 'white'
            plt.plot(x, y, 'o', markersize=30, color=color, markeredgecolor='black', zorder=3)
        else:
            plt.plot(x, y, 'o', markersize=30, color='white', markeredgecolor='black', zorder=3)
        plt.text(x, y, node, fontsize=14, ha='center', va='center', zorder=4)
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    return plt.gcf()

def main():
    """Main function to solve the challenge"""
    print("Challenge 3 Results:\n")
    
    # Draw the original graph
    graph_fig = draw_graph()
    graph_fig.savefig('graph.png')
    
    # 1. All possible paths from A to K
    paths_A_to_K = find_all_paths('A', 'K')
    print(f"1. Semua kemungkinan Path dari A ke K ({len(paths_A_to_K)} paths):")
    for i, path in enumerate(paths_A_to_K, 1):
        print(f"   Path {i}: {' -> '.join(path)}")
    
    # Visualize one of the paths
    if paths_A_to_K:
        path_fig = visualize_path(paths_A_to_K[0], "Path dari A ke K")
        path_fig.savefig('path_A_to_K.png')
    
    print()
    
    # 2. All possible paths from G to J
    paths_G_to_J = find_all_paths('G', 'J')
    print(f"2. Semua kemungkinan Path dari G ke J ({len(paths_G_to_J)} paths):")
    for i, path in enumerate(paths_G_to_J, 1):
        print(f"   Path {i}: {' -> '.join(path)}")
    
    if paths_G_to_J:
        path_fig = visualize_path(paths_G_to_J[0], "Path dari G ke J")
        path_fig.savefig('path_G_to_J.png')
    
    print()
    
    # 3. All possible paths from E to F
    paths_E_to_F = find_all_paths('E', 'F')
    print(f"3. Semua kemungkinan Path dari E ke F ({len(paths_E_to_F)} paths):")
    for i, path in enumerate(paths_E_to_F, 1):
        print(f"   Path {i}: {' -> '.join(path)}")
    
    if paths_E_to_F:
        path_fig = visualize_path(paths_E_to_F[0], "Path dari E ke F")
        path_fig.savefig('path_E_to_F.png')
    
    print()
    
    # 4. All possible cycles if A is the starting point
    cycles_A = find_all_cycles('A')
    print(f"4. Semua kemungkinan Cycle jika A adalah titik awal ({len(cycles_A)} cycles):")
    for i, cycle in enumerate(cycles_A, 1):
        print(f"   Cycle {i}: {' -> '.join(cycle)}")
    
    if cycles_A:
        cycle_fig = visualize_path(cycles_A[0], "Cycle dengan A sebagai titik awal")
        cycle_fig.savefig('cycle_A.png')
    
    print()
    
    # 5. All possible cycles if K is the starting point
    cycles_K = find_all_cycles('K')
    print(f"5. Semua kemungkinan Cycle jika K adalah titik awal ({len(cycles_K)} cycles):")
    for i, cycle in enumerate(cycles_K, 1):
        print(f"   Cycle {i}: {' -> '.join(cycle)}")
    
    if cycles_K:
        cycle_fig = visualize_path(cycles_K[0], "Cycle dengan K sebagai titik awal")
        cycle_fig.savefig('cycle_K.png')
    
    print()
    
    # 6. Shortest and longest circuit from A to K
    shortest_circuit_A_K = find_shortest_circuit('A', 'K')
    longest_circuit_A_K = find_longest_circuit('A', 'K')
    
    print("6. Circuit terpendek dan terpanjang dari A ke K:")
    if shortest_circuit_A_K:
        print(f"   Circuit terpendek: {' -> '.join(shortest_circuit_A_K)} (panjang: {len(shortest_circuit_A_K)-1})")
        circuit_fig = visualize_path(shortest_circuit_A_K, "Circuit terpendek dari A ke K")
        circuit_fig.savefig('shortest_circuit_A_to_K.png')
    else:
        print("   Tidak ada circuit dari A ke K")
    
    if longest_circuit_A_K:
        print(f"   Circuit terpanjang: {' -> '.join(longest_circuit_A_K)} (panjang: {len(longest_circuit_A_K)-1})")
        circuit_fig = visualize_path(longest_circuit_A_K, "Circuit terpanjang dari A ke K")
        circuit_fig.savefig('longest_circuit_A_to_K.png')
    
    print()
    
    # 7. Shortest and longest circuit from G to J
    shortest_circuit_G_J = find_shortest_circuit('G', 'J')
    longest_circuit_G_J = find_longest_circuit('G', 'J')
    
    print("7. Circuit terpendek dan terpanjang dari G ke J:")
    if shortest_circuit_G_J:
        print(f"   Circuit terpendek: {' -> '.join(shortest_circuit_G_J)} (panjang: {len(shortest_circuit_G_J)-1})")
        circuit_fig = visualize_path(shortest_circuit_G_J, "Circuit terpendek dari G ke J")
        circuit_fig.savefig('shortest_circuit_G_to_J.png')
    else:
        print("   Tidak ada circuit dari G ke J")
    
    if longest_circuit_G_J:
        print(f"   Circuit terpanjang: {' -> '.join(longest_circuit_G_J)} (panjang: {len(longest_circuit_G_J)-1})")
        circuit_fig = visualize_path(longest_circuit_G_J, "Circuit terpanjang dari G ke J")
        circuit_fig.savefig('longest_circuit_G_to_J.png')
    
    print()
    
    # 8. Shortest and longest circuit from E to F
    shortest_circuit_E_F = find_shortest_circuit('E', 'F')
    longest_circuit_E_F = find_longest_circuit('E', 'F')
    
    print("8. Circuit terpendek dan terpanjang dari E ke F:")
    if shortest_circuit_E_F:
        print(f"   Circuit terpendek: {' -> '.join(shortest_circuit_E_F)} (panjang: {len(shortest_circuit_E_F)-1})")
        circuit_fig = visualize_path(shortest_circuit_E_F, "Circuit terpendek dari E ke F")
        circuit_fig.savefig('shortest_circuit_E_to_F.png')
    else:
        print("   Tidak ada circuit dari E ke F")
    
    if longest_circuit_E_F:
        print(f"   Circuit terpanjang: {' -> '.join(longest_circuit_E_F)} (panjang: {len(longest_circuit_E_F)-1})")
        circuit_fig = visualize_path(longest_circuit_E_F, "Circuit terpanjang dari E ke F")
        circuit_fig.savefig('longest_circuit_E_to_F.png')
    
    print("\nSemua hasil telah divisualisasikan dan disimpan sebagai file gambar.")

if __name__ == "__main__":
    main()
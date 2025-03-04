import matplotlib.pyplot as plt
import numpy as np
from collections import deque

# Define the graph structure for Challenge 2
graph = {
    'A': ['B', 'D'],
    'B': ['A', 'C', 'E', 'F'],
    'C': ['B', 'F'],
    'D': ['A', 'E'],
    'E': ['B', 'D', 'F'],
    'F': ['B', 'C', 'E']
}

# Node positions for visualization
node_positions = {
    'A': (1, 3),
    'B': (3, 3),
    'C': (5, 3),
    'D': (1, 1),
    'E': (3, 1),
    'F': (5, 1)
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
    
    plt.title('Challenge 2 - Graph Visualization')
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

def visualize_multiple_paths(paths, title, max_display=6):
    """Visualize multiple paths on separate subplots"""
    n_paths = min(len(paths), max_display)
    rows = (n_paths + 1) // 2  # Calculate number of rows needed
    
    fig, axes = plt.subplots(rows, 2, figsize=(16, 6 * rows))
    fig.suptitle(title, fontsize=16)
    
    # Handle the case of a single row
    if rows == 1:
        axes = [axes]
    
    for i in range(n_paths):
        row, col = i // 2, i % 2
        ax = axes[row][col]
        
        path = paths[i]
        
        # Draw all edges in light gray
        for node, neighbors in graph.items():
            x1, y1 = node_positions[node]
            for neighbor in neighbors:
                x2, y2 = node_positions[neighbor]
                ax.plot([x1, x2], [y1, y2], 'lightgray', zorder=1)
        
        # Draw path edges in red and thicker
        for j in range(len(path) - 1):
            x1, y1 = node_positions[path[j]]
            x2, y2 = node_positions[path[j+1]]
            ax.plot([x1, x2], [y1, y2], 'r-', linewidth=3, zorder=2)
        
        # Draw nodes
        for node, (x, y) in node_positions.items():
            if node in path:
                color = 'lightblue' if node == path[0] or node == path[-1] else 'white'
                ax.plot(x, y, 'o', markersize=30, color=color, markeredgecolor='black', zorder=3)
            else:
                ax.plot(x, y, 'o', markersize=30, color='white', markeredgecolor='black', zorder=3)
            ax.text(x, y, node, fontsize=14, ha='center', va='center', zorder=4)
        
        ax.set_title(f"Path {i+1}: {' → '.join(path)}")
        ax.axis('off')
    
    # Hide any unused subplots
    for i in range(n_paths, rows * 2):
        row, col = i // 2, i % 2
        if row < len(axes) and col < len(axes[0]):
            axes[row][col].axis('off')
    
    plt.tight_layout(rect=[0, 0, 1, 0.97])  # Make room for suptitle
    return fig

def main():
    """Main function to solve Challenge 2"""
    print("Challenge 2 Results:\n")
    
    # Draw the original graph
    graph_fig = draw_graph()
    graph_fig.savefig('challenge2_graph.png')
    plt.close(graph_fig)
    
    # 1. All possible paths from A to C
    paths_A_to_C = find_all_paths('A', 'C')
    print(f"1. Semua kemungkinan Path dari A ke C ({len(paths_A_to_C)} paths):")
    for i, path in enumerate(paths_A_to_C, 1):
        print(f"   Path {i}: {' → '.join(path)}")
    
    # Visualize paths from A to C
    if paths_A_to_C:
        multi_path_fig = visualize_multiple_paths(paths_A_to_C, "Semua Path dari A ke C")
        multi_path_fig.savefig('challenge2_all_paths_A_to_C.png')
        plt.close(multi_path_fig)
        
        # Also visualize first path for example
        path_fig = visualize_path(paths_A_to_C[0], "Contoh Path dari A ke C")
        path_fig.savefig('challenge2_example_path_A_to_C.png')
        plt.close(path_fig)
    
    print()
    
    # 2. All possible cycles if C is the starting point
    cycles_C = find_all_cycles('C')
    print(f"2. Semua kemungkinan Cycle jika C adalah titik awal ({len(cycles_C)} cycles):")
    for i, cycle in enumerate(cycles_C, 1):
        print(f"   Cycle {i}: {' → '.join(cycle)}")
    
    # Visualize cycles starting from C
    if cycles_C:
        multi_cycle_fig = visualize_multiple_paths(cycles_C, "Semua Cycle dengan C sebagai titik awal")
        multi_cycle_fig.savefig('challenge2_all_cycles_C.png')
        plt.close(multi_cycle_fig)
        
        # Also visualize first cycle for example
        cycle_fig = visualize_path(cycles_C[0], "Contoh Cycle dengan C sebagai titik awal")
        cycle_fig.savefig('challenge2_example_cycle_C.png')
        plt.close(cycle_fig)
    
    print()
    
    # 3. All possible cycles if B is the starting point
    cycles_B = find_all_cycles('B')
    print(f"3. Semua kemungkinan Cycle jika B adalah titik awal ({len(cycles_B)} cycles):")
    for i, cycle in enumerate(cycles_B, 1):
        print(f"   Cycle {i}: {' → '.join(cycle)}")
    
    # Visualize cycles starting from B
    if cycles_B:
        multi_cycle_fig = visualize_multiple_paths(cycles_B, "Semua Cycle dengan B sebagai titik awal")
        multi_cycle_fig.savefig('challenge2_all_cycles_B.png')
        plt.close(multi_cycle_fig)
        
        # Also visualize first cycle for example
        cycle_fig = visualize_path(cycles_B[0], "Contoh Cycle dengan B sebagai titik awal")
        cycle_fig.savefig('challenge2_example_cycle_B.png')
        plt.close(cycle_fig)
    
    print()
    
    # 4. Shortest and longest circuit from A to C
    shortest_circuit_A_C = find_shortest_circuit('A', 'C')
    longest_circuit_A_C = find_longest_circuit('A', 'C')
    
    print("4. Circuit terpendek dan terpanjang dari A ke C:")
    if shortest_circuit_A_C:
        print(f"   Circuit terpendek: {' → '.join(shortest_circuit_A_C)} (panjang: {len(shortest_circuit_A_C)-1})")
        circuit_fig = visualize_path(shortest_circuit_A_C, "Circuit terpendek dari A ke C")
        circuit_fig.savefig('challenge2_shortest_circuit_A_to_C.png')
        plt.close(circuit_fig)
    else:
        print("   Tidak ada circuit dari A ke C")
    
    if longest_circuit_A_C:
        print(f"   Circuit terpanjang: {' → '.join(longest_circuit_A_C)} (panjang: {len(longest_circuit_A_C)-1})")
        circuit_fig = visualize_path(longest_circuit_A_C, "Circuit terpanjang dari A ke C")
        circuit_fig.savefig('challenge2_longest_circuit_A_to_C.png')
        plt.close(circuit_fig)
    
    print("\nSemua hasil telah divisualisasikan dan disimpan sebagai file gambar.")

    # Create a summary visualization with all key findings
    plt.figure(figsize=(15, 10))
    plt.suptitle('Challenge 2 - Rangkuman Hasil', fontsize=18)
    
    # Layout grid
    grid = plt.GridSpec(2, 2, wspace=0.3, hspace=0.4)
    
    # 1. First subplot - Graph
    ax1 = plt.subplot(grid[0, 0])
    for node, neighbors in graph.items():
        x1, y1 = node_positions[node]
        for neighbor in neighbors:
            x2, y2 = node_positions[neighbor]
            ax1.plot([x1, x2], [y1, y2], 'k-', zorder=1)
    
    for node, (x, y) in node_positions.items():
        ax1.plot(x, y, 'o', markersize=30, color='white', markeredgecolor='black', zorder=2)
        ax1.text(x, y, node, fontsize=14, ha='center', va='center', zorder=3)
    
    ax1.set_title('Graf Challenge 2')
    ax1.axis('off')
    
    # 2. Example path from A to C
    ax2 = plt.subplot(grid[0, 1])
    if paths_A_to_C:
        path = paths_A_to_C[0]
        
        # Draw all edges in light gray
        for node, neighbors in graph.items():
            x1, y1 = node_positions[node]
            for neighbor in neighbors:
                x2, y2 = node_positions[neighbor]
                ax2.plot([x1, x2], [y1, y2], 'lightgray', zorder=1)
        
        # Draw path edges in red and thicker
        for i in range(len(path) - 1):
            x1, y1 = node_positions[path[i]]
            x2, y2 = node_positions[path[i+1]]
            ax2.plot([x1, x2], [y1, y2], 'r-', linewidth=3, zorder=2)
        
        # Draw nodes
        for node, (x, y) in node_positions.items():
            if node in path:
                color = 'lightblue' if node == path[0] or node == path[-1] else 'white'
                ax2.plot(x, y, 'o', markersize=30, color=color, markeredgecolor='black', zorder=3)
            else:
                ax2.plot(x, y, 'o', markersize=30, color='white', markeredgecolor='black', zorder=3)
            ax2.text(x, y, node, fontsize=14, ha='center', va='center', zorder=4)
    
    ax2.set_title(f'Contoh Path dari A ke C: {" → ".join(path)}')
    ax2.axis('off')
    
    # 3. Example cycle from C
    ax3 = plt.subplot(grid[1, 0])
    if cycles_C:
        path = cycles_C[0]
        
        # Draw all edges in light gray
        for node, neighbors in graph.items():
            x1, y1 = node_positions[node]
            for neighbor in neighbors:
                x2, y2 = node_positions[neighbor]
                ax3.plot([x1, x2], [y1, y2], 'lightgray', zorder=1)
        
        # Draw path edges in red and thicker
        for i in range(len(path) - 1):
            x1, y1 = node_positions[path[i]]
            x2, y2 = node_positions[path[i+1]]
            ax3.plot([x1, x2], [y1, y2], 'r-', linewidth=3, zorder=2)
        
        # Draw nodes
        for node, (x, y) in node_positions.items():
            if node in path:
                color = 'lightblue' if node == path[0] or node == path[-1] else 'white'
                ax3.plot(x, y, 'o', markersize=30, color=color, markeredgecolor='black', zorder=3)
            else:
                ax3.plot(x, y, 'o', markersize=30, color='white', markeredgecolor='black', zorder=3)
            ax3.text(x, y, node, fontsize=14, ha='center', va='center', zorder=4)
    
    ax3.set_title(f'Contoh Cycle dengan C sebagai titik awal: {" → ".join(cycles_C[0])}' if cycles_C else 'Tidak ada cycle dengan C sebagai titik awal')
    ax3.axis('off')
    
    # 4. Circuit from A to C
    ax4 = plt.subplot(grid[1, 1])
    if shortest_circuit_A_C:
        path = shortest_circuit_A_C
        
        # Draw all edges in light gray
        for node, neighbors in graph.items():
            x1, y1 = node_positions[node]
            for neighbor in neighbors:
                x2, y2 = node_positions[neighbor]
                ax4.plot([x1, x2], [y1, y2], 'lightgray', zorder=1)
        
        # Draw path edges in red and thicker
        for i in range(len(path) - 1):
            x1, y1 = node_positions[path[i]]
            x2, y2 = node_positions[path[i+1]]
            ax4.plot([x1, x2], [y1, y2], 'r-', linewidth=3, zorder=2)
        
        # Draw nodes
        for node, (x, y) in node_positions.items():
            if node in path:
                color = 'lightblue' if node == path[0] or node == path[-1] else 'white'
                ax4.plot(x, y, 'o', markersize=30, color=color, markeredgecolor='black', zorder=3)
            else:
                ax4.plot(x, y, 'o', markersize=30, color='white', markeredgecolor='black', zorder=3)
            ax4.text(x, y, node, fontsize=14, ha='center', va='center', zorder=4)
    
    ax4.set_title(f'Circuit terpendek dari A ke C: {" → ".join(shortest_circuit_A_C)}' if shortest_circuit_A_C else 'Tidak ada circuit dari A ke C')
    ax4.axis('off')
    
    plt.savefig('challenge2_summary.png', dpi=150, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()
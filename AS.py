import tkinter as tk
from tkinter import messagebox
from queue import PriorityQueue

class AStarVisualization:
    def __init__(self, root, canvas_width=600, canvas_height=500):
        self.root = root
        self.root.title("A* Algorithm Visualization")

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="#f0f0f0", highlightthickness=0)
        self.canvas.pack()

        self.nodes = {'A': (50, 50), 'B': (150, 50), 'C': (225, 60),
                      'D': (70, 150), 'E': (150, 150), 'F': (220, 120),
                      'G': (50, 250), 'H': (150, 250), 'I': (250, 250),
                      'J': (350, 300), 'K': (400, 150), 'L': (550, 50),
                      'M': (550, 250), 'N': (350, 50), 'O': (450, 50),
                      'P': (250, 200), 'Q': (450, 250), 'R': (550, 150),
                      'S': (350, 350), 'T': (450, 300), 'U': (550, 350),
                      'V': (350, 450), 'W': (450, 450), 'X': (70, 450),
                      'Y': (250, 450), 'Z': (50, 400)}

        self.edges = [('A', 'B', 2), ('A', 'D', 4), ('B', 'C', 3), 
                      ('P', 'F', 1), ('B', 'E', 1), ('C', 'F', 5), 
                      ('E', 'F', 2), ('P', 'N', 4), ('C', 'T', 12),
                      ('I', 'J', 3), ('K', 'L', 4), ('W', 'S', 8),
                      ('N', 'O', 5), ('M', 'J', 2), ('H', 'I', 7),
                      ('J', 'M', 2), ('U', 'M', 15), ('G', 'V', 2),
                      ('P', 'E', 3), ('R', 'I', 2), ('Q', 'K', 15),
                      ('S', 'T', 2), ('S', 'T', 2), ('T', 'V', 4),
                      ('D', 'G', 2), ('U', 'V', 1), ('V', 'W', 2),
                      ('R', 'O', 15), ('Z', 'H', 3), ('Z', 'X', 3),
                      ('X', 'Y', 7), ('Y', 'S', 1)]

        self.start_node = tk.StringVar()
        self.end_node = tk.StringVar()

        self.red_lines = []

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Start Node:", font=("Helvetica", 12)).pack()
        start_entry = tk.Entry(self.root, textvariable=self.start_node, font=("Helvetica", 12))
        start_entry.pack()

        tk.Label(self.root, text="End Node:", font=("Helvetica", 12)).pack()
        end_entry = tk.Entry(self.root, textvariable=self.end_node, font=("Helvetica", 12))
        end_entry.pack()

        run_button = tk.Button(self.root, text="Run A*", command=self.run_astar, font=("Helvetica", 12), bg="#4caf50", fg="white")
        run_button.pack()

        reset_button = tk.Button(self.root, text="Reset", command=self.reset, font=("Helvetica", 12), bg="#f44336", fg="white")
        reset_button.pack()

        self.draw_nodes_and_edges()

    def draw_nodes_and_edges(self):
        for node, pos in self.nodes.items():
            x, y = pos
            oval = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="#2196f3", outline="#2196f3")
            text = self.canvas.create_text(x, y, text=node, font=("Helvetica", 8), fill="white")
            self.canvas.tag_raise(text)

        for edge in self.edges:
            start, end, weight = edge
            x1, y1 = self.nodes[start]
            x2, y2 = self.nodes[end]
            line = self.canvas.create_line(x1, y1, x2, y2, fill="#757575", width=1)
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            self.canvas.create_text(mid_x + 2, mid_y, text=str(weight), font=("Helvetica", 8), fill="black")
            self.canvas.tag_lower(line)

    def run_astar(self):
        self.reset()

        start_node = self.start_node.get()
        end_node = self.end_node.get()

        if start_node not in self.nodes or end_node not in self.nodes:
            messagebox.showerror("Error", "Invalid start or end node.")
            return

        path, distance = self.astar(start_node, end_node)

        if not path:
            messagebox.showinfo("Path not found", f"No path exists between {start_node} and {end_node}")
        else:
            self.highlight_shortest_path(path)
            messagebox.showinfo("Shortest Path", f"Shortest path from {start_node} to {end_node}: {' -> '.join(path)}\nDistance: {distance:.2f}")


    def astar(self, start, end):
        open = PriorityQueue()
        open.put((0, start, []))
        closed = set()

        while not open.empty():
            cost, node, path = open.get()

            if node in closed:
                continue

            closed.add(node)
            path = path + [node]

            if node == end:
                return path, cost

            for neighbor, weight in self.get_neighbors(node):
                if neighbor not in closed:
                    g_cost = cost + weight
                    h_cost = heuristic(self.nodes[neighbor], self.nodes[end])
                    f_cost = g_cost + h_cost
                    open.put((f_cost, neighbor, path))

        return [], float('infinity')

    def get_neighbors(self, node):
        return [(edge[1], edge[2]) if edge[0] == node else (edge[0], edge[2]) for edge in self.edges if node in edge[:2]]

    def highlight_shortest_path(self, path):
        for i in range(len(path) - 1):
            start_node = path[i]
            end_node = path[i + 1]
            x1, y1 = self.nodes[start_node]
            x2, y2 = self.nodes[end_node]
            line = self.canvas.create_line(x1, y1, x2, y2, fill="#f44336", width=2)
            self.canvas.tag_lower(line)
            self.red_lines.append(line)

    def reset(self):
        for line_id in self.red_lines:
            self.canvas.delete(line_id)

        self.red_lines = []


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


if __name__ == "__main__":
    root = tk.Tk()
    app = AStarVisualization(root)
    root.mainloop()

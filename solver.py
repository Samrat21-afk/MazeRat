import matplotlib.pyplot as plt
import numpy as np

#So the first step for us is to visualize the maze. In the maze.txt file, I have created something like maze where 1 denotes walls and 0 denotes blank areas from where movement is possible
maze = []
with open("maze3.txt") as f:
    for line in f:
        maze.append([int(x) for x in line.split()])

start = (0, 0)
goal = (len(maze) - 1, len(maze[0]) - 1)
print("Maze loaded:", maze)

#After we read the contents of maze.txt, the next step is to implement the idea of the process. For this, we are going to use object oriented programming. The idea is that we have a frontier which uses queue concept or the last-in first-out concept. 
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        
#In the above lines of code, we have created an object called Node, which has its attributes of state, its parent node and one or more action nodes.
class QueueFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("no solution")
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node

#This is a neighbors function 
def neighbors(state):
    row, col = state
    results = []

    if row > 0 and maze[row-1][col] == 0:
        results.append(("up", (row-1, col)))
    if row < len(maze)-1 and maze[row+1][col] == 0:
        results.append(("down", (row+1, col)))
    if col > 0 and maze[row][col-1] == 0:
        results.append(("left", (row, col-1)))
    if col < len(maze[0])-1 and maze[row][col+1] == 0:
        results.append(("right", (row, col+1)))

    return results

#we have implemented the Breadth first search, or the last in first out approach. Below is the code for the function breadth_first_search
def breadth_first_search(start, goal):
    start_node = Node(state=start, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start_node)
    explored = set()

    while True:
        node = frontier.remove()
        if node.state == goal:
            actions, cells = [], []
            while node.parent is not None:
                actions.append(node.action)
                cells.append(node.state)
                node = node.parent
            return actions[::-1], cells[::-1]  # reverse path

        explored.add(node.state)

        for action, state in neighbors(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)

#Here, we are going to implement the breadth_first_search function.
actions, cells = breadth_first_search(start, goal)
print("Solution path:", cells)

#Here, we are going to visualize the function
'''
def print_maze_with_path(maze, path):
    maze_copy = [row[:] for row in maze]
    for r, c in path:
        if (r, c) != start and (r, c) != goal:
            maze_copy[r][c] = "*"

    for r in range(len(maze_copy)):
        row_str = ""
        for c in range(len(maze_copy[0])):
            if (r, c) == start: row_str += "S "
            elif (r, c) == goal: row_str += "G "
            elif maze_copy[r][c] == 1: row_str += "# "
            elif maze_copy[r][c] == "*": row_str += "* "
            else: row_str += ". "
        print(row_str)

print_maze_with_path(maze, cells)
'''
#After finding the optimal path, here, we are visualizing the optimal path
maze_array = np.array(maze)
maze_vis = maze_array.copy()

for r, c in cells:
    maze_vis[r][c] = 2  # mark path

plt.figure(figsize=(5,5))
plt.imshow(maze_vis, cmap='gray_r')
plt.xticks([]); plt.yticks([])
plt.text(0,0,'S',color='green',ha='center',va='center',fontsize=12,fontweight='bold')
plt.text(len(maze[0])-1,len(maze)-1,'G',color='red',ha='center',va='center',fontsize=12,fontweight='bold')
plt.show()

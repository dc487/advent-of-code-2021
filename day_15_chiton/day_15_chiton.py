import pathlib
from queue import PriorityQueue

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

def run_djikstra_pathfinding(risk_matrix, starting_node, destination_node):
    width = len(risk_matrix[0])
    height = len(risk_matrix)

    x = starting_node[0]
    y = starting_node[1]

    node_queue = PriorityQueue()
    visited_nodes = set()
    visited_nodes.add(starting_node)
    
    if x - 1 >= 0:
        node = (x - 1, y)
        risk_score = risk_matrix[node[0]][node[1]]
        node_queue.put((risk_score, node))

    if y - 1 >= 0:
        node = (x, y - 1)
        risk_score = risk_matrix[node[0]][node[1]]
        node_queue.put((risk_score, node))

    if x + 1 < width:
        node = (x + 1, y)
        risk_score = risk_matrix[node[0]][node[1]]
        node_queue.put((risk_score, node))

    if y + 1 < height:
        node = (x, y + 1)
        risk_score = risk_matrix[node[0]][node[1]]
        node_queue.put((risk_score, node))

    while not node_queue.empty():
        (current_risk_score, next_node) = node_queue.get()
        if next_node in visited_nodes:
            continue

        visited_nodes.add(next_node)

        if next_node[0] == destination_node[0] and next_node[1] == destination_node[1]:
            return current_risk_score

        x = next_node[0]
        y = next_node[1]

        if x - 1 >= 0:
            node = (x - 1, y)
            if node not in visited_nodes:
                risk_score = current_risk_score + risk_matrix[node[0]][node[1]]
                node_queue.put((risk_score, node))

        if y - 1 >= 0:
            node = (x, y - 1)
            if node not in visited_nodes:
                risk_score = current_risk_score + risk_matrix[node[0]][node[1]]
                node_queue.put((risk_score, node))

        if x + 1 < width:
            node = (x + 1, y)
            if node not in visited_nodes:
                risk_score = current_risk_score + risk_matrix[node[0]][node[1]]
                node_queue.put((risk_score, node))

        if y + 1 < height:
            node = (x, y + 1)
            if node not in visited_nodes:
                risk_score = current_risk_score + risk_matrix[node[0]][node[1]]
                node_queue.put((risk_score, node))

    return 0


if __name__ == "__main__":
    input = load_input()

    risk_matrix = []
    for line in input:
        risk_line = []
        for character in line:
            risk_line.append(int(character))
        risk_matrix.append(risk_line)

    destination_node = (len(risk_matrix[0]) - 1, len(risk_matrix) - 1)
    print(run_djikstra_pathfinding(risk_matrix, (0,0), destination_node))

    for i in range(len(input)):
        line = risk_matrix[i]
        for j in range(1, 5):
            for character in input[i]:
                next_character = (int(character) + j) % 10
                if next_character < int(character):
                    next_character += 1
                line.append(next_character)

    for i in range(1, 5):
        for j in range(len(input)):
            new_line = risk_matrix[j][:]
            for k in range(len(risk_matrix[j])):
                next_character = (risk_matrix[j][k] + i) % 10
                if next_character < risk_matrix[j][k]:
                    next_character += 1
                new_line[k] = next_character

            risk_matrix.append(new_line)

    destination_node = (len(risk_matrix[0]) - 1, len(risk_matrix) - 1)
    print(run_djikstra_pathfinding(risk_matrix, (0,0), destination_node))
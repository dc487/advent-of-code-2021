import pathlib

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

if __name__ == "__main__":
    input = load_input()

    risk_matrix = []
    for line in input:
        risk_line = []
        for character in line:
            risk_line.append(int(character))
        risk_matrix.append(risk_line)

    max_distance = sum([sum(x) for x in risk_matrix])

    unvisited_nodes = {}
    for x in range(len(risk_matrix)):
        for y in range(len(risk_matrix[x])):
            unvisited_nodes[str(x) + "," + str(y)] = max_distance

    visited_nodes = {}
    current_node = (0,0)
    unvisited_nodes["0,0"] = 0

    max_x = 0
    max_y = 0

    destination_node = str(len(risk_matrix[0]) - 1) + "," + str(len(risk_matrix) - 1)
    while destination_node not in visited_nodes.keys():
        x = current_node[0]
        y = current_node[1]
        c_node = str(x) + "," + str(y)

        if (x > max_x):
            max_x = x

        if (y > max_y):
            max_y = y

        if c_node in visited_nodes.keys():
            print("help")
            break

        if x - 1 >= 0:
            node = str(x - 1) + "," + str(y)
            if node not in visited_nodes.keys():
                risk_score = unvisited_nodes[c_node] + risk_matrix[x - 1][y]
                unvisited_nodes[node] = min(risk_score, unvisited_nodes[node])

        if y - 1 >= 0:
            node = str(x) + "," + str(y - 1)
            if node not in visited_nodes.keys():
                risk_score = unvisited_nodes[c_node] + risk_matrix[x][y - 1]
                unvisited_nodes[node] = min(risk_score, unvisited_nodes[node])

        if x + 1 < len(risk_matrix[0]):
            node = str(x + 1) + "," + str(y)
            if node not in visited_nodes.keys():
                risk_score = unvisited_nodes[c_node] + risk_matrix[x + 1][y]
                unvisited_nodes[node] = min(risk_score, unvisited_nodes[node])

        if y + 1 < len(risk_matrix):
            node = str(x) + "," + str(y + 1)
            if node not in visited_nodes.keys():
                risk_score = unvisited_nodes[c_node] + risk_matrix[x][y + 1]
                unvisited_nodes[node] = min(risk_score, unvisited_nodes[node])

        visited_nodes[c_node] = unvisited_nodes[c_node]
        unvisited_nodes.pop(c_node, None)
        min_score = max_distance
        for node in unvisited_nodes.keys():
            if unvisited_nodes[node] < min_score:
                min_score = unvisited_nodes[node]
                parts = node.split(",")
                current_node = (int(parts[0]), int(parts[1]))

    print(visited_nodes[destination_node])

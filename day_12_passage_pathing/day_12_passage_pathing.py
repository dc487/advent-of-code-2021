import pathlib

class _Edge:
    def __init__(self, edge_string):
        self.edge_string = edge_string
        parts = edge_string.split("-")
        self.start = parts[0]
        self.end = parts[1]

def load_input():
    return [_Edge(x) for x in pathlib.Path("./input.txt").read_text().strip("\n").splitlines()]

def get_paths(paths, edges, current_path, visited_caves, starting_node):
    if starting_node == "end":
        current_path.append("end")
        paths.append(current_path)
        return

    if starting_node.islower():
        if starting_node in visited_caves:
            return
        
        visited_caves.add(starting_node)

    current_path.append(starting_node)
    for node in [x for x in edges if x.start == starting_node]:
        get_paths(paths, edges, current_path[:], visited_caves.copy(), node.end)

    for node in [x for x in edges if x.end == starting_node]:
        get_paths(paths, edges, current_path[:], visited_caves.copy(), node.start)

def get_paths_2(paths, edges, current_path, visited_caves, starting_node, visited_one_cave_twice):
    if starting_node == "end":
        current_path.append("end")
        paths.append(current_path)
        return

    if starting_node.islower():
        if starting_node in visited_caves:
            if visited_one_cave_twice or starting_node == "start":
                return
            else:
                visited_one_cave_twice = True
        
        visited_caves.add(starting_node)

    current_path.append(starting_node)
    for node in [x for x in edges if x.start == starting_node]:
        get_paths_2(paths, edges, current_path[:], visited_caves.copy(), node.end, visited_one_cave_twice)

    for node in [x for x in edges if x.end == starting_node]:
        get_paths_2(paths, edges, current_path[:], visited_caves.copy(), node.start, visited_one_cave_twice)

if __name__ == "__main__":
    input = load_input()

    paths = []
    get_paths(paths, input, [], set(), "start")
    print(len(paths))
    
    paths = []
    get_paths_2(paths, input, [], set(), "start", False)
    print(len(paths))

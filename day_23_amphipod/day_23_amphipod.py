import pathlib
import heapq

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

def print_state(state, pod_size):
    room_positions_char = {
        'a1': 3,
        'a2': 3,
        'a3': 3,
        'a4': 3,
        'b1': 5,
        'b2': 5,
        'b3': 5,
        'b4': 5,
        'c1': 7,
        'c2': 7,
        'c3': 7,
        'c4': 7,
        'd1': 9,
        'd2': 9,
        'd3': 9,
        'd4': 9
    }

    state_letters = {
        0: 'A',
        1: 'A',
        2: 'A',
        3: 'A',
        4: 'B',
        5: 'B',
        6: 'B',
        7: 'B',
        8: 'C',
        9: 'C',
        10: 'C',
        11: 'C',
        12: 'D',
        13: 'D',
        14: 'D',
        15: 'D'
    }

    printed_state = []
    printed_state.append("#############")
    printed_state.append("#...........#")
    printed_state.append("###.#.#.#.###")
    for i in range(pod_size - 1):
        printed_state.append("  #.#.#.#.#")
    printed_state.append("  #########")

    i = 0
    for x in state:
        if x.startswith('h'):
            position = int(x[1:])
            printed_state[1] = printed_state[1][:position] + state_letters[i] + printed_state[1][position + 1:]
        else:
            position = int(x[1:]) + 1
            printed_state[position] = printed_state[position][:room_positions_char[x]] + state_letters[i] + printed_state[position][room_positions_char[x] + 1:]
        i += 1

    for line in printed_state:
        print(line)

    print("")

def run_pathfinding(initial_state, pod_size):
    desired_locations = {
        0: 'a',
        1: 'b',
        2: 'c',
        3: 'd'
    }

    room_positions = {
        0: 3,
        1: 5,
        2: 7,
        3: 9
    }

    room_positions_char = {
        'a1': 3,
        'a2': 3,
        'a3': 3,
        'a4': 3,
        'b1': 5,
        'b2': 5,
        'b3': 5,
        'b4': 5,
        'c1': 7,
        'c2': 7,
        'c3': 7,
        'c4': 7,
        'd1': 9,
        'd2': 9,
        'd3': 9,
        'd4': 9
    }

    move_energies = {
        0: 1,
        1: 10,
        2: 100,
        3: 1000
    }

    visited_states = set()

    state_queue = []
    heapq.heappush(state_queue, (0, 0, initial_state, []))

    while len(state_queue) > 0:
        (weighting, energy, current_state, current_path) = heapq.heappop(state_queue)

        if current_state in visited_states:
            continue

        visited_states.add(current_state)

        end_condition_met = True
        for letter_index in range(4):
            desired_location = desired_locations[letter_index]
            for pod_number in range(pod_size):
                if not current_state[pod_size * letter_index + pod_number].startswith(desired_location):
                    end_condition_met = False
                    break

        if end_condition_met:
            current_path.append(current_state)
            return (energy, current_path)

        for letter_index in range(4):
            desired_location = desired_locations[letter_index]
            all_letters_in_correct_location = True
            for pod_number in range(pod_size):
                if not current_state[pod_size * letter_index + pod_number].startswith(desired_location):
                    all_letters_in_correct_location = False
                    break

            if all_letters_in_correct_location:
                continue

            # find the number of amphipods in the correct position
            min_room_position = pod_size + 1
            for room_position in range(pod_size, 0, -1):
                room_identifier = desired_location + str(room_position)
                room_filled = False
                for pod_number in range(pod_size):
                    if current_state[pod_size * letter_index + pod_number] == room_identifier:
                        room_filled = True
                        break

                if room_filled:
                    min_room_position = room_position
                else:
                    break

            for pod_number in range(pod_size):
                current_index = pod_size * letter_index + pod_number
                current_room = current_state[current_index][:1]
                current_room_position = int(current_state[current_index][1:])

                if current_room == desired_location and current_room_position >= min_room_position:
                    # we're in the correct location!
                    continue

                if current_room == 'h':
                    # we're in the hallway, and the room is available to be filled
                    canMove = True

                    # is there anything else blocking the way into the room?
                    for j in range(min_room_position - 1, 0, -1):
                        if desired_location + str(j) in current_state:
                            canMove = False
                            break

                    if canMove:
                        for j in range(room_positions[letter_index], current_room_position, 1 if room_positions[letter_index] <= current_room_position else -1):
                            if "h" + str(j) in current_state:
                                canMove = False
                                break

                    if canMove:
                        next_energy = energy + move_energies[letter_index] * (abs(current_room_position - room_positions[letter_index]) + min_room_position - 1)
                        next_weighting = next_energy
                        next_path = current_path[:] + [current_state]
                        heapq.heappush(state_queue, (next_weighting, next_energy, current_state[:current_index] + (desired_location + str(min_room_position - 1),) + current_state[current_index + 1:], next_path))

                elif current_room != 'h': 
                    # we're in the wrong room (or wrong position in right room)
                    # Move to all possible hallway positions (ultimately will be the same as moving directly to an available room)
                    # make sure there's nothing above us:

                    something_above_us = False
                    for above_room_position in range(1, current_room_position):
                        above_room = current_room + str(above_room_position)
                        if above_room in current_state:
                            # something's above us - we can't move
                            something_above_us = True
                            break

                    if something_above_us:
                        continue

                    room_position = room_positions_char[current_state[current_index]]

                    for k in range(1, 12):
                        if k == 3 or k == 5 or k == 7 or k == 9:
                            # we can't stop outside a room
                            continue
                    
                        canMove = True
                        for j in range(k, room_position, 1 if k <= room_position else -1):
                            if "h" + str(j) in current_state:
                                canMove = False
                                break
                                
                        if canMove:
                            next_energy = energy + move_energies[letter_index] * (abs(room_position - k) + int(current_room_position))
                            next_weighting = next_energy
                            next_path = current_path[:] + [current_state]
                            heapq.heappush(state_queue, (next_weighting, next_energy, current_state[:current_index] + ('h' + str(k),) + current_state[current_index + 1:], next_path))


if __name__ == "__main__":
    input = load_input()

    state = {
        'A': [],
        'B': [],
        'C': [],
        'D': []
    }

    state[input[2][3]].append('a1')
    state[input[3][3]].append('a2')
    state[input[2][5]].append('b1')
    state[input[3][5]].append('b2')
    state[input[2][7]].append('c1')
    state[input[3][7]].append('c2')
    state[input[2][9]].append('d1')
    state[input[3][9]].append('d2')

    
    (energy, current_path) = run_pathfinding((state['A'][0], state['A'][1], state['B'][0], state['B'][1], state['C'][0], state['C'][1], state['D'][0], state['D'][1]), 2)
    for state in current_path:
        print_state(state, 2)
    print(energy)

    state = {
        'A': [],
        'B': [],
        'C': [],
        'D': []
    }

    state[input[2][3]].append('a1')
    state[input[3][3]].append('a4')
    state[input[2][5]].append('b1')
    state[input[3][5]].append('b4')
    state[input[2][7]].append('c1')
    state[input[3][7]].append('c4')
    state[input[2][9]].append('d1')
    state[input[3][9]].append('d4')

    (energy, current_path) = run_pathfinding((state['A'][0], state['A'][1], 'c3', 'd2', state['B'][0], state['B'][1], 'b3', 'c2', state['C'][0], state['C'][1], 'b2', 'd3', state['D'][0], state['D'][1], 'a2', 'a3'), 4)
    for state in current_path:
        print_state(state, 4)
    print(energy)
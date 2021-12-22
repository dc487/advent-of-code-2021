import pathlib
from functools import cache

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

@cache
def play_quantum_game(player_1_position, player_2_position, player_1_score, player_2_score, current_player, next_dice_roll):
    next_player = 1

    if current_player == 1:
        player_1_position += next_dice_roll % 10
        if player_1_position > 10:
            player_1_position -= 10
        player_1_score += player_1_position

        if player_1_score >= 21:
            return (1, 0)

        next_player = 2

    else:
        player_2_position += next_dice_roll % 10
        if player_2_position > 10:
            player_2_position -= 10
        player_2_score += player_2_position

        if player_2_score >= 21:
            return (0, 1)

        next_player = 1

    return roll_quantum_dirac_dice(player_1_position, player_2_position, player_1_score, player_2_score, next_player)


def roll_quantum_dirac_dice(player_1_position, player_2_position, player_1_score, player_2_score, current_player):
    player_1_wins = 0
    player_2_wins = 0

    (next_player_1_wins, next_player_2_wins) = play_quantum_game(player_1_position, player_2_position, player_1_score, player_2_score, current_player, 3)
    player_1_wins += 1 * next_player_1_wins
    player_2_wins += 1 * next_player_2_wins

    (next_player_1_wins, next_player_2_wins) = play_quantum_game(player_1_position, player_2_position, player_1_score, player_2_score, current_player, 4)
    player_1_wins += 3 * next_player_1_wins
    player_2_wins += 3 * next_player_2_wins

    (next_player_1_wins, next_player_2_wins) = play_quantum_game(player_1_position, player_2_position, player_1_score, player_2_score, current_player, 5)
    player_1_wins += 6 * next_player_1_wins
    player_2_wins += 6 * next_player_2_wins

    (next_player_1_wins, next_player_2_wins) = play_quantum_game(player_1_position, player_2_position, player_1_score, player_2_score, current_player, 6)
    player_1_wins += 7 * next_player_1_wins
    player_2_wins += 7 * next_player_2_wins

    (next_player_1_wins, next_player_2_wins) = play_quantum_game(player_1_position, player_2_position, player_1_score, player_2_score, current_player, 7)
    player_1_wins += 6 * next_player_1_wins
    player_2_wins += 6 * next_player_2_wins

    (next_player_1_wins, next_player_2_wins) = play_quantum_game(player_1_position, player_2_position, player_1_score, player_2_score, current_player, 8)
    player_1_wins += 3 * next_player_1_wins
    player_2_wins += 3 * next_player_2_wins

    (next_player_1_wins, next_player_2_wins) = play_quantum_game(player_1_position, player_2_position, player_1_score, player_2_score, current_player, 9)
    player_1_wins += 1 * next_player_1_wins
    player_2_wins += 1 * next_player_2_wins

    return (player_1_wins, player_2_wins)

if __name__ == "__main__":
    input = load_input()

    player_1_position = int(input[0].split(" ")[-1])
    player_2_position = int(input[1].split(" ")[-1])

    player_1_score = 0
    player_2_score = 0

    losing_score = 0

    deterministic_dice_value = 1
    dice_roll_count = 0

    while True:
        player_1_roll = 3 * deterministic_dice_value + 3
        dice_roll_count += 3
        deterministic_dice_value += 3

        player_1_position += player_1_roll % 10
        if player_1_position > 10:
            player_1_position -= 10
        player_1_score += player_1_position

        if player_1_score >= 1000:
            losing_score = player_2_score
            break

        player_2_roll = 3 * deterministic_dice_value + 3
        dice_roll_count += 3
        deterministic_dice_value += 3

        player_2_position += player_2_roll % 10
        if player_2_position > 10:
            player_2_position -= 10
        player_2_score += player_2_position

        if player_2_score >= 1000:
            losing_score = player_1_score
            break

    print(losing_score * dice_roll_count)

    player_1_position = int(input[0].split(" ")[-1])
    player_2_position = int(input[1].split(" ")[-1])

    (player_1_wins, player_2_wins) = roll_quantum_dirac_dice(player_1_position, player_2_position, 0, 0, 1)
    print(max(player_1_wins, player_2_wins))


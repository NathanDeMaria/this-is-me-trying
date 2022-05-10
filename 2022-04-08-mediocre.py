"""
https://fivethirtyeight.com/features/can-you-be-mediocre-enough-to-win/
"""


def _get_final_points(b_choice: int, c_choice: int) -> dict[int, float]:
    points = [6, 8, 10]
    a_choice = 3

    choices = [a_choice, b_choice, c_choice]
    middle = sorted(choices)[1]

    round_winners = [i for i, c in enumerate(choices) if c == middle]

    winner_groups = []
    for round_winner in round_winners:
        points_copy = points.copy()
        points_copy[round_winner] += middle

        game_winning_score = sorted(points_copy)[1]
        game_winners = [i for i, c in enumerate(points_copy) if c == game_winning_score]
        winner_groups.append(game_winners)
    
    group_points = 1 / len(winner_groups)
    total_odds = {i: 0.0 for i in range(3)}
    for group in winner_groups:
        individual_points = group_points / len(group)
        for winning_player in group:
            total_odds[winning_player] += individual_points
    return total_odds


def main():
    results = []

    valid_b_choices={9, 10}
    valid_c_choices={9, 10}

    for c_choice in valid_c_choices:
        for b_choice in valid_b_choices:
            player_scores = _get_final_points(b_choice, c_choice)
            result = b_choice, c_choice, player_scores
            print(result)
            results.append(result)
        print()
    
    # b would only choose ones where b has a chance at winning
    valid_b_choices = set(b_choice for b_choice, _, player_scores in results if player_scores[1] > 0.5)
    valid_c_choices = set(c_choice for _, c_choice, player_scores in results if player_scores[2] > 0.5)
    print(f"{valid_b_choices=}")
    print(f"{valid_c_choices=}")


if __name__ == '__main__':
    main()

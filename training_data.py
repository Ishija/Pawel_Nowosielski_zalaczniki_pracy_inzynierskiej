from cards_list import cards_model, cards, combinations
import time
from tqdm import tqdm
import random


def draw_cards(n):
    return random.sample(cards, n)


def put_hands(arr, i):
    all_hands = [arr[0 + i], arr[6 + i]]
    return all_hands


def hand_set(hand, com_cards):
    drawn_cards = sorted(hand + com_cards)
    suits = [card[1] for card in drawn_cards]
    ranks = sorted(
        [int(card[:-1]) if card[:-1].isdigit() else {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[card[:-1]] for card in
         hand + com_cards])

    cards_to_set = sorted(zip(ranks, suits))
    count_straight = 1
    count_straight_flush = 1
    straight = False
    straight_flush = False

    for i in range(1, len(cards_to_set)):
        if cards_to_set[i][0] == cards_to_set[i - 1][0] + 1:
            if cards_to_set[i][1] == cards_to_set[i - 1][1]:
                count_straight_flush += 1
            count_straight += 1
        elif cards_to_set[i][0] > cards_to_set[i - 1][0] + 1:
            count_straight_flush = 1
            count_straight = 1
        if count_straight_flush >= 5:
            straight_flush = True
        elif count_straight >= 5:
            straight = True

    if ranks[0] == 2 and ranks[1] == 3 and ranks[2] == 4 and ranks[3] == 5 and ranks[6] == 14: straight = True
    if ranks[0] == 2 and ranks[1] == 3 and ranks[2] == 4 and ranks[3] == 5 and ranks[6] == 14 \
            and suits[0] == suits[1] == suits[2] == suits[3] == suits[6]: straight_flush = True

    flush = (suits.count('H') == 5 or suits.count('S') == 5 or suits.count('C') == 5 or suits.count('D') == 5)
    royal_flush = False
    if all(x in drawn_cards for x in ['TH', 'JH', 'QH', 'KH', 'AH']) or \
            all(x in drawn_cards for x in ['TD', 'JD', 'QD', 'KD', 'AD']) or \
            all(x in drawn_cards for x in ['TC', 'JC', 'QC', 'KC', 'AC']) or \
            all(x in drawn_cards for x in ['TS', 'JS', 'QS', 'KS', 'AS']):
        royal_flush = True

    counts = [ranks.count(rank) for rank in set(ranks)]
    four_of_a_kind = (4 in counts)
    full_house = (3 in counts) and (2 in counts)
    three_of_a_kind = (3 in counts) and not full_house
    two_pair = (counts.count(2) == 2)
    one_pair = (counts.count(2) == 1)
    if royal_flush:
        return 9
    elif straight_flush:
        return 8
    elif four_of_a_kind:
        return 7
    elif full_house:
        return 6
    elif flush:
        return 5
    elif straight:
        return 4
    elif three_of_a_kind:
        return 3
    elif two_pair:
        return 2
    elif one_pair:
        return 1
    else:
        return 0


def winning_set(hand_sets):
    return max(hand_sets)


with open('training_data_10k.txt', 'w') as file:
    number_of_games_per_set = 1000
    start = time.time()
    live_deck = []
    for type_of_set in range(10):
        print(combinations[type_of_set])
        live_deck_set = set()
        progress_bar = tqdm(total=number_of_games_per_set, ncols=80)
        while len(live_deck_set) < number_of_games_per_set:
            all_cards = draw_cards(17)
            hands_cards = [put_hands(all_cards, i) for i in range(6)]
            community_cards = all_cards[12:17]
            sets = [hand_set(hands_cards[j - 1], community_cards) for j in range(1, 7)]
            set_w = winning_set(sets)
            save_line = all_cards[0:16]
            save_line.append(set_w)
            if set_w == type_of_set:
                live_deck_set.add(tuple(save_line))
            progress_bar.update(1)
            progress_bar.set_description(f"Progress: {len(live_deck_set)}/{number_of_games_per_set}")
        progress_bar.close()
        live_deck += list(live_deck_set)

    for cards_data in live_deck:
        for i in range(16):
            file.write(str(cards_model[cards_data[i]]) + ' ')
        file.write(str(cards_data[16]) + '\n')

    end = time.time()
    print((end - start) * 10 ** 3)


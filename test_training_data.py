import unittest
from training_data import draw_cards, put_hands, hand_set, winning_set


class TestPokerFunctions(unittest.TestCase):
    def test_draw_cards(self):
        n = 5
        cards = draw_cards(n)
        self.assertEqual(len(cards), n)

    def test_put_hands(self):
        arr = ['TH', 'TS', 'AH', 'KH', 'TC', 'TD', '9S', '8D', '9D', '2H', '5S', '6S']
        i = 0
        hands = put_hands(arr, i)
        self.assertEqual(len(hands), 2)
        self.assertEqual(hands, ['TH', '9S'])
        i = 1
        hands = put_hands(arr, i)
        self.assertEqual(len(hands), 2)
        self.assertEqual(hands, ['TS', '8D'])
        i = 2
        hands = put_hands(arr, i)
        self.assertEqual(len(hands), 2)
        self.assertEqual(hands, ['AH', '9D'])
        i = 3
        hands = put_hands(arr, i)
        self.assertEqual(len(hands), 2)
        self.assertEqual(hands, ['KH', '2H'])
        i = 4
        hands = put_hands(arr, i)
        self.assertEqual(len(hands), 2)
        self.assertEqual(hands, ['TC', '5S'])
        i = 5
        hands = put_hands(arr, i)
        self.assertEqual(len(hands), 2)
        self.assertEqual(hands, ['TD', '6S'])

    def test_hand_set_high_card(self):
        hand = ["2H", "3H"]
        community_cards = ["6H", "TD", "AC", "QS", "7C"]
        rank = hand_set(hand, community_cards)
        self.assertEqual(rank, 0)

    def test_hand_set_one_pair(self):
        hand = ["2H", "3H"]
        community_cards = ["6H", "2D", "AC", "QS", "7C"]
        rank = hand_set(hand, community_cards)
        self.assertEqual(rank, 1)

    def test_hand_set_two_pairs(self):
        hand = ["2H", "3H"]
        community_cards = ["2S", "3D", "9C", "TD", "JH"]
        rank = hand_set(hand, community_cards)
        self.assertEqual(rank, 2)

    def test_hand_set_Three_of_a_Kind(self):
        hand = ["2H", "3H"]
        community_cards = ["2D", "2S", "9D", "TC", "JS"]
        rank = hand_set(hand, community_cards)
        self.assertEqual(rank, 3)

    def test_hand_set_Straight(self):
        hand = ["5H", "TH"]
        community_cards = ["AC", "2C", "3C", "4D", "QD"]
        rank = hand_set(hand, community_cards)
        self.assertEqual(rank, 4)

    def test_hand_set_Flush(self):
        hand = ["2H", "3H"]
        community_cards = ["7H", "8H", "9H", "TD", "JD"]
        rank = hand_set(hand, community_cards)
        self.assertEqual(rank, 5)

    def test_hand_set_Full_house(self):
        hand = ["2H", "3H"]
        community_cards = ["2D", "2S", "3C", "TH", "JD"]
        rank = hand_set(hand, community_cards)
        self.assertEqual(rank, 6)

    def test_hand_set_four_of_a_kind(self):
        hand = ["2H", "3H"]
        community_cards = ["2D", "2C", "2S", "TC", "JH"]
        rank = hand_set(hand, community_cards)
        self.assertEqual(rank, 7)

    def test_hand_set_straight_flush(self):
        hand = ["8H", "6H"]
        community_cards = ["AC", "2C", "3C", "4C", "5C"]
        rank = hand_set(hand, community_cards)
        self.assertEqual(rank, 8)

    def test_hand_set_royal_flush(self):
        hand = ["KH", "QH"]
        community_cards = ["7C", "8C", "AH", "TH", "JH"]
        rank = hand_set(hand, community_cards)
        self.assertEqual(rank, 9)

    def test_winning_set(self):
        sets = [1, 2, 3, 4, 5, 6]
        winner = winning_set(sets)
        self.assertEqual(winner, 6)


if __name__ == '__main__':
    unittest.main()

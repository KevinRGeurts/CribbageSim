# Standard
import unittest
import io
from unittest.mock import patch

# Local
from card import Card
from deck import StackedDeck
from CribbagePlayStrategy import InteractiveCribbagePlayStrategy, HoyleishPlayerCribbagePlayStrategy, HoyleishDealerCribbagePlayStrategy
from CribbageGame import CribbageGame

class Test_CribbageGame(unittest.TestCase):
    
    # Patch results in dealer scoring a pair with their first card played, and winning the game.
    @patch('sys.stdin', io.StringIO('4\n3\n2\n1\n0\n2\n'))
    def test_play_both_interactive_end_at_first_score(self):

        # Create a stacked deck
        sd = StackedDeck()
        # Player will be dealt cards 1 - 6
        # Dealer will be dealt cards 7 - 12
        # Starter will be card 13
        card_list = [Card('S','10'), Card('C','5'), Card('D','10'), Card('C','3'), Card('H','8'), Card('H','K'),
                     Card('S','Q'), Card('H','7'), Card('C','6'), Card('D','A'), Card('H','10'), Card('S','K'),
                     Card('H','5')]
        sd.add_cards(card_list)
        
        game = CribbageGame(player_strategy1 = InteractiveCribbagePlayStrategy(), player_strategy2 = InteractiveCribbagePlayStrategy())
        game._deal._deck = sd
        
        # Player1 will be one point from winning when the game begins, so the first score for that player will win the game.
        game._board.peg_for_player1(120)
        return_val = game.play()

        # Did Player1 win?
        exp_val = game._player1
        act_val = return_val[0]
        self.assertEqual(exp_val, act_val)

        # Is Player1 score 121?
        exp_val = 121
        act_val = return_val[1]
        self.assertEqual(exp_val, act_val)

        # Has there been only 1 deal?
        exp_val = 1
        act_val = return_val[3]
        self.assertEqual(exp_val, act_val)

    @patch('sys.stdin', io.StringIO('3\n0\n3\n2\n1\n0\n2\n0\ng\n1\n0\n0\ng\n0\ng\n1\n0\n2\n0\n1\n0\n1\n2\n0\n0\n0\n0\ng\n'))
    def test_play_both_interactive_end_at_second_show(self):

        # Create a stacked deck
        sd = StackedDeck()
        # Player will be dealt cards 1 - 6 for deal 1, and cards 14 - 19 for deal 2
        # Dealer will be dealt cards 7 - 12 for deal 1, and cards 20 - 25 for deal 2
        # Starter will be card 13 for deal 1, and card 26 for deal 2
        card_list = [Card('H','4'), Card('H','9'), Card('C','10'), Card('S','A'), Card('C','J'), Card('C','5'),
                     Card('H','5'), Card('H','10'), Card('C','2'), Card('D','2'), Card('S','9'), Card('S','7'),
                     Card('S','4'),
                     Card('S','3'), Card('H','A'), Card('H','6'), Card('D','7'), Card('H','7'), Card('D','2'),
                     Card('D','3'), Card('C','J'), Card('H','9'), Card('D','J'), Card('S','J'), Card('D','A'),
                     Card('D','10')]
        sd.add_cards(card_list)
        
        game = CribbageGame(player_strategy1 = InteractiveCribbagePlayStrategy(), player_strategy2 = InteractiveCribbagePlayStrategy())
        game._deal._deck = sd
        
        # Player2 will win after dealing the second deal, and showing the crib 
        game._board.peg_for_player2(97)
        return_val = game.play()

        # Did Player2 win?
        exp_val = game._player2
        act_val = return_val[0]
        self.assertEqual(exp_val, act_val)

        # Is Player2 score 121?
        exp_val = 121
        act_val = return_val[1]
        self.assertEqual(exp_val, act_val)

        # is Player1 score as expected?
        exp_val = 18
        act_val = return_val[2]
        self.assertEqual(exp_val, act_val)

        # Has there been 2 deals?
        exp_val = 2
        act_val = return_val[3]
        self.assertEqual(exp_val, act_val)

    @patch('sys.stdin', io.StringIO('3\n2\n0\n0\n1\ng\n0\n1\n0\n2\n1\n1\n0\ng\n'))
    def test_play_one_interactive_end_at_second_show(self):

        # Create a stacked deck
        sd = StackedDeck()
        # Player will be dealt cards 1 - 6 for deal 1, and cards 14 - 19 for deal 2
        # Dealer will be dealt cards 7 - 12 for deal 1, and cards 20 - 25 for deal 2
        # Starter will be card 13 for deal 1, and card 26 for deal 2
        card_list = [Card('H','4'), Card('H','9'), Card('C','10'), Card('S','A'), Card('C','J'), Card('C','5'),
                     Card('H','5'), Card('H','10'), Card('C','2'), Card('D','2'), Card('S','9'), Card('S','7'),
                     Card('S','4'),
                     Card('S','3'), Card('H','A'), Card('H','6'), Card('D','7'), Card('H','7'), Card('D','2'),
                     Card('D','3'), Card('C','J'), Card('H','9'), Card('D','J'), Card('S','J'), Card('D','A'),
                     Card('D','10')]
        sd.add_cards(card_list)
        
        game = CribbageGame(player_strategy1 = InteractiveCribbagePlayStrategy(), player_strategy2 = HoyleishPlayerCribbagePlayStrategy(),
                            dealer_strategy2 = HoyleishDealerCribbagePlayStrategy())
        game._deal._deck = sd
        
        # Player2 will win after dealing the second deal, and showing the crib 
        game._board.peg_for_player2(100)
        return_val = game.play()

        # Did Player2 win?
        exp_val = game._player2
        act_val = return_val[0]
        self.assertEqual(exp_val, act_val)

        # Is Player2 score 121?
        exp_val = 121
        act_val = return_val[1]
        self.assertEqual(exp_val, act_val)

        # is Player1 score as expected?
        exp_val = 17
        act_val = return_val[2]
        self.assertEqual(exp_val, act_val)

        # Has there been 2 deals?
        exp_val = 2
        act_val = return_val[3]
        self.assertEqual(exp_val, act_val)

       

if __name__ == '__main__':
    unittest.main()

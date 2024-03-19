# Standard
import unittest
import io
from unittest.mock import patch

# Local
from card import Card
from deck import StackedDeck
from CribbagePlayStrategy import InteractiveCribbagePlayStrategy
from CribbageGame import CribbageGame

class Test_CribbageGame(unittest.TestCase):
    
    # Patch results in dealer scoring a pair with their first card played, and winning the game.
    @patch('sys.stdin', io.StringIO('4\n3\n2\n1\n0\n2\n'))
    def test_play_end_at_first_score(self):

        # Create a stacked deck
        sd = StackedDeck()
        # Player will be dealt cards 1 - 6
        # Dealer will be dealt cards 7 - 12
        # Starter will be card 13
        card_list = [Card('S','10'), Card('C','5'), Card('D','10'), Card('C','3'), Card('H','8'), Card('H','K'),
                     Card('S','Q'), Card('H','7'), Card('C','6'), Card('D','A'), Card('H','10'), Card('S','K'),
                     Card('H','5')]
        sd.add_cards(card_list)
        
        game = CribbageGame(strategy1 = InteractiveCribbagePlayStrategy(), strategy2 = InteractiveCribbagePlayStrategy())
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

    # Patch results in dealer scoring a pair with their first card played, and winning the game.
    @patch('sys.stdin', io.StringIO('4\n3\n2\n1\n'))
    def test_play_end_at_second_show(self):

        # Create a stacked deck
        sd = StackedDeck()
        # Player will be dealt cards 1 - 6
        # Dealer will be dealt cards 7 - 12
        # Starter will be card 13
        card_list = [Card('S','10'), Card('C','5'), Card('D','10'), Card('C','3'), Card('H','8'), Card('H','K'),
                     Card('S','Q'), Card('H','7'), Card('C','6'), Card('D','A'), Card('H','10'), Card('S','K'),
                     Card('H','5')]
        sd.add_cards(card_list)
        
        game = CribbageGame(strategy1 = InteractiveCribbagePlayStrategy(), strategy2 = InteractiveCribbagePlayStrategy())
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

       

if __name__ == '__main__':
    unittest.main()

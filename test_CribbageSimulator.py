# Standard
import logging
import unittest
import io
from unittest.mock import patch

# Local
from card import Card
from deck import StackedDeck
from CribbageSimulator import CribbageSimulator
from CribbageGame import CribbageGame
from CribbagePlayStrategy import InteractiveCribbagePlayStrategy

class Test_CribbageSimulator(unittest.TestCase):
 
    # Patch results in dealer scoring a pair with their first card played, and winning the game.
    @patch('sys.stdin', io.StringIO('4\n3\n2\n1\n0\n2\n'))
    def test_logging_info(self):
        
        # Set up logging
        sim = CribbageSimulator()
        sim.setup_logging()

        # Create an interactive cribbage game
        game = CribbageGame(player_strategy1 = InteractiveCribbagePlayStrategy(), player_strategy2 = InteractiveCribbagePlayStrategy())

        # Create a stacked deck
        sd = StackedDeck()
        # Player will be dealt cards 1 - 6
        # Dealer will be dealt cards 7 - 12
        # Starter will be card 13
        card_list = [Card('S','10'), Card('C','5'), Card('D','10'), Card('C','3'), Card('H','8'), Card('H','K'),
                     Card('S','Q'), Card('H','7'), Card('C','6'), Card('D','A'), Card('H','10'), Card('S','K'),
                     Card('H','5')]
        sd.add_cards(card_list)
        
        game._deal._deck = sd
        
        # Player1 will be one point from winning when the game begins, so the first score for that player will win the game.
        game._board.peg_for_player1(120)
        
        # Test that logger works as expected
        with self.assertLogs('cribbage_logger', level=logging.INFO) as cm:
            game.play()
        
        # Test that the info messages sent to the logger are as expected
        self.assertEqual(cm.output[0], 'INFO:cribbage_logger:Player human_player will deal.')    
        self.assertEqual(cm.output[1], 'INFO:cribbage_logger:Starter card: 5H')
        
    # Patch results in dealer scoring a pair with their first card played, and winning the game.
    @patch('sys.stdin', io.StringIO('4\n3\n2\n1\n0\n2\n'))
    def test_logging_debug(self):

        # Set up logging
        sim = CribbageSimulator()
        sim.setup_logging()

        # Create an interactive cribbage game
        game = CribbageGame(player_strategy1 = InteractiveCribbagePlayStrategy(), player_strategy2 = InteractiveCribbagePlayStrategy())

        # Create a stacked deck
        sd = StackedDeck()
        # Player will be dealt cards 1 - 6
        # Dealer will be dealt cards 7 - 12
        # Starter will be card 13
        card_list = [Card('S','10'), Card('C','5'), Card('D','10'), Card('C','3'), Card('H','8'), Card('H','K'),
                     Card('S','Q'), Card('H','7'), Card('C','6'), Card('D','A'), Card('H','10'), Card('S','K'),
                     Card('H','5')]
        sd.add_cards(card_list)
        
        game._deal._deck = sd
        
        # Player1 will be one point from winning when the game begins, so the first score for that player will win the game.
        game._board.peg_for_player1(120)
        
        # Test that logger works as expected
        with self.assertLogs('cribbage_logger', level=logging.DEBUG) as cm:
            game.play()
        
        # Test that the debug messages sent to the logger are as expected
        self.assertEqual(cm.output[0], 'INFO:cribbage_logger:Player human_player will deal.')    
        self.assertEqual(cm.output[1], 'DEBUG:cribbage_logger:Dealt player hand: 10S 5C 10D 3C 8H KH')
        self.assertEqual(cm.output[2], 'DEBUG:cribbage_logger:Dealt player hand: [Card(\'S\',\'10\'), Card(\'C\',\'5\'), Card(\'D\',\'10\'), Card(\'C\',\'3\'), Card(\'H\',\'8\'), Card(\'H\',\'K\')]')


if __name__ == '__main__':
    unittest.main()

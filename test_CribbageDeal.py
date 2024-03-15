# Standard
import unittest
import io
from unittest.mock import patch

# Local
from card import Card
from hand import Hand
from deck import StackedDeck
from CribbagePlayStrategy import InteractiveCribbagePlayStrategy
from CribbageDeal import CribbageDeal

class Test_CribbageDeal(unittest.TestCase):
    
    def test_determine_score_showing(self):
        
        deal = CribbageDeal()

        h = Hand()
        h.add_cards([Card('S','9'), Card('C','6'), Card('H','2'), Card('D','K')])
        s = Card('S','6')
        
        exp_val = 6
        act_val = deal.determine_score_showing(h, s)
        self.assertEqual(exp_val, act_val)

    def test_determine_score_play_fifteen(self):
        
        deal = CribbageDeal()

        h = Hand()
        h.add_cards([Card('S','9'), Card('C','6')])
        
        exp_val = 2
        act_val = deal.determine_score_playing(h)
        self.assertEqual(exp_val, act_val)

    def test_determine_score_play_pair(self):
        
        deal = CribbageDeal()

        h = Hand()
        h.add_cards([Card('S','9'), Card('C','J'), Card('H','J')])
        
        exp_val = 2
        act_val = deal.determine_score_playing(h)
        self.assertEqual(exp_val, act_val)

    def test_determine_score_play_run(self):
        
        deal = CribbageDeal()

        h = Hand()
        h.add_cards([Card('S','9'), Card('C','J'), Card('H','10')])
        
        exp_val = 3
        act_val = deal.determine_score_playing(h)
        self.assertEqual(exp_val, act_val)

    def test_determine_score_play_run_15(self):
        
        deal = CribbageDeal()

        h = Hand()
        h.add_cards([Card('S','4'), Card('C','6'), Card('H','5')])
        
        exp_val = 5
        act_val = deal.determine_score_playing(h)
        self.assertEqual(exp_val, act_val)

    # Apply a patch() decorator to replace keyboard input from user with a string.
    # The patch should result in...
    # Player places 10 and 3 in crib
    # Dealer places K and A in crib
    # Player leads 8
    # Dealer follows with 7 (15 total), scoring 15 for 2
    # Player follows with 7 (22 total), scoring 2 for a pair
    # Dealer follws with 9D, scoring 2 for 31, and ending the go round
    # Player leads J
    # Dealer follws with 9C (19 total)
    # Player follows with 5 (24 total)
    # Dealer declares go.
    # Player can't play another card, and scores 1 for the go, and ending the go round
    # Dealer leads 8, scoring 1 for playing the last card
    # Score from play is Dealer 5, Player 3
    # Score from show is:
    #      Dealer: 2 runs of 4 for 8, 1 pair for 2, 3 15's for 6, for a total of 16
    #      Player: run of 4 for 4, 2 15's for 4, for a total of 8
    # Total score with play and show is Dealer 5 + 16 = 21, Player 3 + 8 = 11
    @patch('sys.stdin', io.StringIO('5\n1\n5\n0\n1\n3\n1\n0\n0\n0\n0\ng\n0\ng\n'))
    def test_play_interactive_1(self):

        # Create a stacked deck
        sd = StackedDeck()
        # Player will be dealt cards 1 - 6
        # Dealer will be dealt cards 7 - 12
        # Starter will be card 13
        card_list = [Card('D','J'), Card('S','10'), Card('H','8'), Card('C','7'), Card('H','5'), Card('C','3'),
                     Card('S','K'), Card('D','9'), Card('C','9'), Card('D','8'), Card('S','7'), Card('H','A'),
                     Card('S','6')]
        sd.add_cards(card_list)
        
        deal = CribbageDeal(InteractiveCribbagePlayStrategy(), InteractiveCribbagePlayStrategy())
        deal._deck = sd
        
        deal.play()
        
        # Did we get the expected dealer score from playing the deal?
        exp_val = 21
        act_val = deal._dealer_score
        self.assertEqual(exp_val, act_val)

        # Did we get the expected player score from playing the deal?
        exp_val = 11
        act_val = deal._player_score
        self.assertEqual(exp_val, act_val)

    # Apply a patch() decorator to replace keyboard input from user with a string.
    # The patch should result in...
    # Player places 7 and 3 in crib (patch: 3\n0\n)
    # Dealer places 9 and 7 in crib (5\n4\n)
    # Player leads 4 (0\n)
    # Dealer follows with KC (14 total) (2\n)
    # Player follows with KD (24 total), scoring 2 for a pair (2\n)
    # Dealer declares go (g\n)
    # Player plays A (25 total), scoring 1 for the go, and ending the go round (0\n)
    # Dealer leads next go round with JS (0\n)
    # Player follows with Q (20 total) (0\n)
    # Dealer follows with KS (30 total), scoring 3 for run (1\n)
    # Player has no cards left, so declares go (g\n)
    # Dealer can't play and scores on for 30, ending the go round
    # Player declares go on leading the next go round because has no remaining cards (g\n)
    # Dealer plays (really leads) JH to start the next go round (10 total), and scores 1 for playing the last card (automatic player go?) (0\n)
    # Score from play is Dealer 5, Player 3
    # Score from show is:
    #      Dealer: 2 pair for 4, 4 15's for 8, for a total of 12
    #      Crib: 2 15's for 4, 1 pair for 2, for a total of 6
    #      Player: 4 15's for 8, for a total of 8
    # Total score with play and show is Dealer 5 + 12 + 6 = 23, Player 3 + 8 = 11
    @patch('sys.stdin', io.StringIO('3\n0\n5\n4\n0\n2\n2\ng\n0\n0\n0\n1\ng\ng\n0\n'))
    def test_play_interactive_2(self):

        # Create a stacked deck
        sd = StackedDeck()
        # Player will be dealt cards 1 - 6
        # Dealer will be dealt cards 7 - 12
        # Starter will be card 13
        card_list = [Card('S','3'), Card('H','4'), Card('H','A'), Card('D','7'), Card('H','Q'), Card('D','K'),
                     Card('S','J'), Card('H','J'), Card('C','K'), Card('S','K'), Card('C','7'), Card('D','9'),
                     Card('C','5')]
        sd.add_cards(card_list)
        
        deal = CribbageDeal(InteractiveCribbagePlayStrategy(), InteractiveCribbagePlayStrategy())
        deal._deck = sd
        
        deal.play()
        
        # Did we get the expected dealer score from playing the deal?
        exp_val = 23
        act_val = deal._dealer_score
        self.assertEqual(exp_val, act_val)

        # Did we get the expected player score from playing the deal?
        exp_val = 11
        act_val = deal._player_score
        self.assertEqual(exp_val, act_val)
    
if __name__ == '__main__':
    unittest.main()

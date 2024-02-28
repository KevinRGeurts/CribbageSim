# Standard
import unittest

# Local
from card import Card
from hand import Hand
from CribbageCombination import FifteenCombination
from CribbagePlayStrategy import DummyCribbagePlayStrategy
from CribbageDeal import CribbageDeal

class Test_CribbageDeal(unittest.TestCase):
    
    def test_determine_score_show(self):
        
        deal = CribbageDeal()

        h = Hand()
        h.add_cards([Card('S','9'), Card('C','6'), Card('H','2'), Card('D','K')])
        s = Card('S','6')
        
        exp_val = 6
        act_val = deal.determine_score(h, s, False)
        self.assertEqual(exp_val, act_val)

    def test_determine_score_play_fifteen(self):
        
        deal = CribbageDeal()

        h = Hand()
        h.add_cards([Card('S','9'), Card('C','6')])
        
        exp_val = 2
        act_val = deal.determine_score(h, None, True)
        self.assertEqual(exp_val, act_val)

    def test_determine_score_play_pair(self):
        
        deal = CribbageDeal()

        h = Hand()
        h.add_cards([Card('S','9'), Card('C','J'), Card('H','J')])
        
        exp_val = 2
        act_val = deal.determine_score(h, None, True)
        self.assertEqual(exp_val, act_val)

    def test_determine_score_play_run(self):
        
        deal = CribbageDeal()

        h = Hand()
        h.add_cards([Card('S','9'), Card('C','J'), Card('H','10')])
        
        exp_val = 3
        act_val = deal.determine_score(h, None, True)
        self.assertEqual(exp_val, act_val)


if __name__ == '__main__':
    unittest.main()

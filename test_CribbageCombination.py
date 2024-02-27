# Standard
import unittest

# Local
from card import Card
from hand import Hand
from CribbageCombination import CribbageCombination

class Test_CribbageCombination(unittest.TestCase):
    
    def test_permutations_size_2(self):
        
        h = Hand()
        h.add_cards([Card('S','2'), Card('C','6'), Card('H','2'), Card('D','K'), Card('S','6')])
        cc = CribbageCombination()
        
        # Create permutations of size 2
        permutations = cc.permutations(2, h.get_cards())

        # Did we get the expected number of permutations of size 2?
        exp_val = 10
        act_val = len(permutations)
        self.assertEqual(exp_val, act_val)
        
        # Is the first permutation as expected?
        exp_val = ('2', '6')
        act_val = (permutations[0][0].get_pips(), permutations[0][1].get_pips())
        self.assertEqual(exp_val, act_val)

        # Is the last permutation as expected?
        exp_val = ('K', '6')
        act_val = (permutations[len(permutations)-1][0].get_pips(), permutations[len(permutations)-1][1].get_pips())
        self.assertTupleEqual(exp_val, act_val)


if __name__ == '__main__':
    unittest.main()

# Standard
import unittest

# Local
from CribbagePlayStrategy import CribbagePlayStrategy
from CribbageDeal import CribbageDeal

class Test_CribbagePlayStrategy(unittest.TestCase):
    
    def test_form_crib(self):

        cd = CribbageDeal()

        cps = CribbagePlayStrategy()
        self.assertRaises(NotImplementedError, cps.form_crib, cd.xfer_player_card_to_crib, cd.get_player_hand)

    def test_follow(self):

        cd = CribbageDeal()

        cps = CribbagePlayStrategy()
        self.assertRaises(NotImplementedError, cps.follow, 0, cd.play_card_for_player, cd.get_player_hand)

    def test_go(self):

        cd = CribbageDeal()

        cps = CribbagePlayStrategy()
        self.assertRaises(NotImplementedError, cps.go, 0, cd.play_card_for_player, cd.get_player_hand,
                          cd.get_combined_play_pile, cd.determine_score_playing, cd.peg_for_player)


if __name__ == '__main__':
    unittest.main()

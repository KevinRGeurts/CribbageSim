# Standard
import unittest

# Local
from card import Card
from hand import Hand
from deck import StackedDeck
from CribbagePlayStrategy import HoyleishCribbagePlayStrategy, HoyleishDealerCribbagePlayStrategy, HoyleishPlayerCribbagePlayStrategy
from CribbageDeal import CribbageDeal


class Test_HoyleishCribbagePlayStrategy(unittest.TestCase):
    
    def test_guaranteed_hand_score(self):
        
        hcp = HoyleishCribbagePlayStrategy()
        
        h = Hand()
        h.add_cards([Card('S','9'), Card('S','9'), Card('S','10'), Card('S','J')])
        
        # 2 runs of 3 for 6, 1 pair for 2, flush for 4, all total = 12
        exp_val = 12
        act_val = hcp.guaranteed_hand_score(h)
        self.assertEqual(exp_val, act_val)

    def test_guaranteed_crib_score_pair(self):
        
        hcp = HoyleishCribbagePlayStrategy()
        
        h = Hand()
        h.add_cards([Card('C','9'), Card('S','9')])
        
        # 1 pair for 2
        exp_val = 2
        act_val = hcp.guaranteed_crib_score(h)
        self.assertEqual(exp_val, act_val)

    def test_guaranteed_crib_score_15(self):
        
        hcp = HoyleishCribbagePlayStrategy()
        
        h = Hand()
        h.add_cards([Card('H','7'), Card('S','8')])
        
        # 1 fifteen for 2
        exp_val = 2
        act_val = hcp.guaranteed_crib_score(h)
        self.assertEqual(exp_val, act_val)

    def test_guaranteed_crib_score_none(self):
        
        hcp = HoyleishCribbagePlayStrategy()
        
        h = Hand()
        h.add_cards([Card('H','7'), Card('S','K')])
        
        exp_val = 0
        act_val = hcp.guaranteed_crib_score(h)
        self.assertEqual(exp_val, act_val)

    def test_permute_and_score_dealt_hand(self):

        hcp = HoyleishCribbagePlayStrategy()
        
        h = Hand()
        h.add_cards([Card('C','9'), Card('S','9'), Card('S','10'), Card('S','J'), Card('H','2'), Card('D','2')])

        options_list = hcp.permute_and_score_dealt_hand(h.get_cards())

        # Did we get the expected number of options?
        exp_val = 15
        act_val = len(options_list)
        self.assertEqual(exp_val, act_val)

        # Does the first option have the expected hand score?
        # 2 runs of 3 for 6, 1 pair for 2, all total = 8
        exp_val = 8
        act_val = options_list[0].hand_score
        self.assertEqual(exp_val, act_val)

        # Does the first option have the expected hand Card()s?
        exp_val = h.get_cards()[0:4]
        act_val = options_list[0].hand
        self.assertEqual(exp_val, act_val)

        # Does the first option have the expected crib score?
        # 1 pair (of 2's) for 2
        exp_val = 2
        act_val = options_list[0].crib_score
        self.assertEqual(exp_val, act_val)

        # Does the first option have the expectee crib Card()s?
        exp_val = h.get_cards()[4:6]
        act_val = options_list[0].crib
        self.assertEqual(exp_val, act_val)

    def test_follow_no_playable_card(self):
        exp_val = 1
        act_val = 0
        self.assertEqual(exp_val, act_val)

    def test_follow_lead(self):
        exp_val = 1
        act_val = 0
        self.assertEqual(exp_val, act_val)

    def test_lead_1(self):
        exp_val = 1
        act_val = 0
        self.assertEqual(exp_val, act_val)

    def test_follow_1(self):
        exp_val = 1
        act_val = 0
        self.assertEqual(exp_val, act_val)

    def test_go_1(self):
        exp_val = 1
        act_val = 0
        self.assertEqual(exp_val, act_val)

    def test_dealer_form_crib_max_hand(self):

         # Create a stacked deck
        sd = StackedDeck()
        # Dealer will be dealt cards 1 - 6
        card_list = [Card('S','10'), Card('C','5'), Card('D','10'), Card('C','3'), Card('H','8'), Card('H','K')]
        sd.add_cards(card_list)
        
        deal = CribbageDeal(HoyleishDealerCribbagePlayStrategy(), HoyleishDealerCribbagePlayStrategy())
        deal._deck = sd
        deal.draw_for_dealer(6)
        
        hcp = HoyleishDealerCribbagePlayStrategy()
        hcp.form_crib(deal.xfer_dealer_card_to_crib, deal.get_dealer_hand)

        # Do we have the expected first card in the crib?
        crib = deal._crib_hand.get_cards()
        exp_val = ('C', '3')
        act_val = (crib[0].get_suit(), crib[0].get_pips())
        self.assertTupleEqual(exp_val, act_val)

        # Do we have the expected first card in the crib?
        crib = deal._crib_hand.get_cards()
        exp_val = ('H', '8')
        act_val = (crib[1].get_suit(), crib[1].get_pips())
        self.assertTupleEqual(exp_val, act_val)

    def test_dealer_form_crib_max_hand_crib(self):

         # Create a stacked deck
        sd = StackedDeck()
        # Dealer will be dealt cards 1 - 6
        card_list = [Card('S','10'), Card('C','5'), Card('D','10'), Card('C','8'), Card('H','8'), Card('H','K')]
        sd.add_cards(card_list)
        
        deal = CribbageDeal(HoyleishDealerCribbagePlayStrategy(), HoyleishDealerCribbagePlayStrategy())
        deal._deck = sd
        deal.draw_for_dealer(6)
        
        hcp = HoyleishDealerCribbagePlayStrategy()
        hcp.form_crib(deal.xfer_dealer_card_to_crib, deal.get_dealer_hand)

        # Do we have the expected first card in the crib?
        crib = deal._crib_hand.get_cards()
        exp_val = ('C', '8')
        act_val = (crib[0].get_suit(), crib[0].get_pips())
        self.assertTupleEqual(exp_val, act_val)

        # Do we have the expected first card in the crib?
        crib = deal._crib_hand.get_cards()
        exp_val = ('H', '8')
        act_val = (crib[1].get_suit(), crib[1].get_pips())
        self.assertTupleEqual(exp_val, act_val)

    def test_player_form_crib_max_hand_less_crib(self):

         # Create a stacked deck
        sd = StackedDeck()
        # Player will be dealt cards 1 - 6
        card_list = [Card('S','10'), Card('C','5'), Card('D','10'), Card('C','8'), Card('H','8'), Card('H','K')]
        sd.add_cards(card_list)
        
        deal = CribbageDeal(HoyleishPlayerCribbagePlayStrategy(), HoyleishDealerCribbagePlayStrategy())
        deal._deck = sd
        deal.draw_for_player(6)
        
        hcp = HoyleishPlayerCribbagePlayStrategy()
        hcp.form_crib(deal.xfer_player_card_to_crib, deal.get_player_hand)

        # Do we have the expected Card()s in the crib?
        exp_val = [card_list[4], card_list[5]]
        act_val = crib = deal._crib_hand.get_cards()
        self.assertEqual(exp_val, act_val)
        

if __name__ == '__main__':
    unittest.main()

# Standard
import unittest

# Local
from card import Card
from hand import Hand
from deck import StackedDeck
from CribbagePlayStrategy import HoyleishCribbagePlayStrategy, HoyleishDealerCribbagePlayStrategy
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

    def test_form_crib(self):

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
        

if __name__ == '__main__':
    unittest.main()

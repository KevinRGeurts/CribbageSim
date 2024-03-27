# Standard
import logging
from pathlib import Path
from time import process_time
from random import seed

# Local
from deck import StackedDeck, Deck
from card import Card
from hand import Hand
from CribbageCombination import CribbageComboInfo, PairCombination, HisNobsCombination, RunCombination, FifteenCombination, PairCombinationPlaying, RunCombinationPlaying
from UserResponseCollector import UserResponseCollector_query_user, BlackJackQueryType
from CribbagePlayStrategy import InteractiveCribbagePlayStrategy, HoyleishDealerCribbagePlayStrategy, HoyleishCribbagePlayStrategy, HoyleishPlayerCribbagePlayStrategy
from CribbageDeal import CribbageDeal
from CribbageGame import CribbageGame
from CribbageSimulator import CribbageSimulator


def play_interactive_game():
    """
    Use CribbageSimulator to play an interactive game.
    """

    game = CribbageGame(strategy1 = InteractiveCribbagePlayStrategy(), strategy2 = InteractiveCribbagePlayStrategy())
    game.play()

    return None

def play_interactive_deal():
    """
    Use CribbageSimulator to play an interactive deal.
    """

    deal = CribbageDeal(InteractiveCribbagePlayStrategy(), InteractiveCribbagePlayStrategy())
    deal.play()

    return None

def play_auto_deal():
    """
    Use CribbageSimulator to play a completely automatic deal. 
    """
    deal = CribbageDeal(HoyleishPlayerCribbagePlayStrategy(), HoyleishDealerCribbagePlayStrategy())
    deal.play()

def play_debug():
    """
    Use CribbageSimulator to set up and execute a debugging scenario.
    """

    hcp = HoyleishCribbagePlayStrategy()
        
    h = Hand()
    h.add_cards([Card('C','6'), Card('D','7'), Card('H','8'), Card('S','9')])

    ratings_list = hcp.rate_leads_in_hand(h)


    # # Create a stacked deck
    # sd = StackedDeck()
    # # Player will be dealt cards 1 - 6
    # card_list = [Card('S','10'), Card('C','5'), Card('D','10'), Card('C','8'), Card('H','8'), Card('H','K')]
    # sd.add_cards(card_list)
        
    # deal = CribbageDeal(HoyleishPlayerCribbagePlayStrategy(), HoyleishDealerCribbagePlayStrategy())
    # deal._deck = sd
    # deal.draw_for_player(6)
        
    # hcp = HoyleishPlayerCribbagePlayStrategy()
    # hcp.form_crib(deal.xfer_player_card_to_crib, deal.get_player_hand)

    # crib = deal._crib_hand.get_cards()

    
    # # Create a stacked deck
    # sd = StackedDeck()
    # # Player will be dealt cards 1 - 6
    # # Dealer will be dealt cards 7 - 12
    # # Starter will be card 13
    # card_list = [Card('S','10'), Card('C','5'), Card('D','10'), Card('C','3'), Card('H','8'), Card('H','K'),
    #                 Card('S','Q'), Card('H','7'), Card('C','6'), Card('D','A'), Card('H','10'), Card('S','K'),
    #                 Card('H','5')]
    # sd.add_cards(card_list)
        
    # deal = CribbageDeal(HoyleishDealerCribbagePlayStrategy(), HoyleishDealerCribbagePlayStrategy())
    # deal._deck = sd
        
    # deal.play()
    
    return None
    


if __name__ == '__main__':
    
    """
    Query the user for how they wish to use the Cribage simulator, and then launch that usage.
    This includes a "debug" usage to set up what ever situation is needed for debugging, since I can't seem to reliably debug unit tests.
    """
    
    # Set up logging
    CribbageSimulator().setup_logging()
    
    print('---------------------------------')
    print('*** Python Cribbage Simulator ***')
    print('---------------------------------')
        
    # Build a query for the user to obtain their choice of how to user the simulator
    query_preface = 'How do you want to use the simulator?'
    query_dic = {'q':'Quit', 'g':'Interactive Game', 'i':'Interactive Deal', 'a':'Automatic Deal', 'd':'Debug'}
    response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
    
    while response != 'q':
        
        match response:
            
            case 'g':
                play_interactive_game()
            
            case 'i':
                play_interactive_deal()

            case 'a':
                play_auto_deal()

            case 'd':
                play_debug()
        
        print('--------------------')
        response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
      
   

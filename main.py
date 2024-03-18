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
from CribbagePlayStrategy import InteractiveCribbagePlayStrategy
from CribbageDeal import CribbageDeal


def play_interactive():
    """
    Use CribbageSimulator to play an interactive game.
    """

    deal = CribbageDeal(InteractiveCribbagePlayStrategy(), InteractiveCribbagePlayStrategy())
    deal.play()

    return None

def play_debug():
    """
    Use CribbageSimulator to set up and execute a debugging scenario.
    """

    # Create a stacked deck
    sd = StackedDeck()
    # Player will be dealt cards 1 - 6
    # Dealer will be dealt cards 7 - 12
    # Starter will be card 13
    card_list = [Card('H','3'), Card('S','3'), Card('C','8'), Card('S','4'), Card('C','10'), Card('S','2'),
                    Card('S','6'), Card('C','7'), Card('C','4'), Card('D','A'), Card('H','9'), Card('C','2'),
                    Card('D','2')]
    sd.add_cards(card_list)
        
    deal = CribbageDeal(InteractiveCribbagePlayStrategy(), InteractiveCribbagePlayStrategy())
    deal._deck = sd
        
    deal.play()
    
    return None
    


if __name__ == '__main__':
    
    """
    Query the user for how they wish to use the Cribage simulator, and then launch that usage.
    This includes a "debug" usage to set up what ever situation is needed for debugging, since I can't seem to reliably debug unit tests.
    """
    
    # Set up logging
    # BlackJackSim().setup_logging()
    
    print('--------------------')
    print('*** Python Criggage Simulator ***')
    print('--------------------')
        
    # Build a query for the user to obtain their choice of how to user the simulator
    query_preface = 'How do you want to use the simulator?'
    query_dic = {'q':'Quit', 'i':'Interactive Game', 'd':'Debug'}
    response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
    
    while response != 'q':
        
        match response:
            
            case 'i':
                play_interactive()

            case 'd':
                play_debug()
        
        print('--------------------')
        response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
      
   

# Standard
import logging
from pathlib import Path
from time import process_time
from random import seed

# Local
from deck import StackedDeck, Deck
from card import Card
from hand import Hand
from CribbageCombination import CribbageComboInfo, PairCombination, HisNobsCombination
from UserResponseCollector import UserResponseCollector_query_user, BlackJackQueryType


def play_interactive():
    """
    Use CribbageSimulator to play an interactive game.
    """

    return None

def play_debug():
    """
    Use CribbageSimulator to set up and execute a debugging scenario.
    """
    hnc = HisNobsCombination()
    
    hand = Hand()
    hand.add_cards([Card('S','2'), Card('C','6'), Card('H','J'), Card('D','K')])
    stater = Card('H','8')
    
    # This is a cribbage hand, so make sure it has 4 cards
    assert(hand.get_num_cards() == 4)

    info = CribbageComboInfo()
    info.combo_name = hnc.get_name()
        
    cards = hand.get_cards()

    # Are any of the cards in the hand a Jack? If so, does the suit of the Jack match the starter? Then list them.
    jacks_in_hand = []
    for i in range(len(cards)):
        if cards[i].get_pips() == "J":
            if cards[i].get_suit() == starter.get_suit():
                jacks_in_hand.append(cards[i])

    # Since cribbage should always be played with a single, non-infinite deck, we should never find more than one Jack where the suit
    # matches the starter.

    assert (len(jacks_in_hand) <= 1)
                    
    if len(jacks_in_hand) == 1:
        info.number_instances = 1
        info.instance_list = [jacks_in_hand]
        # info.score = info.number_instances * self._score_per_combo
    
    #info = pc.score(h)
    
    print(info)
    
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
      
   

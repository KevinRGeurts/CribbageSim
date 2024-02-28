# Standard
import logging
from pathlib import Path
from time import process_time
from random import seed

# Local
from deck import StackedDeck, Deck
from card import Card
from hand import Hand
from CribbageCombination import CribbageComboInfo, PairCombination, HisNobsCombination, RunCombination
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
    
    rc = RunCombination()
    
    info = CribbageComboInfo()
    info.combo_name = rc._combo_name
    
    hand = Hand()
    hand.add_cards([Card('S','2'), Card('C','3'), Card('H','4'), Card('D','5')])
    starter = Card('H','6')
    
    cards = hand.get_cards()
    cards.append(starter)
    
    permutations = rc.permutations(5, cards)

    # Do we have a run of five cards?
    is_run = True
    # Iterate through the five-card permutations and determine how many of them are a run
    for p in permutations:
        # Sort the cards in the permutation, this requires, Card class to have __lt__ method implemented
        p.sort()
        # TODO: From here the concept is to see if each successive card has a "value" that is one greater than the previous card
        # This will require Card to have a method that returns a "sequencing count" where A=1, J=11, Q=12, K=13.
        # Once this is implemented the Card.__lt__() can be rewritten to use the sequencing count.
        first_card = p.pop(0)
        prev_sequence_count = first_card.get_sequence_count()
        for c in p:
            if c.get_sequence_count() == prev_sequence_count + 1:
                prev_sequence_count = c.get_sequence_count()
            else:
                is_run = False
                break
        if is_run:
            info.number_instances += 1
            info.score = 5
            # Since we popped the first card off p, when need to reassemble the original p to append it to the info.instance_list of lists
            info.instance_list.append([first_card].extend(p))
    
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
      
   

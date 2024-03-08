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

    pile = Hand()
    pile.add_cards([Card('D','J'), Card('S','2'), Card('C','2'), Card('H','2'), Card('D','2')])
    pcp = PairCombinationPlaying()
    info = pcp.score(pile)


    return None

def play_debug():
    """
    Use CribbageSimulator to set up and execute a debugging scenario.
    """
    
    # deal = CribbageDeal(InteractiveCribbagePlayStrategy(), InteractiveCribbagePlayStrategy())
    # deal.play()

    pile = Hand()
    pile.add_cards([Card('S','A'), Card('C','J'), Card('H','9'), Card('D','10')])
    rcp = RunCombinationPlaying()
    info = rcp.score(pile)

    exp_val = 'run: 1 for 3: 9H 10D JC , '
    act_val = str(info)
    print(act_val)
 
    
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
      
   

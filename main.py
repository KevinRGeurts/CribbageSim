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
from CribbageGame import CribbageGame


def play_interactive_game():
    """
    Use CribbageSimulator to play an interactive game.
    """

    game = CribbageGame(strategy1 = InteractiveCribbagePlayStrategy(), strategy2 = InteractiveCribbagePlayStrategy())
    game.play()

    return None

def play_interactive_deal():
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
    card_list = [Card('S','10'), Card('C','5'), Card('D','10'), Card('C','3'), Card('H','8'), Card('H','K'),
                    Card('S','Q'), Card('H','7'), Card('C','6'), Card('D','A'), Card('H','10'), Card('S','K'),
                    Card('H','5')]
    sd.add_cards(card_list)
        
    game = CribbageGame(strategy1 = InteractiveCribbagePlayStrategy(), strategy2 = InteractiveCribbagePlayStrategy())
    game._deal._deck = sd
        
    # Player1 (The dealer) will be one point from winning when the game begins, so the first score for that player will win the game.
    game._board.peg_for_player1(120)
    return_val = game.play()
    
    # # Create a stacked deck
    # sd = StackedDeck()
    # # Player will be dealt cards 1 - 6
    # # Dealer will be dealt cards 7 - 12
    # # Starter will be card 13
    # card_list = [Card('H','3'), Card('S','3'), Card('C','8'), Card('S','4'), Card('C','10'), Card('S','2'),
    #                 Card('S','6'), Card('C','7'), Card('C','4'), Card('D','A'), Card('H','9'), Card('C','2'),
    #                 Card('D','2')]
    # sd.add_cards(card_list)
        
    # deal = CribbageDeal(InteractiveCribbagePlayStrategy(), InteractiveCribbagePlayStrategy())
    # deal._deck = sd
        
    # deal.play()
    
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
    query_dic = {'q':'Quit', 'g':'Interactive Game', 'i':'Interactive Deal', 'd':'Debug'}
    response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
    
    while response != 'q':
        
        match response:
            
            case 'g':
                play_interactive_game()
            
            case 'i':
                play_interactive_deal()

            case 'd':
                play_debug()
        
        print('--------------------')
        response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
      
   

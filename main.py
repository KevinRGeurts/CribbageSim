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

    game = CribbageGame(player_strategy1 = InteractiveCribbagePlayStrategy(), player_strategy2 = HoyleishPlayerCribbagePlayStrategy(),
                        dealer_strategy2 = HoyleishDealerCribbagePlayStrategy())
    game.play()

    return None

def play_interactive_deal():
    """
    Use CribbageSimulator to play an interactive deal, as the dealer.
    """

    deal = CribbageDeal(HoyleishPlayerCribbagePlayStrategy(), InteractiveCribbagePlayStrategy())
    deal.play()

    return None

def play_auto_game():
        """
        Use CribbageSimulator to plan an interactive game, as player1.
        """
        
        game = CribbageGame(player_strategy1 = HoyleishPlayerCribbagePlayStrategy(), player_strategy2 = HoyleishPlayerCribbagePlayStrategy(),
                            dealer_strategy1 = HoyleishDealerCribbagePlayStrategy(), dealer_strategy2 = HoyleishDealerCribbagePlayStrategy())
        game.play()
        
        return None

def play_auto_deal():
    """
    Use CribbageSimulator to play a completely automatic deal. 
    """
    # Seed the random number generator
    from random import seed
    seed(1234567890)

    deal = CribbageDeal(HoyleishPlayerCribbagePlayStrategy(), HoyleishDealerCribbagePlayStrategy())
    deal.play()

def play_debug():
    """
    Use CribbageSimulator to set up and execute a debugging scenario.
    """
    # Seed the random number generator
    from random import seed

    my_seed = 1234568673
    
    while my_seed <= 1234568673:
       
        print(f"Seed Value: {my_seed}")
        seed(my_seed)

        game = CribbageGame(player_strategy1 = HoyleishPlayerCribbagePlayStrategy(), player_strategy2 = HoyleishPlayerCribbagePlayStrategy(),
                            dealer_strategy1 = HoyleishDealerCribbagePlayStrategy(), dealer_strategy2 = HoyleishDealerCribbagePlayStrategy())
        return_val = game.play()

        my_seed += 1

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
    query_dic = {'q':'Quit', 'g':'Interactive Game', 'i':'Interactive Deal', 'a':'Automatic Game', 'b':'Automatic Deal',  'd':'Debug'}
    response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
    
    while response != 'q':
        
        match response:
            
            case 'g':
                play_interactive_game()
            
            case 'i':
                play_interactive_deal()
            
            case 'a':
                play_auto_game()

            case 'b':
                play_auto_deal()

            case 'd':
                play_debug()
        
        print('--------------------')
        response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
      
   

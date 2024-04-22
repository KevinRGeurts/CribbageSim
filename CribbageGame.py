# Standard imports
import logging
from enum import Enum

# Local imports
from CribbageBoard import CribbageBoard
from CribbageDeal import CribbageDeal
from CribbagePlayStrategy import CribbagePlayStrategy, InteractiveCribbagePlayStrategy, HoyleishDealerCribbagePlayStrategy, HoyleishPlayerCribbagePlayStrategy
from exceptions import CribbageGameOverError
from UserResponseCollector import UserResponseCollectorError, UserResponseCollectorTerminateQueryingThreadError

class CribbagePlayers(Enum):
    """
    An enumeration of the participants in a cribbage simulator.
    """
    PLAYER_1 = 1 
    PLAYER_2 = 2


class CribbageGameInfo:
    """
    A class with all members/attributes considered public. Used to return information about the results of a cribbage game,
    from CribbageGame.play(...).
    """
    def __init__(self):
        """
        Create and initialize attributes.
        """
        self.player1_total_play_score = 0
        self.player1_total_his_heals_score = 0 # Starter card was a J
        self.player1_total_show_score = 0
        self.player1_total_crib_score = 0
        self.player2_total_play_score = 0
        self.player2_total_his_heals_score = 0 # Starter card was a J
        self.player2_total_show_score = 0
        self.player2_total_crib_score = 0
        self.winning_player = ''
        self.winning_player_final_score = 0
        self.losing_player_final_score = 0
        self.deals_in_game = 0
 

class CribbageGame:
    """
    Class representing a cribbage game, to be played out by two players, player1 and player2.
    """
    
    def __init__(self, name1 = 'human_player', name2 = 'machine_player',
                 player_strategy1 = InteractiveCribbagePlayStrategy(), player_strategy2 = HoyleishPlayerCribbagePlayStrategy(),
                 dealer_strategy1 = None, dealer_strategy2 = None):
        """
        Construct a cribbage game with a CribbageBoard, two player names, and a CribbageDeal.
        :parameter name1: Name of player1, string
        :parameter name2: Name of player2, string
        :parameter player_strategy1: Player strategy for player1, Instance of CribbagePlayStrategy
        :parameter player_strategy2: Player strategy for player2, Instance of CribbagePlayStrategy
        :parameter dealer_strategy1: Dealer strategy for player1 (defaults to player_strategy1 if None), Instance of CribbagePlayStrategy
        :parameter dealer_strategy2: Dealer strategy for player2 (defaults to player_strategy2 if None), Instance of CribbagePlayStrategy
        """
        assert(isinstance(player_strategy1, CribbagePlayStrategy))
        assert(isinstance(player_strategy2, CribbagePlayStrategy))
        if dealer_strategy1: assert(isinstance(dealer_strategy1, CribbagePlayStrategy))
        if dealer_strategy2: assert(isinstance(dealer_strategy2, CribbagePlayStrategy))
        self._board = CribbageBoard()
        self._player1 = name1
        self._player2 = name2
        self._player1_player_strategy = player_strategy1
        if dealer_strategy1: 
            self._player1_dealer_strategy = dealer_strategy1
        else:
            self._player1_dealer_strategy = player_strategy1
        self._player2_player_strategy = player_strategy2
        if dealer_strategy2: 
            self._player2_dealer_strategy = dealer_strategy2
        else:
            self._player2_dealer_strategy = player_strategy2
        self._deal = CribbageDeal(self._player2_player_strategy, self._player1_dealer_strategy)

    def get_player1_name(self):
        """
        :return: Name of player1, string
        """
        return self._player1
    
    def get_player2_name(self):
        """
        :return: Name of player2, string
        """
        return self._player2
    
    def get_player_scores(self):
        """
        :return: (player1 score, player2 score), tuple
        """
        return self._board.get_scores()
        
    def peg_for_player1(self, count = 1):
        """
        Peg on the board count for player1.
        :parameter count: The count to peg for player1 on the board, int
        :return: Current peg total for player1 after pegging count, int
        """
        return self._board.peg_for_player1(count)
        
    def peg_for_player2(self, count = 1):
        """
        Peg on the board count for player2.
        :parameter count: The count to peg for player2 on the board, int
        :return: Current peg total for player2 after pegging count, int
        """
        return self._board.peg_for_player2(count)
        
    def play(self):
        """
        Play a game of cribbage.
        :return: Information about the results of the game, CribbageGameInfo object
        :return: (Name of Winning Player, Winning Player Final Score, Losing Player Final Score, Number of Deals In Game), tuple (string, int, int, int)
        """

        # Get the logger 'cribbage_logger'
        logger = logging.getLogger('cribbage_logger')

        game_over = False
        deal_count = 0
        return_val = CribbageGameInfo()
        # return_val = ('nobody', 0, 0, 0)
        
        # TODO: For now player1 will always deal first, but implement random selection, such as cutting for high card
        # Consider that this predictability is beneficial to unit testing.
        next_to_deal = CribbagePlayers.PLAYER_1
        
        while not game_over:
        
            deal_count += 1

            # Reset deal so we are ready for a new deal
            match next_to_deal:
                case CribbagePlayers.PLAYER_1:
                    logger.info(f"Player {self._player1} will deal.")
                    self._deal.reset_deal(self.peg_for_player2, self.peg_for_player1)
                    # Set the correct strategies for player and dealer
                    self._deal.set_player_play_strategy(self._player2_player_strategy)
                    self._deal.set_dealer_play_strategy(self._player1_dealer_strategy)
                    next_to_deal = CribbagePlayers.PLAYER_2
                case CribbagePlayers.PLAYER_2:
                    logger.info(f"Player {self._player2} will deal.")
                    self._deal.reset_deal(self.peg_for_player1, self.peg_for_player2)
                    # Set the correct strategies for player and dealer
                    self._deal.set_player_play_strategy(self._player1_player_strategy)
                    self._deal.set_dealer_play_strategy(self._player2_dealer_strategy)
                    next_to_deal = CribbagePlayers.PLAYER_1
            
            # Play the current deal
            try:
                deal_info = self._deal.play()
                # Accumulate deal results info into game results info
                match next_to_deal:
                    case CribbagePlayers.PLAYER_1:
                        # Since we already rotated next_to_deal above, Player_1 was the player for the deal we just played
                        return_val.player1_total_play_score += deal_info.player_play_score
                        return_val.player1_total_show_score += deal_info.player_show_score
                        return_val.player2_total_play_score += deal_info.dealer_play_score
                        return_val.player2_total_his_heals_score += deal_info.dealer_his_heals_score
                        return_val.player2_total_show_score += deal_info.dealer_show_score
                        return_val.player2_total_crib_score += deal_info.dealer_crib_score
                    case CribbagePlayers.PLAYER_2:
                        # Since we already rotated next_to_deal above, Player_1 was the dealer for the deal we just played
                        return_val.player2_total_play_score += deal_info.player_play_score
                        return_val.player2_total_show_score += deal_info.player_show_score
                        return_val.player1_total_play_score += deal_info.dealer_play_score
                        return_val.player1_total_his_heals_score += deal_info.dealer_his_heals_score
                        return_val.player1_total_show_score += deal_info.dealer_show_score
                        return_val.player1_total_crib_score += deal_info.dealer_crib_score
            except CribbageGameOverError as e:
                # Log why the game ended, for example, that it ended while the crib was being shown. This information is obtained from the exception.
                logger.info(e.args[0])
                # Accumulate deal info for last deal of the game into game info, because it will not have happened above, due to the exception ending the game.
                (p1_score, p2_score) = self._board.get_scores()
                if p1_score == 121:
                    return_val.winning_player = self._player1
                    return_val.winning_player_final_score = p1_score
                    return_val.losing_player_final_score = p2_score
                    return_val.deals_in_game = deal_count
                    logger.info(f"Player {self._player1} wins the game.")
                else:
                    return_val.winning_player = self._player2
                    return_val.winning_player_final_score = p2_score
                    return_val.losing_player_final_score = p1_score
                    return_val.deals_in_game = deal_count
                    logger.info(f"Player {self._player2} wins the game.")
                # Handle accumulating deal info that arrived in CribbageGameOverError into game info
                match next_to_deal:
                    case CribbagePlayers.PLAYER_1:
                        # Since we already rotated next_to_deal above, Player_1 was the player for the deal we just played
                        return_val.player1_total_play_score += e.deal_info.player_play_score
                        return_val.player1_total_show_score += e.deal_info.player_show_score
                        return_val.player2_total_play_score += e.deal_info.dealer_play_score
                        return_val.player2_total_his_heals_score += e.deal_info.dealer_his_heals_score
                        return_val.player2_total_show_score += e.deal_info.dealer_show_score
                        return_val.player2_total_crib_score += e.deal_info.dealer_crib_score
                    case CribbagePlayers.PLAYER_2:
                        # Since we already rotated next_to_deal above, Player_1 was the dealer for the deal we just played
                        return_val.player2_total_play_score += e.deal_info.player_play_score
                        return_val.player2_total_show_score += e.deal_info.player_show_score
                        return_val.player1_total_play_score += e.deal_info.dealer_play_score
                        return_val.player1_total_his_heals_score += e.deal_info.dealer_his_heals_score
                        return_val.player1_total_show_score += e.deal_info.dealer_show_score
                        return_val.player1_total_crib_score += e.deal_info.dealer_crib_score
                break
        
            except UserResponseCollectorTerminateQueryingThreadError as e:
                # For now, do nothing but (1) Log that game terminated early, and (2) return a default CribbageGameInfo object
                # TODO: Investigate any problems
                logger.info(f"Cribbage game terminating in the middle of play, at request of user.")
                return CribbageGameInfo()

            # Log end of deal board
            logger.info(f"After deal {str(deal_count)}:\n{str(self._board)}")
 
        # Log end of game results
        logger.info(f"At game end, after {deal_count} deals:\n{str(self._board)}")
        logger.info(f"     Winning Player: {return_val.winning_player}")
        logger.info(f"     Winning Player Final Score: {return_val.winning_player_final_score}")
        logger.info(f"     Losing Player Final Score: {return_val.losing_player_final_score}")
        logger.info(f"Statistics for {self._player1}:")
        logger.info(f"     Total Play Score: {return_val.player1_total_play_score}")
        logger.info(f"     Total His Heals Score: {return_val.player1_total_his_heals_score}")
        logger.info(f"     Total Show Score: {return_val.player1_total_show_score}")
        logger.info(f"     Total Crib Score: {return_val.player1_total_crib_score}")
        logger.info(f"     Check Sum: {return_val.player1_total_play_score + return_val.player1_total_his_heals_score + return_val.player1_total_show_score + return_val.player1_total_crib_score}")
        logger.info(f"Statistics for {self._player2}:")
        logger.info(f"     Total Play Score: {return_val.player2_total_play_score}")
        logger.info(f"     Total His Heals Score: {return_val.player2_total_his_heals_score}")
        logger.info(f"     Total Show Score: {return_val.player2_total_show_score}")
        logger.info(f"     Total Crib Score: {return_val.player2_total_crib_score}")
        logger.info(f"     Check Sum: {return_val.player2_total_play_score + return_val.player2_total_his_heals_score + return_val.player2_total_show_score + return_val.player2_total_crib_score}")

        return return_val


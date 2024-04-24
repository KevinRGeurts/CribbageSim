# Standard imports
import logging

# Local imports
from exceptions import CribbageGameOverError
from CribbageGameOutputEvents import CribbageGameOutputEvents, CribbageGameLogInfo


class CribbageBoard(object):
    """
    Represents a cribbage board, so that progress through the game can be kept for both players.
    """
    
    def __init__(self):
        """
        Construct a cribbage board.
        """
        # x_current = the peg position of the leading peg, that is, the current score
        # x_previous = the peg position of the traling peg, that is the score prior to the latest pegging 
        self._player1_current = 0
        self._player1_previous = 0
        self._player2_current = 0
        self._player2_previous = 0
        
    def peg_for_player1(self, points = 1):
        """
        Peg the argument points for player 1, by leapfrogging the trailing peg points number of holes past the leading peg.
        :parameter points: The number of points to peg, int
        :return: The current score for player 1, after pegging points, int
        """
        assert(points>0)
        # Get the logger 'cribbage_logger'
        logger = logging.getLogger('cribbage_logger')

        self._player1_previous = self._player1_current
        self._player1_current += points
        if self._player1_current >= 121:
            self._player1_current = 121
            raise CribbageGameOverError
        logger.info(f"Player 1 peg locations: {self._player1_current},{self._player1_previous}",
                    extra=CribbageGameLogInfo(event_type=CribbageGameOutputEvents.UPDATE_SCORE_PLAYER1,
                                              score_player1=(self._player1_current,self._player1_previous)))
        return self._player1_current
        
    def peg_for_player2(self, points = 1):
        """
        Peg the argument points for player 2, by leapfrogging the trailing peg points number of holes past the leading peg.
        :parameter points: The number of points to peg, int
        :return: The current score for player 2, after pegging points, int
        """
        assert(points>0)
        # Get the logger 'cribbage_logger'
        logger = logging.getLogger('cribbage_logger')

        self._player2_previous = self._player2_current
        self._player2_current += points
        if self._player2_current >= 121:
            self._player2_current = 121
            raise CribbageGameOverError
        logger.info(f"Player 2 peg locations: {self._player2_current},{self._player2_previous}",
                    extra=CribbageGameLogInfo(event_type=CribbageGameOutputEvents.UPDATE_SCORE_PLAYER2,
                                              score_player2=(self._player2_current,self._player2_previous)))
        return self._player2_current
    
    def get_scores(self):
        """
        Return the current scores for both players.
        :return: (player 1 score, player 2 score), tuple
        """
        return (self._player1_current, self._player2_current)
    
    def get_player1_status(self):
        """
        Return the location of both leading and trailing pegs for player 1.
        :return: (Leading peg location, Trailing peg location), tuple
        """
        return (self._player1_current, self._player1_previous)
    
    def get_player2_status(self):
        """
        Return the location of both leading and trailing pegs for player 2.
        :return: (Leading peg location, Trailing peg location), tuple
        """
        return (self._player2_current, self._player2_previous)
    
    def __str__(self):
        """
        Return a string representing the current state of the board.
        """
        s = f"Player 1: Current = {self._player1_current}, Previous = {self._player1_previous}\n"
        s += f"Player 2: Current = {self._player2_current}, Previous = {self._player2_previous}"
        return s
        
        





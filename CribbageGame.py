# Standard imports
from enum import Enum

# Local imports
from CribbageBoard import CribbageBoard
from CribbageDeal import CribbageDeal
from CribbagePlayStrategy import CribbagePlayStrategy, InteractiveCribbagePlayStrategy
from exceptions import CribbageGameOverError

class CribbagePlayers(Enum):
    """
    An enumeration of the participants in a cribbage simulator.
    """
    PLAYER_1 = 1 
    PLAYER_2 = 2


class CribbageGame:
    """
    Class representing a cribbage game, to be played out by two players, player1 and player2.
    """
    
    def __init__(self, name1 = 'player 1', name2 = 'player 2',
                 strategy1 = InteractiveCribbagePlayStrategy(), strategy2 = InteractiveCribbagePlayStrategy()):
        """
        Construct a cribbage game with a CribbageBoard, two player names, and a CribbageDeal.
        :parameter name1: Name of player1, string
        :parameter name2: Name of player2, string
        :parameter strategy1: Playing strategy for player1, Instance of CribbagePlayStrategy
        :parameter strategy2: Playing strategy for player2, Instance of CribbagePlayStrategy
        """
        assert(isinstance(strategy1, CribbagePlayStrategy))
        assert(isinstance(strategy2, CribbagePlayStrategy))
        self._board = CribbageBoard()
        self._player1 = name1
        self._player2 = name2
        self._deal = CribbageDeal(strategy1, strategy2)

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
        :return: (Name of Winning Player, Winning Player Final Score, Losing Player Final Score, Number of Deals In Game), tuple (string, int, int, int)
        """

        game_over = False
        deal_count = 0
        return_val = ('nobody', 0, 0, 0)
        
        # TODO: For now player1 will always deal first, but implement random selection, such as cutting for high card
        # Consider that this predictability is beneficial to unit testing.
        next_to_deal = CribbagePlayers.PLAYER_1
        
        while not game_over:
        
            deal_count += 1
            
            # Reset deal so we are ready for a new deal
            match next_to_deal:
                case CribbagePlayers.PLAYER_1:
                    print(f"Player {self._player1} will deal.")
                    self._deal.reset_deal(self.peg_for_player2, self.peg_for_player1)
                    next_to_deal = CribbagePlayers.PLAYER_2
                case CribbagePlayers.PLAYER_2:
                    print(f"Player {self._player2} will deal.")
                    self._deal.reset_deal(self.peg_for_player1, self.peg_for_player2)
                    next_to_deal = CribbagePlayers.PLAYER_1
            
            # Play the current deal
            try:
                self._deal.play()
            except CribbageGameOverError:
                (p1_score, p2_score) = self._board.get_scores()
                if p1_score == 121:
                    return_val = (self._player1, p1_score, p2_score, deal_count)
                    print(f"Player {self._player1} wins the game.")
                else:
                    print(f"Player {self._player2} wins the game.")
                    return_val = (self._player2, p2_score, p1_score, deal_count)
                break

            # Print out end of deal board
            print(f"After deal {str(deal_count)}:\n{str(self._board)}")

        # Print out end of game results
        print(f"At game end, after {deal_count} deals:\n{str(self._board)}")

        return return_val


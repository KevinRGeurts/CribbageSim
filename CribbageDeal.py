# Standard imports
from enum import Enum

# Local imports
from card import Card
from deck import Deck
from hand import Hand
from CribbagePlayStrategy import CribbagePlayStrategy
from CribbageCombination import FifteenCombinationPlaying, PairCombination, FifteenCombination, RunCombination, FlushCombination, HisNobsCombination, PairCombinationPlaying, RunCombinationPlaying


class CribbageRole(Enum):
    """
    An enumeration of the roles of participants in a cribbage simulator.
    """
    DEALER = 1 
    PLAYER = 2


class CribbageDeal:
    """
    Class representing a single deal in cribbage, to be played out by a dealer and a player.
    """
    
    def __init__(self, player_strategy = CribbagePlayStrategy(), dealer_strategy = CribbagePlayStrategy()):
        """
        Construct a finite deck of Cards, an empty dealer Hand, an empty player Hand, and, and empty crib Hand.
        Create a starter card, which is expected to be replaced with a dealt one.
        Set strategies for dealer and player hand play.
        Create empgy Hand(s) for the dealer and player "played cards" piles during a go round. Also create an empty Hand for the combined
            pile. Expect combined pile to be passed as information to play strategies when following, and for scoring determination
            during play. Expect individual piles to be displayed such as during interactive play.
        :parameter player_strategy: CribbagePlayStrategy instance used to play player hand, CribbagePlayStrategy or child instance
        :parameter dealerer_strategy: CribbagePlayStrategy instance used to play dealer hand, CribbagePlayStrategy or child instance
        """
        self._deck = Deck(isInfinite = False)
        self._dealer_hand = Hand()
        self.set_dealer_play_strategy(dealer_strategy)
        # TODO: Determine if _dealer_pile is needed
        self._dealer_pile = Hand()
        self._dealer_score = 0
        self._player_hand = Hand()
        self._crib_hand = Hand()
        self.set_player_play_strategy(player_strategy)
        # TODO: Determine if _player_pile is needed
        self._player_pile = Hand()
        self._player_score = 0
        self._combined_pile = Hand()
        self._starter = Card()
        self._play_combinations = [FifteenCombinationPlaying(), PairCombinationPlaying(), RunCombinationPlaying()]
        self._show_combinations = [PairCombination(), FifteenCombination(), RunCombination(), FlushCombination(), HisNobsCombination()]

    def set_player_play_strategy(self, ps = CribbagePlayStrategy()):
        """
        Set the player play strategy.
        :parameter ps: The player play strategy, CribbagePlayStrategy()
        :return: None
        """
        assert(isinstance(ps, CribbagePlayStrategy))
        self._player_play_strategy = ps
        return None
            
    def set_dealer_play_strategy(self, ps = CribbagePlayStrategy()):
        """
        Set the dealer play strategy.
        :parameter ps: The dealer play strategy, CribbagePlayerPlayStrategy()
        :return: None
        """
        assert(isinstance(ps, CribbagePlayStrategy))
        self._dealer_play_strategy = ps
        return None

    def get_combined_play_pile(self):
        """
        Return a list of cards in the combined play pile.
        :return: A list of the cards in the combined play pile, List of Card instances
        """
        return list(self._combined_pile.get_cards())
    
    def draw_for_dealer(self, number=1):
        """
        Draw one or more cards from deck into dealer's hand.
        :parameter number: How many cards to draw into dealer's hand, int
        :return: A list of Card(s) in the hand after the draw
        """
        return self._dealer_hand.add_cards(self._deck.draw(number))

    def draw_for_player(self, number=1):
        """
        Draw one or more cards from deck into player's hand.
        :parameter number: How many cards to draw into player's hand, int
        :return: A list of Card(s) in the hand after the draw
        """
        return self._player_hand.add_cards(self._deck.draw(number))

    def get_player_hand(self):
        """
        Return the cards remaining in the player's hand as a list.
        :return: List of cards that are remaining in the player's hand, list
        """
        return list(self._player_hand.get_cards())

    def get_dealer_hand(self):
        """
        Return the cards remaining in the dealer's hand as a list.
        :return: List of cards that are remaining in the dealer's hand, list
        """
        return list(self._dealer_hand.get_cards())

    def draw_starter_card(self):
        """
        Draw one card from deck to be the starter card.
        :return: The starter card, Card object
        """
        self._starter = self._deck.draw()
        return self._starter

    def play_card_for_player(self, index = 0):
        """
        Play the card at index location in the player's hand. Remove it from the player's hand, and add it to the player's and combined piles.
        :parameter index: The index location in the player's hand of the card to play, int [0...number of cards in hand - 1]
        :return: The pips count of the card played, int
        """
        card = self._player_hand.remove_card(index)
        self._player_pile.add_cards(card)
        self._combined_pile.add_cards(card)
        return card.count_card()
        
    def play_card_for_dealer(self, index = 0):
        """
        Play the card at index location in the dealer's hand. Remove it from the dealer's hand, and add it to the dealer's and combined piles.
        :parameter index: The index location in the dealer's hand of the card to play, int [0...number of cards in hand - 1]
        :return: The pips count of the card played, int
        """
        card = self._dealer_hand.remove_card(index)
        self._dealer_pile.add_cards(card)
        self._combined_pile.add_cards(card)
        return card.count_card()

    def peg_for_player(self, count = 1):
        """
        Add count to the player's score.
        :parameter count: The number of pegs (points) to add to the player's score, int
        :return: The current player point score, int
        """
        self._player_score += count
        return self._player_score

    def peg_for_dealer(self, count = 1):
        """
        Add count to the dealer's score.
        :parameter count: The number of pegs (points) to add to the dealer's score, int
        :return: The current dealer point score, int
        """
        self._dealer_score += count
        return self._dealer_score

    def xfer_player_card_to_crib(self, index = 0):
        """
        Transfer the card at index location in the player's hand to the crib. Remove it from the player's hand.
        :parameter index: The index location in the player's hand of the card to play, int [0...number of cards in hand - 1]
        :return None:
        """
        card = self._player_hand.remove_card(index)
        self._crib_hand.add_cards(card)
        return None

    def xfer_dealer_card_to_crib(self, index = 0):
        """
        Transfer the card at index location in the dealer's hand to the crib. Remove it from the dealer's hand.
        :parameter index: The index location in the dealer's hand of the card to play, int [0...number of cards in hand - 1]
        :return None:
        """
        card = self._dealer_hand.remove_card(index)
        self._crib_hand.add_cards(card)
        return None

    def determine_score_showing(self, hand = Hand(), starter = None):
        """
        Determine the score of hand during show.
        :parameter hand: The hand to score, Hand instance
        :parameter starter: The starter card, Card instance
        :return: The total score of all combinations in the hand, int
        """
        score = 0
        for combo in self._show_combinations:
            info = combo.score(hand, starter)
            print(info)
            score += info.score
        return score

    def determine_score_playing(self, combined_pile = Hand()):
        """
        Determine the score during play.
        :parameter hand: The combined, ordered pile of played cards to check for a score, Hand instance
        :return: Points scored based on play of last card, int
        """
        score = 0
        for combo in self._play_combinations:
            info = combo.score(combined_pile)
            print(info)
            score += info.score
        return score

    def log_pegging_info(self):
        """
        Currently outputs to stdout current state of pegging for dealer and player cumulatively during the hand.
        Eventually this will be converted to use logging.
        :return: None
        """
        print('Dealer total score thus far for the dealt hand: ', str(self._dealer_score))
        print('Player total score thus far for the dealt hand: ', str(self._player_score))
        return None
    
    def log_play_info(self, preface = '', go_round_count = 0):
        """
        Currently outputs to stdout current state of hands, play piles, play count, and scores. Eventually this will be converted to using logging.
        :parameter preface: A string to use as a header for the output, for example to indicate that it is 'after lead', 'after follow', 'after go', etc., string
        :parameter go_round_count: The current play count during the go round, int
        :return: None
        """
        header = preface
        header += ':'
        print(header)
        print('     Dealer hand after lead: ', str(self._dealer_hand))
        print('     Dealer pile after lead: ', str(self._dealer_pile))
        print('     Player hand after lead: ', str(self._player_hand))
        print('     Player pile after lead: ', str(self._player_pile))
        print('     Combined pile after lead: ', str(self._combined_pile))
        print('     Play count after lead: ', str(go_round_count))
        return None

    def play(self):
        """
        Play the cribbage deal.
        """
        # Shuffle, that is, rebuild the deck
        self._deck.create_deck()
        
        # Deal player and dealer hands from the deck. In a normal game, this would be one card at a time alternating.
        # However, in this case it is advantageous to deal all six cards to each hand at once, to facilitate using a stacked deck for testing.
        self.draw_for_player(6)
        print('Dealt player hand: ', str(self._player_hand))
        self.draw_for_dealer(6)
        print('Dealt dealer hand: ', str(self._dealer_hand))
       
        # Apply the player and dealer strategies to have player and dealer select two cards each from their hands to form the crib.
        self._player_play_strategy.form_crib(self.xfer_player_card_to_crib, self.get_player_hand)
        self._dealer_play_strategy.form_crib(self.xfer_dealer_card_to_crib, self.get_dealer_hand)
        print('Player hand after crib formed: ', str(self._player_hand))
        print('Dealer hand after crib formed: ', str(self._dealer_hand))
        print('Crib hand: ', str(self._crib_hand))

        # Deal the starter card. IFF it is a Jack, peg 2 for the dealer.
        starter = self.draw_starter_card()
        print('Starter card: ', str(starter))
        if starter.get_pips() == 'J':
            # Peg 2 for dealer
            self.peg_for_dealer(2)

        # Set variable that tracks which player will play next.
        # For the first go round, the player always leads.    
        next_to_play = CribbageRole.PLAYER    
            
        # TODO: Create a loop at this level that plays multiple go rounds until the dealt cards for both players are exhausted 
        while len(self._dealer_hand) > 0 or len(self._player_hand) > 0:   
            
            # Set the go round cumulative score to 0
            go_round_count = 0
            go_declared = False
        
            # Clear the combined pile of cards played during the go round, as this pile is used for scoring during play
            self._combined_pile = Hand()

            # Whoever is next to play leads the "go" round. Use their play strategy to do so.
            # Try commenting this out to see if it allows play through to the exhasution of cards. I think the only downside of this
            # is that a player who runs out of cards in the previous go round may need to declare a go in the next round.
            # match next_to_play:
            #     case CribbageRole.PLAYER:
            #         count = self._player_play_strategy.lead(self.play_card_for_player, self.get_player_hand)
            #         next_to_play = CribbageRole.DEALER
            #     case CribbageRole.DEALER:
            #         count = self._dealer_play_strategy.lead(self.play_card_for_dealer, self.get_dealer_hand)
            #         next_to_play = CribbageRole.PLAYER
            # go_round_count += count
            # self.log_play_info('After lead', go_round_count)

            # If go_declared, then it is a signal that the go round has finished inside this while loop by playing out a go, and it is
            # time to return to the outside while and launch the next go round. if go_round_count == 31, then it is a signal that the 
            # go round has finished inside this while loop by play count reaching exactly 31, and again, it is time to return to the outside
            # while loop.
            while not go_declared and go_round_count != 31:

                # Whoever is next to play follows using their play strategy.
                match next_to_play:
                    case CribbageRole.PLAYER:
                        (count, go_declared) = self._dealer_play_strategy.follow(go_round_count, self.play_card_for_player, self.get_player_hand)
                        # Assess if any score in play has occured based on the player's follow. If so, peg it for the player.
                        score = self.determine_score_playing(self._combined_pile)
                        print('Score: ', str(score))
                        self.peg_for_player(score)
                        # Rotate who will play next
                        next_to_play = CribbageRole.DEALER
                    case CribbageRole.DEALER:
                        (count, go_declared) = self._dealer_play_strategy.follow(go_round_count, self.play_card_for_dealer, self.get_dealer_hand)
                        # Assess if any score in play has occured based on the dealer's follow. If so, peg it for the dealer.
                        score = self.determine_score_playing(self._combined_pile)
                        print('Score: ', str(score))
                        self.peg_for_dealer(score)
                        # Rotate who will play next
                        next_to_play = CribbageRole.PLAYER
                go_round_count += count

                self.log_play_info('After follow', go_round_count)
                print('Go Declared?: ', str(go_declared))

                # Has count for the go round reached exactly 31?
                if go_round_count == 31:
                    print('Go round ends with count of 31.')
                    match next_to_play:
                        case CribbageRole.PLAYER:
                            # Since we rotate who will play next above, this means that dealer played to reach 31
                            self.peg_for_dealer(2)
                        case CribbageRole.Dealer:
                            # Since we rotate who will play next above, this means that player played to reach 31
                            self.peg_for_player(2)
                    continue # Get us out of the while.

                if (go_declared):
                    # Instruct the next_to_play to try to play out to 31
                    match next_to_play:
                        case CribbageRole.PLAYER:
                            count = self._player_play_strategy.go(go_round_count, self.play_card_for_player, self.get_player_hand,
                                                                  self.get_combined_play_pile, self.determine_score_playing, self.peg_for_player)
                            # Score 1 or 2 for the player, or 1 for the dealer, depending on how they player played out the go
                            if count > 0:
                                # Player was able to play one or more cards, peg 2 for a 31 or 1 for the go
                                go_round_count += count
                                if (go_round_count) == 31:
                                    self.peg_for_player(2)
                                else:
                                    self.peg_for_player(1)
                                # Rotate who will play next
                                next_to_play = CribbageRole.DEALER
                            else:
                                # Player was not able to play any cards, so peg one for the dealer, for the go
                                self.peg_for_dealer(1)
                                # Do NOT rotate who will play next, since the go declaration did not result in any cards being played
                        case CribbageRole.DEALER:
                            count = self._dealer_play_strategy.go(go_round_count, self.play_card_for_dealer, self.get_dealer_hand,
                                                                  self.get_combined_play_pile, self.determine_score_playing, self.peg_for_dealer)
                            # Score 1 or 2 for the dealer, or 1 for the player, depending on how they dealer played out the go
                            if count > 0:
                                # Dealer was able to play one or more cards, peg 2 for a 31 or 1 for the go
                                go_round_count += count
                                if (go_round_count) == 31:
                                    self.peg_for_dealer(2)
                                else:
                                    self.peg_for_dealer(1)
                                # Rotate who will play next
                                next_to_play = CribbageRole.PLAYER
                            else:
                                # Dealer was not able to play any cards, so peg one for the player, for the go
                                self.peg_for_player(1)
                                # Do NOT rotate who will play next, since the go declaration did not result in any cards being played
                    self.log_play_info('After go', go_round_count)
                    continue # Get us out of the while.
            
                # If go has not been declared, then continuing alternating follows, until go is declared, or we run out of cards in both hands
                # That is, the while should keep cycling
                # end of while not go_declared:
        
        
            # Time for "showing" that is scoring hands. Use the set of CribbageCombination's to score, in order, player's hand, dealer's hand, crib.
            # Peg appropriately.
            

        
        # Play continues until both dealer and player are out of cards.
        # end of while dealer or player have cards left in their hand
            
        # TODO: After determining score from showing hands, print out the scoring combinations

        # It's time to show (that is, count the hands after playing). During play, the hands have been emptied into the play piles, so score the piles.
 
        # Score the player's hand
        score = self.determine_score_showing(self._player_pile, starter)
        self.peg_for_player(score)
        print('Player score from showing hand: ', score)
        
        # Score the dealer's hand
        score = self.determine_score_showing(self._dealer_pile, starter)
        self.peg_for_dealer(score)
        print('Dealer score from showing hand: ', score)
        
        # Score the dealer's crib
        score = self.determine_score_showing(self._crib_hand, starter)
        self.peg_for_dealer(score)
        print('Dealer score from showing crib: ', score)

        self.log_pegging_info()

        # If at any time during play, player or dealer pegs to end of board, game is over.

        # If at any time during showing, player or dealer pegs to end of board, game is over.

        return None
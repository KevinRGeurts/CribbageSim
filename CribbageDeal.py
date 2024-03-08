# Standard imports

# Local imports
from card import Card
from deck import Deck
from hand import Hand
from CribbagePlayStrategy import CribbagePlayStrategy
from CribbageCombination import PairCombination, FifteenCombination, RunCombination, FlushCombination, HisNobsCombination, PairCombinationPlaying, RunCombinationPlaying


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
        self._dealer_pile = Hand()
        self._dealer_score = 0
        self._player_hand = Hand()
        self._crib_hand = Hand()
        self.set_player_play_strategy(player_strategy)
        self._player_pile = Hand()
        self._player_score = 0
        self._combined_pile = Hand()
        self._starter = Card()
        self._play_combinations = [PairCombinationPlaying(), RunCombinationPlaying()]
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

    # TODO: Logic for scoring while playing needs to be more complex. Can't just iterate through the list of combinations.
    # When looking for a pair, must only look at the last two cards in the combined pile
    # When looking for a 15, can look back more than two cards, but can't include all cards previously used to score a 15. That is, don't score the same 15 twice.
    # When looking for a run, can look back more than three cards, but can't include all cards previously used to score a run unless we've made a longer run
    # by adding the last card. That is, don't score the same run twice.
    # Might need to do this by scoring twice. Once with the current pile less last card, and then again with the current pile as is, and compare the two results.
    # But honestly, I'm a bit at a loss on this.
    def determine_score_playing(self, play_count = 0, combined_pile = Hand()):
        """
        Determine the score during play.
        :parameter play_count: The current count for the current go round, int
        :parameter hand: The combined, ordered pile of played cards to check for a score, Hand instance
        :return: Points scored based on play of last card, int
        """
        score = 0
        # Check for 15 by looking only at the current play_count
        if (play_count == 15):
            score += 2
        # Check for a double pair royal, pair royal, and pair
        for combo in self._play_combinations:
            info = combo.score(combined_pile)
            print(info)
            score += info.score
        return score

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

        # Set the go round cumulative score to 0
        go_round_count = 0
        go_declared = False

        # Non-dealer, i.e., the player, leads the first "go" round. Use the player play strategy to do so.
        count = self._player_play_strategy.lead(self.play_card_for_player, self.get_player_hand)
        go_round_count += count
        print('Player hand after lead: ', str(self._player_hand))
        print('Player pile after lead: ', str(self._player_pile))
        print('Combined pile after lead: ', str(self._combined_pile))
        print('Play count after lead: ', str(go_round_count))

        while not go_declared:

            # Dealer follows using the dealer play strategy.
            (count, go_declared) = self._dealer_play_strategy.follow(go_round_count, self.play_card_for_dealer, self.get_dealer_hand)
            go_round_count += count
            
            print('Dealer hand after follow: ', str(self._dealer_hand))
            print('Dealer pile after follow: ', str(self._dealer_pile))
            print('Combined pile after follow: ', str(self._combined_pile))
            print('Play count after follow: ', str(go_round_count))
            print('Go Declared?: ', str(go_declared))

            # TODO: Assess if any score in play has occured based on the dealer's follow. If so, peg it for the dealer.
            # score = self.determine_score(self._combined_pile)
            # print('Score: ', str(score))
            # self.peg_for_dealer(score)
            
            if (go_declared):
                # Instruct the player to try to play out to 31
                count = self._player_play_strategy.go(go_round_count, self.play_card_for_player, self.get_player_hand)
                # Score 1 or 2 for the player, or 1 for the dealer, depending on how they player played out the go
                if count > 0:
                    # Player was able to play one or more cards, peg 2 for a 31 or 1 for the go
                    go_round_count += count
                    if (go_round_count) == 31:
                        self.peg_for_player(2)
                    else:
                        self.peg_for_player(1)
                else:
                    # Player was not able to play any cards, so peg one for the dealer, for the go
                    self.peg_for_dealer(1)
                print('Dealer hand after go: ', str(self._dealer_hand))
                print('Dealer pile after go: ', str(self._dealer_pile))
                print('Player hand after go: ', str(self._player_hand))
                print('Player pile after go: ', str(self._player_pile))
                print('Combined pile after go ', str(self._combined_pile))
                print('Play count after go: ', str(go_round_count))
                continue # Get us out of the while.

            # Player follows using the player play strategy
            (count, go_declared) = self._player_play_strategy.follow(go_round_count, self.play_card_for_player, self.get_player_hand)
            go_round_count += count
            
            print('Player hand after follow: ', str(self._player_hand))
            print('Player pile after follow: ', str(self._player_pile))
            print('Combined pile after follow: ', str(self._combined_pile))
            print('Play count after follow: ', str(go_round_count))
            print('Go Declared?: ', str(go_declared))

            # TODO: Assess if any score in play has occured based on the player's follow. If so, peg it for the player.
            # score = self.determine_score(self._combined_pile)
            # print('Score: ', str(score))
            # self.peg_for_dealer(score)

            if (go_declared):
                # Instruct the dealer to try to play out to 31
                count = self._dealer_play_strategy.go(go_round_count, self.play_card_for_dealer, self.get_dealer_hand)
                # Score 1 or 2 for the dealer, or 1 for the player, depending on how they dealer played out the go
                if count > 0:
                    # dealer was able to play one or more cards, peg 2 for a 31 or 1 for the go
                    go_round_count += count
                    if (go_round_count) == 31:
                        self.peg_for_dealer(2)
                    else:
                        self.peg_for_dealer(1)
                else:
                    # Dealer was not able to play any cards, so peg one for the player, for the go
                    self.peg_for_player(1)
                print('Dealer hand after go: ', str(self._dealer_hand))
                print('Dealer pile after go: ', str(self._dealer_pile))
                print('Player hand after go: ', str(self._player_hand))
                print('Player pile after go: ', str(self._player_pile))
                print('Combined pile after go ', str(self._combined_pile))
                print('Play count after go: ', str(go_round_count))
                continue # Get us out of the while.

                # If go has not been declared, then continuing alternating follows, until go is declared, or we run out of cards in both hands
                # That is, the while should keep cycling
        
        
            # Play continues until both dealer and player are out of cards.

            # If at any time during play, player or dealer pegs to end of board, game is over.

        # Time for "showing" that is scoring hands. Use the set of CribbageCombination's to score, in order, player's hand, dealer's hand, crib.
        # Peg appropriately.

        # If at any time during showing, player or dealer pegs to end of board, game is over.
        


        return None
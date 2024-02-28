# Standard imports

# Local imports


class CribbagePlayStrategy:
    """
    Following a Strategy design pattern, this is the interface class for all cribbage hand playing strategies.
    Each child must by convention and necessity implement these methods:
        form_crib(...) - For selecting two cards from the dealt six to be placed in the crib 
        lead(...) - For selecting the first card to play after a round of play has finished after a "go"
        follow(...) - For selecting subsequent cards to play seeking finally a "go". This logic will depend on all cards played so far during
            the current "go" round by both dealer and player. Could also depend on how close to done the game is, since when a player is a few
            pegs from winning and the game is close, scoring during play may be more valualbe than getting a high count during show.
    """

    # Note: Will need separate strategies for dealer and player, since, for example, form_crib(...) logic will depend heavily on who dealt


class DummyCribbagePlayStrategy(CribbagePlayStrategy):
    """
    An very simple and very dumb implementation of CribbagePlayStrategy, intended only to be used during initial development of the simulator,
    so that overall algorithmic flow of playing can be worked out before working about playing well.
    """
    
    def form_crib(self, xfer_to_crib_callback):
        """
        Forms the crib by providing the first two cards in the hand, regardless of what they are.
        :parameter xfer_to_crib_callback: Bound method used to transfer cards from hand to crib, e.g., CribbageDeal.xfer_player_card_to_crib
        :return: None
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(xfer_to_crib_callback))
        
        # This is a dumb former of the crib, so just dump the first two cards in the hand
        xfer_to_crib_callback(0)
        xfer_to_crib_callback(0)
        return None

    def lead(self, play_card_callback):
        """
        Leads (plays) the first remaining card in the hand, regardless of what it is.
        :parameter play_card_callback: Bound method used to play a card from hand, e.g., CribbageDeal.play_card_for_player
        :return: None
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(play_card_callback))
        
        # This is a dumb player, always playing the first card left in the hand
        play_card_callback(0)
        return None

    def follow(self, play_card_callback):
        """
        Follows (plays) by playing the first remaining card in the hand, regardless of what it is.
        :parameter play_card_callback: Bound method used to play a card from hand, e.g., CribbageDeal.play_card_for_player
        :return: None
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(play_card_callback))
        
        # This is a dumb player, always playing the first card left in the hand
        play_card_callback(0)
        return None

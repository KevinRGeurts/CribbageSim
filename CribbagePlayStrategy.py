# Standard imports
from enum import Enum

# Local imports
from UserResponseCollector import UserResponseCollector_query_user, BlackJackQueryType
from CribbageCombination import CribbageComboInfo
from CribbageCombination import CribbageCombinationShowing, PairCombination, FifteenCombination, RunCombination, FlushCombination
from hand import Hand


class CribbageCribOption:
    """
    A class with structured information about a possible option for forming the crib. All class attributes are intended to be "public".
        hand: List of 4 cards to be retained in the hand if a crib is formed using this option, list of Card objects
        hand_score: The guaranteed score of the cards in the hand when the hand is shown, that is, the score of the cards without
            consideration of a possible starter card, int
        crib: List of 2 cards to be layed in teh crib if a crib is formed using this option, list of Card objects
        crib_score: The guaranteed score of the two cards in the crib when the crib is shown, that is, the score of the cards without
            consideration of a possible starter card or the other player's contribution to the crib, int
    """
    def __init__(self):
        """
        Construct an object of this class.
        """
        self.hand = []
        self.hand_score = 0
        self.crb = []
        self.crib_score = 0

    def __str__(self):
        hand = Hand()
        hand.add_cards(self.hand)
        crib = Hand()
        crib.add_cards(self.crib)
        return f"{hand},{self.hand_score},{crib},{self.crib_score}"


class CribbagePlayStrategy:
    """
    Following a Strategy design pattern, this is the interface class for all cribbage hand playing strategies.
    Each child must by convention and necessity implement these methods:
        form_crib(...) - For selecting two cards from the dealt six to be placed in the crib 
        follow(...) - For selecting subsequent cards to play seeking finally a "go". This logic will depend on all cards played so far during
            the current "go" round by both dealer and player. Could also depend on how close to done the game is, since when a player is a few
            pegs from winning and the game is close, scoring during play may be more valualbe than getting a high count during show.
        go(...) - For playing out as many cards as possible AFTER opponent has declared "go".
    """
    
    def form_crib(self, xfer_to_crib_callback, get_hand_callback, play_recorder_callback=None):
        """
        This is an abstract method that MUST be implemented by children. If called, it will raise NotImplementedError
        Called to decide which cards from the hand to place in the crib.
        :parameter xfer_to_crib_callback: Bound method used to transfer cards from hand to crib, e.g., CribbageDeal.xfer_player_card_to_crib
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :parameter play_recorder_callback: Bound method used to record user choices for cards to lay off in the crib
        :return: None
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(xfer_to_crib_callback))
        assert(callable(get_hand_callback))
        if play_recorder_callback: assert(callable(play_recorder_callback))
        raise NotImplementedError
        return None

    def follow(self, go_count, play_card_callback, get_hand_callback, get_play_pile_callback, play_recorder_callback=None):
        """
        This is an abstract method that MUST be implemented by children. If called, it will raise NotImplementedError
        Called to decide which card to follow (play) in a go round.
        :parameter go_count: The current cumulative count of the go round before the follow, int
        :parameter play_card_callback: Bound method used to play a card from hand, e.g., CribbageDeal.play_card_for_player
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :parameter get_play_pile_callback: Bound method used to obtain the pile of played cards, e.g., CribbageDeal.get_player_hand
        :parameter play_recorder_callback: Bound method used to record user choices for cards to lay off in the crib
        :return: (The pips count of the card played as int, Go declared as boolean), tuple
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(play_card_callback))
        assert(callable(get_hand_callback))
        assert(callable(get_play_pile_callback))
        if play_recorder_callback: assert(callable(play_recorder_callback))
        raise NotImplementedError
        return ('10', False)

    def go(self, go_count, play_card_callback, get_hand_callback, get_play_pile_callback, score_play_callback, peg_callback,
           play_recorder_callback=None):
        """
        This is an abstract method that MUST be implemented by children. If called, it will raise NotImplementedError
        Deter,ome which card(s) if any to play in a go round after opponent has declared go.
        :parameter go_count: The current cumulative count of the go round that caused opponent to declare go, int
        :parameter play_card_callback: Bound method used to play a card from hand, e.g., CribbageDeal.play_card_for_player
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :parameter get_play_pile_callback: Bound method used to obtain the pile of played cards, e.g., CribbageDeal.get_player_hand
        :parameter score_play_callback: Bound method used to determine any scoring while go is being played out, e.g., CribbageDeal.determine_score_playing
        :parameter peg_callback: Bound method used to determine any scoring while go is being played out, e.g., CribbageDeal.peg_for_player
        :parameter play_recorder_callback: Bound method used to record user choices for cards to lay off in the crib
        :return: The sum of pips count of any cards played, int
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(play_card_callback))
        assert(callable(get_hand_callback))
        assert(callable(score_play_callback))
        assert(callable(peg_callback))
        if play_recorder_callback: assert(callable(play_recorder_callback))
        raise NotImplementedError
        return 0


    # Note: Will need separate strategies for dealer and player, since, for example, form_crib(...) logic will depend heavily on who dealt


class HoyleishCribbagePlayStrategy(CribbagePlayStrategy):
    """
    Base class for dealer and player play strategies based initially/roughly on "Strategy for Cribbage" described in Hoyle. The "ish"
    implies that not all recommendations from Hoyle may be implemented, and other strategy components may be implemented alternatively or
    in addition too.
    """
    def __init__(self):
        """
        Construct an object of this class.
        """
        # All elements of the _guaranteed_4card_combinations and _guaranteed_2card_combinations lists must be children of
        # CribbageCombinationShowing class.
        self._guaranteed_4card_combinations = [PairCombination(), FifteenCombination(), RunCombination(), FlushCombination()]
        self._guaranteed_2card_combinations = [PairCombination(), FifteenCombination()]
        

    def follow(self, go_count, play_card_callback, get_hand_callback, get_play_pile_callback, play_recorder_callback=None):
        """
        Follows (plays) a card based initially/roughly on "Strategy for Cribbage" described in Hoyle. The "ish" implies that not all recommendations
        from Hoyle may be implemented, and other strategy components may be implemented alternatively or in addition too.
        :parameter go_count: The current cumulative count of the go round before the follow, int
        :parameter play_card_callback: Bound method used to play a card from hand, e.g., CribbageDeal.play_card_for_player
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :parameter get_play_pile_callback: Bound method used to obtain the pile of played cards, e.g., CribbageDeal.get_player_hand
        :parameter play_recorder_callback: Bound method used to record user choices for cards to lay off in the crib
        :return: (The pips count of the card played as int, Go declared as boolean), tuple
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(play_card_callback))
        assert(callable(get_hand_callback))
        assert(callable(get_play_pile_callback))
        if play_recorder_callback: assert(callable(play_recorder_callback))
        
        # Default tuple to return, arbitrarily here a GO tuple, but expected to be set in all branches below
        return_val = (0, True)
        
        # Deteremine list of cards in the hand that can be played without go_count exceeding 31.
        playable = [c for c in get_hand_callback() if c.count_card() <= (31 - go_count)]

        if len(playable) > 0:
            if len(get_play_pile_callback()) == 0:
                # The play pile has no cards in it, so this is a lead, so call lead(...) method
                count = self.lead(play_card_callback, get_hand_callback)
                return_val = (count, False)
            else:
                # Apply logic for following
                pass
                
        else:
            # If no cards in the hand can be played, then return (0, True), in other words, declare GO.
            return (0, True) 

        return return_val

    def go(self, go_count, play_card_callback, get_hand_callback, get_play_pile_callback, score_play_callback, peg_callback):
        """
        Determine which card(s) if any to play in a go round after their opponent has declared go.
        :parameter go_count: The current cumulative count of the go round that caused opponent to declare go, int
        :parameter play_card_callback: Bound method used to play a card from hand, e.g., CribbageDeal.play_card_for_player
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :parameter get_play_pile_callback: Bound method used to obtain the pile of played cards, e.g., CribbageDeal.get_player_hand
        :parameter score_play_callback: Bound method used to determine any scoring while go is being played out, e.g., CribbageDeal.determine_score_playing
        :parameter peg_callback: Bound method used to determine any scoring while go is being played out, e.g., CribbageDeal.peg_for_player
        :return: The sum of pips count of any cards played, int
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(play_card_callback))
        assert(callable(get_hand_callback))
        assert(callable(score_play_callback))
        assert(callable(peg_callback))
        
        # This isn't implemented, so assert
        assert(False)
        return count

    # TODO: This isn't currently being used for anything. Rather than remove it entirely, keep it for now, but consider repurposing it
    # as a utility called from follow(...) when the play pile is empty. That would encapsulate a strategy specific to leading, but the card would
    # get played in the context of the follow(...) logic.
    def lead(self, play_card_callback, get_hand_callback):
        """
        Leads (plays) a first card in a go round based initially/roughly on "Strategy for Cribbage" described in Hoyle.
        The "ish" implies that not all recommendations from Hoyle may be implemented, and other strategy components may be implemented
        alternatively or in addition too. This is a utility method intended to be called by follow(...) method, not by outsiders.
        :parameter play_card_callback: Bound method used to play a card from hand, e.g., CribbageDeal.play_card_for_player
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :return: The pips count of the card played, int 
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(play_card_callback))
        assert(callable(get_hand_callback))
        
        # This is a dumb player, always playing the first card left in the hand
        count = play_card_callback(0)
        return count

    def guaranteed_hand_score(self, hand = Hand()):
        """
        Utility function that determines the show points with 100% expectation in a cribbage hand. For example, a pair is counted, but a His Nobs
        is NOT counted, because it depends on the suit of the starter, and thus would be considered to have an
        expected value of 1 pnt X 0.25 prob = 0.25 points.
        :parameter hand: The cards to score, Hand object
        :return: Total points in the hand that have 100% expectation of being counted, int
        """
        score = 0
        for combo in self._guaranteed_4card_combinations:
            assert(isinstance(combo, CribbageCombinationShowing))
            info = combo.score(hand)
            score += info.score
        return score

    def guaranteed_crib_score(self, crib = Hand()):
        """
        Utility function that determines the show points with 100% expectation in a cribbage crib contribution of 2 cards.
        For example, a pair is counted, but a His Nobs is NOT counted, because it depends on the suit of the starter, and thus would be considered to have an
        expected value of 1 pnt X 0.25 prob = 0.25 points.
        :parameter hand: The cards to score, Hand object
        :return: Total points in the crib from the 2-card contribution that have 100% expectation of being counted, int
        """
        score = 0
        for combo in self._guaranteed_2card_combinations:
            assert(isinstance(combo, CribbageCombinationShowing))
            info = combo.score(crib)
            score += info.score
        return score

    def permute_and_score_dealt_hand(self, hand = Hand()):
        """
        Utility function that permutes the dealt hand of six cards for all combinations of four cards, scores the four cards in the hand
        for each permutation, and scores teh two cards in the crib for each permutation.
        :parameter hand: The six cards to permute and score, Hand object
        :return: A list of CribbageCribOption instance with hand, crib, and scores for each permutation, list of CribbageCribOption object
        """
        assert(len(hand) == 6)
        
        # Get the cards in the hand, twice, so we have two lists that (for the moment) are duplicates
        cards_1 = list(hand)
        
        # Need a CribbageCombinationShowing() object, to access it's permutations utility method
        permutations = CribbageCombinationShowing().permutations(4, cards_1)

        # Score each permutation and make a list of tuples (list of cards, score)
        priority_list = []
        for p in permutations:
            crib_option = CribbageCribOption()
            crib_option.hand = p
            h = Hand()
            h.add_cards(p)
            p_score = self.guaranteed_hand_score(h)
            crib_option.hand_score = p_score
            priority_list.append(crib_option)
            # Generate the list of cards to be placed in the crib for permutation p, by removing cards from hand
            cards_2 = list(hand)
            for c in p:
                cards_2.remove(c)
            h = Hand()
            h.add_cards(cards_2)
            p_score = self.guaranteed_crib_score(h)
            crib_option.crib_score = p_score
            crib_option.crib = cards_2

        return priority_list

    # TODO: Create another member that returns expected values for a hand. Like a 0.25 points expected value for a jack in the hand.
    # or a (16/52)*2 EV for a 5 in the hand, based on a ten or face card being drawn as starter. What is the EV for a 2 card sequence?
    # What is the EV for a 2 card sequence with gap of one inbetween? Etc. If this is implemented, the concept is it is a secondary prioritization
    # for crib forming, over guaranteed points available in the hand. It might also be used to help determine what card to follow or go.

class HoyleishDealerCribbagePlayStrategy(HoyleishCribbagePlayStrategy):
    """
    Dealer play strategy based initially/roughly on "Strategy for Cribbage" described in Hoyle. The "ish" implies that not all recommendations
    from Hoyle may be implemented, and other strategy components may be implemented alternatively or in addition too. Dealer and player require
    different form_crib(...) implementations because it's okay for the dealer to place points in the crib, whereas the player should almost
    always avoid doing so.
    """
    
    # For the Dealer, crib formation will be based on maximizing (score in hand) + (score in crib).
    def form_crib(self, xfer_to_crib_callback, get_hand_callback, play_recorder_callback=None):
        """
        Forms the crib based initially/roughly on "Strategy for Cribbage" described in Hoyle. The "ish" implies that not all recommendations
        from Hoyle may be implemented, and other strategy components may be implemented alternatively or in addition too.
        :parameter xfer_to_crib_callback: Bound method used to transfer cards from hand to crib, e.g., CribbageDeal.xfer_player_card_to_crib
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :parameter play_recorder_callback: Bound method used to record user choices for cards to lay off in the crib
        :return: None
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(xfer_to_crib_callback))
        assert(callable(get_hand_callback))
        if play_recorder_callback: assert(callable(play_recorder_callback))

        # First crib lay away strategy from Hoyle is to count up all the show points in the hand and lay away the two cards that
        # leave the maximum possible score for the four that will remain in the hand. Here this will be augmented/modified by maximizing the combined
        # score in the hand and the crib.
         
        # Get the cards in the hand
        cards = get_hand_callback()
        
        # Generate permutations of 4-card hands / 2-card crib contributions, and score them
        h = Hand().add_cards(cards)
        priority_list = self.permute_and_score_dealt_hand(h)
        
        # Sort priority_list by descending (guaranteed_hand_score + guaranteed_crib_score)
        sorted_list = sorted(priority_list, key = lambda option: (option.hand_score + option.crib_score), reverse = True)

        # TODO: Could now filter sorted_list for all options that have the same hand_score + crib_score as the first item on the sorted list,
        # and output a debug message, probably including str(sorted_list[i] for each such option), to start to build statistics on how
        # often this prioritization scheme is ambiguous. This would be evidence of potential value in further work on prioritization, such as
        # incorporating expected probability scores.

        # Now transfer to the crib the crib cards for the highest priority option
        for c in sorted_list[0].crib:
            i = cards.index(c)
            xfer_to_crib_callback(i)
            # Refresh cards, since we've pulled a card out of the hand, and thus changed the indexing
            cards = get_hand_callback()
 
        return None


class HoyleishPlayerCribbagePlayStrategy(HoyleishCribbagePlayStrategy):
    """
    Player play strategy based initially/roughly on "Strategy for Cribbage" described in Hoyle. The "ish" implies that not all recommendations
    from Hoyle may be implemented, and other strategy components may be implemented alternatively or in addition too. Dealer and player require
    different form_crib(...) implementations because it's okay for the dealer to place points in the crib, whereas the player should almost
    always avoid doing so.
    """
    
    # For the Player, crib formation will be based on maximizing (score in hand) - (score in crib).
    def form_crib(self, xfer_to_crib_callback, get_hand_callback, play_recorder_callback=None):
        """
        Forms the crib based initially/roughly on "Strategy for Cribbage" described in Hoyle. The "ish" implies that not all recommendations
        from Hoyle may be implemented, and other strategy components may be implemented alternatively or in addition too.
        :parameter xfer_to_crib_callback: Bound method used to transfer cards from hand to crib, e.g., CribbageDeal.xfer_player_card_to_crib
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :parameter play_recorder_callback: Bound method used to record user choices for cards to lay off in the crib
        :return: None
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(xfer_to_crib_callback))
        assert(callable(get_hand_callback))
        if play_recorder_callback: assert(callable(play_recorder_callback))

        # First crib lay away strategy from Hoyle is to count up all the show points in the hand and lay away the two cards that
        # leave the maximum possible score for the four that will remain in the hand. Here this will be augmented/modified by maximizing the
        # score in the hand less the score in the crib.
         
        # Get the cards in the hand
        cards = get_hand_callback()
        
        # Generate permutations of 4-card hands / 2-card crib contributions, and score them
        h = Hand().add_cards(cards)
        priority_list = self.permute_and_score_dealt_hand(h)
        
        # Sort priority_list by descending (guaranteed_hand_score + guaranteed_crib_score)
        sorted_list = sorted(priority_list, key = lambda option: (option.hand_score - option.crib_score), reverse = True)

        # TODO: Could now filter sorted_list for all options that have the same (hand_score - crib_score) as the first item on the sorted list,
        # and output a debug message, probably including str(sorted_list[i] for each such option), to start to build statistics on how
        # often this prioritization scheme is ambiguous. This would be evidence of potential value in further work on prioritization, such as
        # incorporating expected probability scores.

        # Now transfer to the crib the crib cards for the highest priority option
        for c in sorted_list[0].crib:
            i = cards.index(c)
            xfer_to_crib_callback(i)
            # Refresh cards, since we've pulled a card out of the hand, and thus changed the indexing
            cards = get_hand_callback()
 
        return None

class InteractiveCribbagePlayStrategy(CribbagePlayStrategy):
    """
    Implementation of CribbagePlayStrategy where a human player is asked to decide what to do.
    """
    
    def form_crib(self, xfer_to_crib_callback, get_hand_callback, play_recorder_callback=None):
        """
        Ask human player which cards from the hand to place in the crib.
        :parameter xfer_to_crib_callback: Bound method used to transfer cards from hand to crib, e.g., CribbageDeal.xfer_player_card_to_crib
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :parameter play_recorder_callback: Bound method used to record user choices for cards to lay off in the crib
        :return: None
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(xfer_to_crib_callback))
        assert(callable(get_hand_callback))
        if play_recorder_callback: assert(callable(play_recorder_callback))

        # We're interactive here, so ask the user which cards from their hand they want in the crib

        # Build a query for the user to obtain a decision on first card to put in the crib
        query_preface = 'What is the first card you wish to place in the crib?'
        query_dic = {}
        position = 0
        for card in get_hand_callback():
            query_dic[str(position)] = str(card)
            position += 1
        response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
        xfer_to_crib_callback(int(response))
        if play_recorder_callback: play_recorder_callback(f"{response}\\n")
        
        # Build a query for the user to obtain a decision on second card to put in the crib
        query_preface = 'What is the second card you wish to place in the crib?'
        query_dic = {}
        position = 0
        for card in get_hand_callback():
            query_dic[str(position)] = str(card)
            position += 1
        response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
        xfer_to_crib_callback(int(response))
        if play_recorder_callback: play_recorder_callback(f"{response}\\n")

        return None

    # TODO: This isn't currently being used for anything. Rather than remove it entirely, keep it for now, but consider repurposing it
    # as a utility called from follow(...) when the play pile is empty. That would encapsulate a strategy specific to leading, but the card would
    # get played in the context of the follow(...) logic.
    def lead(self, play_card_callback, get_hand_callback):
        """
        Ask human player which card to Lead (play) in a go round.
        :parameter play_card_callback: Bound method used to play a card from hand, e.g., CribbageDeal.play_card_for_player
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :return: The pips count of the card played, int 
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(play_card_callback))
        assert(callable(get_hand_callback))
        
        # We're interactive here, so ask the user which card from their hand they want to lead

        # Build a query for the user to obtain a decision on card to lead
        query_preface = 'What card do you wish to lead?'
        query_dic = {}
        position = 0
        for card in get_hand_callback():
            query_dic[str(position)] = str(card)
            position += 1
        response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
        count = play_card_callback(int(response))
        
        return count

    def follow(self, go_count, play_card_callback, get_hand_callback, get_play_pile_callback, play_recorder_callback=None):
        """
        Ask human player which card to follow (play) in a go round.
        :parameter go_count: The current cumulative count of the go round before the follow, int
        :parameter play_card_callback: Bound method used to play a card from hand, e.g., CribbageDeal.play_card_for_player
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :parameter get_play_pile_callback: Bound method used to obtain the pile of played cards, e.g., CribbageDeal.get_player_hand
        :parameter play_recorder_callback: Bound method used to record user choices for cards to lay off in the crib
        :return: (The pips count of the card played as int, Go declared as boolean), tuple
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(play_card_callback))
        assert(callable(get_hand_callback))
        assert(callable(get_play_pile_callback))
        if play_recorder_callback: assert(callable(play_recorder_callback))
        
        # We're interactive here, so ask the user which card from their hand they want to play

        # Generate list of which if any cards can still be played, which will use "lightly" later.
        # "Lightly" meaning that we will not restrict the list of cards available to choose from, though we will validate that any
        # choice by the user is a valid play.
        playable = [c for c in get_hand_callback() if c.count_card() <= (31 - go_count)]

        declare_go = False
        valid_choice = False
        
        # Build a query for the user to obtain a decision on card to play
        query_preface = 'Current play count is ' + str(go_count) + '. What card do you wish to play?'
        query_dic = {}
        position = 0
        for card in get_hand_callback():
            query_dic[str(position)] = str(card)
            position += 1
        if len(playable) == 0:
            # User has no playable cards, so add 'Go' to the list of choices
            query_dic['g'] = 'Go'
        response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
        
        while not valid_choice:

            if response == 'g':
                valid_choice = True
                declare_go = True
                count = 0
            else:
                # Determine if the chosen card can be played without go_count exceeding 31.
                chosen_card_count = get_hand_callback()[int(response)].count_card()
                if (go_count + chosen_card_count) <= 31:
                    # Card can be played
                    count = play_card_callback(int(response))
                    valid_choice = True
                else:
                    # Card cannot be played
                    # Inform the user and ask for another card choice
                    query_preface = 'Chosen card would cause cumulative play count to exceed 31. What card do you wish to play?'
                    query_dic = {}
                    position = 0
                    for card in get_hand_callback():
                        query_dic[str(position)] = str(card)
                        position += 1
                    if len(playable) == 0:
                        # User has no playable cards, so add 'Go' to the list of choices
                        query_dic['g'] = 'Go'
                    response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
                    
        if play_recorder_callback: play_recorder_callback(f"{response}\\n")
        
        return (count, declare_go)

    def go(self, go_count, play_card_callback, get_hand_callback, get_play_pile_callback, score_play_callback, peg_callback,
           play_recorder_callback=None):
        """
        Ask human player which card(s) if any to play in a go round after their opponent has declared go.
        :parameter go_count: The current cumulative count of the go round that caused opponent to declare go, int
        :parameter play_card_callback: Bound method used to play a card from hand, e.g., CribbageDeal.play_card_for_player
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :parameter get_play_pile_callback: Bound method used to obtain the pile of played cards, e.g., CribbageDeal.get_player_hand
        :parameter score_play_callback: Bound method used to determine any scoring while go is being played out, e.g., CribbageDeal.determine_score_playing
        :parameter peg_callback: Bound method used to determine any scoring while go is being played out, e.g., CribbageDeal.peg_for_player
        :parameter play_recorder_callback: Bound method used to record user choices for cards to lay off in the crib
        :return: The sum of pips count of any cards played, int
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(play_card_callback))
        assert(callable(get_hand_callback))
        assert(callable(score_play_callback))
        assert(callable(peg_callback))
        if play_recorder_callback: assert(callable(play_recorder_callback))
        
        play_count = go_count
        
        # Generate list of which if any cards can still be played
        playable = [c for c in get_hand_callback() if c.count_card() <= (31 - play_count)]

        while (len(playable) > 0):
        
            # We're interactive here, so ask the user which card from playable they want to play

            # Build a query for the user to obtain a decision on card to play
            query_preface = 'Opponent has declared GO. Current play count is ' + str(play_count) + '. What card do you wish to play?'
            query_dic = {}
            position = 0
            for card in playable:
                query_dic[str(position)] = str(card)
                position += 1
            response = UserResponseCollector_query_user(BlackJackQueryType.MENU, query_preface, query_dic)
            if play_recorder_callback: play_recorder_callback(f"{response}\\n")

            # Play card
            play_card_callback(int(response))
            play_count += playable[int(response)].count_card()

            # Score any pairs or runs due to the played card
            score_count = score_play_callback(get_play_pile_callback())
            peg_callback(score_count)

            # Generate list of which if any cards can still be played
            playable = [c for c in get_hand_callback() if c.count_card() <= (31 - play_count)]
        
        return (play_count - go_count)

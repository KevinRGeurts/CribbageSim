# Standard imports

# Local imports
from UserResponseCollector import UserResponseCollector_query_user, BlackJackQueryType


# TODO: If decide to convert lead(...) to utility called by follow(...), then lead(...) may not belong in the list of functions that
# children MUST implement, meaning that the doc string should be updated.
class CribbagePlayStrategy:
    """
    Following a Strategy design pattern, this is the interface class for all cribbage hand playing strategies.
    Each child must by convention and necessity implement these methods:
        form_crib(...) - For selecting two cards from the dealt six to be placed in the crib 
        lead(...) - For selecting the first card to play after a round of play has finished after a "go"
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

    def follow(self, go_count, play_card_callback, get_hand_callback, play_recorder_callback=None):
        """
        This is an abstract method that MUST be implemented by children. If called, it will raise NotImplementedError
        Called to decide which card to follow (play) in a go round.
        :parameter go_count: The current cumulative count of the go round before the follow, int
        :parameter play_card_callback: Bound method used to play a card from hand, e.g., CribbageDeal.play_card_for_player
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :parameter play_recorder_callback: Bound method used to record user choices for cards to lay off in the crib
        :return: (The pips count of the card played as int, Go declared as boolean), tuple
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(play_card_callback))
        assert(callable(get_hand_callback))
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


class DummyCribbagePlayStrategy(CribbagePlayStrategy):
    """
    An very simple and very dumb implementation of CribbagePlayStrategy, intended only to be used during initial development of the simulator,
    so that overall algorithmic flow of playing can be worked out before working about playing well.
    """
    
    def form_crib(self, xfer_to_crib_callback, get_hand_callback):
        """
        Forms the crib by providing the first two cards in the hand, regardless of what they are.
        :parameter xfer_to_crib_callback: Bound method used to transfer cards from hand to crib, e.g., CribbageDeal.xfer_player_card_to_crib
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :return: None
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(xfer_to_crib_callback))
        assert(callable(get_hand_callback))

        # This is a dumb former of the crib, so just dump the first two cards in the hand
        xfer_to_crib_callback(0)
        xfer_to_crib_callback(0)

        return None
    
    # TODO: This isn't currently being used for anything. Rather than remove it entirely, keep it for now, but consider repurposing it
    # as a utility called from follow(...) when the play pile is empty. That would encapsulate a strategy specific to leading, but the card would
    # get played in the context of the follow(...) logic.
    def lead(self, play_card_callback, get_hand_callback):
        """
        Leads (plays) the first remaining card in the hand, regardless of what it is.
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

    def follow(self, go_count, play_card_callback, get_hand_callback):
        """
        Follows (plays) by playing the first remaining card in the hand, regardless of what it is.
        :parameter go_count: The current cumulative count of the go round before the follow, int
        :parameter play_card_callback: Bound method used to play a card from hand, e.g., CribbageDeal.play_card_for_player
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :return: (The pips count of the card played as int, Go declared as boolean), tuple
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(play_card_callback))
        assert(callable(get_hand_callback))
        
        # Deteremine if any card can be played without go_count exceeding 31. If not, then return (0, True)
        
        # This is a dumb player, always playing the first card left in the hand
        count = play_card_callback(0)
        return (count, False)

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

    def follow(self, go_count, play_card_callback, get_hand_callback, play_recorder_callback=None):
        """
        Ask human player which card to follow (play) in a go round.
        :parameter go_count: The current cumulative count of the go round before the follow, int
        :parameter play_card_callback: Bound method used to play a card from hand, e.g., CribbageDeal.play_card_for_player
        :parameter get_hand_callback: Bound method used to obtain cards in hand, e.g., CribbageDeal.get_player_hand
        :parameter play_recorder_callback: Bound method used to record user choices for cards to lay off in the crib
        :return: (The pips count of the card played as int, Go declared as boolean), tuple
        """
        # Sanity check the arguments to make sure they are callable. This does not guarantee they are bound methods, e.g., a class is callable
        # for construction. But it is better than nothing.
        assert(callable(play_card_callback))
        assert(callable(get_hand_callback))
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

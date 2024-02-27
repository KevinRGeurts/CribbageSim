# Local imports
from hand import Hand

class CribbageComboInfo(object):
    """
    A class with all public members, containing information about a particular scoring combination's presence in a cribbage hand.
    """
    
    def __init__(self):
        """
        combo_name: The name of the cribbage scoring combination, string
        number_instances: How many times does the scoring combination appear in the cribbage hand?, int
        score: The total number of points due to all instances of teh scoring combination in the cribbage hand, int
        instance_list: List of lists of Card(s) of the instances of the scoring combination in the cribbage hand, list
        """
        self.combo_name = 'none'
        self.number_instances = 0
        self.score = 0
        self.instance_list = []
        
    def __str__(self):
        s = ''
        s += self.combo_name + ': ' + str(self.number_instances) + ' for ' + str(self.score) + ': '
        for combo in self.instance_list:
            for card in combo:
                s += str(card) + ' '
            s += ', '
        return s


class CribbageCombination(object):
    """
    Following a Strategy design pattern, this is the interface class for all cribbage card scoring combinations.
    Each child must by convention and necessity implement these methods:
        score(...) - Searches a Hand and for the existence of one or more instances of the combination in the Hand.
            Returns information on the istances found and the score resulting from those instances.
    The concept for using this class is that a client could hold a list of instances of children of this class, one for each scoring combination,
    and the client would iterate through that list, calling score(...) method for each one, to tally up the score of a hand.
    """
    
    def __init__(self):
        """
        Construct the base class for a cribbage scoring combination.
        _score_per_combo: The points scored for one instance of a combo in a hand, int
        """
        self._combo_name = 'none'
        self._score_per_combo = 0
        
    def get_name(self):
        return self._combo_name
        

class PairCombination(CribbageCombination):
    """
    Intended to search for, find, and score pairs in a cribbage hand.
    """
    
    def __init__(self):
        """
        Construct the class for pair scoring combination in cribbage hand.
        """
        self._combo_name = 'pair'
        self._score_per_combo = 2
        
    def score(self, hand = Hand()):
        """
        Search hand for all pairs, tally up the score, and return a CribbageComboInfo object.
        :parameter hand: The hand to search for pairs, Hand object
        :return: CribbageComboInfo object with information about the pairs in the hand, CribbageComboInfo object
        """
        
        info = CribbageComboInfo()
        info.combo_name = self._combo_name
        
        cards = hand.get_cards()
        
        # Create a list of all permutations of two cards in the hand.
        permutations = []
        for i in range(len(cards)):
                for j in range(i+1,len(cards)):
                    permutations.append([cards[i], cards[j]])
                    
        # Iterate through the permutations and determine how many of them are pairs
        for p in permutations:
            if p[0].get_pips() == p[1].get_pips():
                info.number_instances += 1
                info.instance_list.append(p)
                
        # Set the score in the info object
        info.score = info.number_instances * self._score_per_combo      
        
        return info





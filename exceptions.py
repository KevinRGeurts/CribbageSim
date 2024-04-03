
class CribbageError(Exception):
    """
    Base exception class for all custom excpetions specific to CribbageSimulator project.
    """
    pass


class CribbageGameOverError(CribbageError):
    """
    Custom exception to be raised when pegging the CribbageBoard results in one player reaching a score of 121, and thus ending the game.
    Arguments expected in **kwargs:
        deal_info: A CribbageDealInfo object containing information up to the point where the pegging was initiated.
        go_play_score: An integer score for playing a scoring combo within a CribbagePlayStrategy.go(...), which if that score
            ends the game, needs to be injected here so that it can be incorporated into deal_info by CribbageDeal.play(...).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.deal_info = kwargs.get('deal_info')
        self.go_play_score = kwargs.get('go_play_score')
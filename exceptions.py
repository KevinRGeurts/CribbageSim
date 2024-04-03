
class CribbageError(Exception):
    """
    Base exception class for all custom excpetions specific to CribbageSimulator project.
    """
    pass


class CribbageGameOverError(CribbageError):
    """
    Custom exception to be raised when pegging the CribbageBoard results in one player reaching a score of 121, and thus ending the game.
    Arguments expected in **kwargs:
        deal_info=: A CribbageDealInfo object containing information up to the point where the pegging was initiated.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.deal_info = kwargs.get('deal_info')
        self.go_play_score = kwargs.get('go_play_score')
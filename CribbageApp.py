# standard imports
from ast import Lambda
import tkinter as tk
from tkinter import ttk

# local imports
from CribbageGame import CribbageGame
from CribbagePlayStrategy import InteractiveCribbagePlayStrategy, HoyleishDealerCribbagePlayStrategy, HoyleishPlayerCribbagePlayStrategy


class CribbageApp(ttk.Frame):
    """
    Class represent a Cribbage application built using tkinter.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.grid(column=0, row=0, sticky='NWES')
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        # The CribbageGame object used to play the cribbage game
        self._game = CribbageGame(player_strategy1 = InteractiveCribbagePlayStrategy(), player_strategy2 = HoyleishPlayerCribbagePlayStrategy(),
                                  dealer_strategy2 = HoyleishDealerCribbagePlayStrategy())
        
        # ----- Widgets

        self._board_widget = CribbageBoardWidget(self)
        self._board_widget.grid(column=1, row=1, rowspan=4, sticky='WE')

        self._starter_widget = CribbageStarterCardWidget(self)
        self._starter_widget.grid(column=2, row=1, sticky='WE')

        self._crib_widget = CribbageCribWidget(self)
        self._crib_widget.grid(column=3, row=1, sticky='WE')
        
        self._player_hand_widget = CribbagePlayerHandWidget(self)
        self._player_hand_widget.grid(column=2, row=2, columnspan=2, sticky='WE')

        self._play_pile_widget = CribbagePlayPileWidget(self)
        self._play_pile_widget.grid(column=2, row=3, columnspan=2, sticky='WE')

        
        self._info_widget = CribbagePlayShowInfoWidget(self)
        self._info_widget.grid(column=2, row=4, columnspan=2, sticky='WE')
        

        
        # # Label showing game score
        # self._lbl_game_score = ttk.Label(self, text=f"{self._game.get_player1_name()}={self._game.get_player_scores()[0]}, {self._game.get_player2_name()}={self._game.get_player_scores()[1]}")
        # self._lbl_game_score.grid(column=1, row=1, sticky='WE')
        
        # # Label showing player1 hand
        # self._lbl_player1_hand = ttk.Label(self)
        # self._lbl_player1_hand.grid(column=1, row=2, sticky='WE')
        # # Applicaton variable for player1 hand
        # self._player1_hand = tk.StringVar()
        # # Set it to some value.
        # self._player1_hand.set(f"{self._game.get_player1_name()} hand: {'KC JD 5S QH'}")
        # # Tell the label widget to watch this variable.
        # self._lbl_player1_hand["textvariable"] = self._player1_hand
        
        
        # # Temporary Quit button
        # self._btn_quit = ttk.Button(self, text='Quit', command=parent.destroy)
        # self._btn_quit.grid(column=2, row=3, sticky='WE')
        
class CribbagePlayerHandWidget(ttk.Labelframe):
    """
    Class represents a tkinter label frame, the wdiget contents of which will represent a player's hand visually in the application.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent, text='Player 1 Hand - Click the card you wish to play')
        # TODO: Make the text for the label frame an application variable, so it can be used to instruct the user of when to form crib and when
        # to play cards.
        
        # List of buttons representing cards in the hand
        self._btns_cards = []
        self._btns_cards.append(ttk.Button(self, text='QH', command=self.OnCardButtonClick))
        self._btns_cards[0].grid(column=1, row=1)
        self._btns_cards.append(ttk.Button(self, text='6C', command=self.OnCardButtonClick))
        self._btns_cards[1].grid(column=2, row=1)
        self._btns_cards.append(ttk.Button(self, text='--', command=self.OnCardButtonClick))
        self._btns_cards[2].grid(column=3, row=1)
        self._btns_cards.append(ttk.Button(self, text='--', command=self.OnCardButtonClick))
        self._btns_cards[3].grid(column=4, row=1)
        self._btns_cards.append(ttk.Button(self, text='--', command=self.OnCardButtonClick))
        self._btns_cards[4].grid(column=5, row=1)
        self._btns_cards.append(ttk.Button(self, text='--', command=self.OnCardButtonClick))
        self._btns_cards[5].grid(column=6, row=1)

        self._btn_undo = ttk.Button(self, text='Undo', command=self.OnUndoButtonClick)
        self._btn_undo.grid(column=8, row=1)

    def OnCardButtonClick(self):
        # Inform the mediator object
        pass

    def OnUndoButtonClick(self):
        # Inform the mediator object
        pass

class CribbageStarterCardWidget(ttk.Labelframe):
    """
    Class represents a tkinter label frame, the wdiget contents of which will represent the starter card visually in the application.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent, text='Starter')
        
        self._btn_starter = ttk.Button(self, text='9H')
        self._btn_starter.grid(column=1, row=1)

class CribbageCribWidget(ttk.Labelframe):
    """
    Class represents a tkinter label frame, the wdiget contents of which will represent the crib in the application.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent, text='Crib')
        
        # List of buttons representing cards in the crib
        self._btns_cards = []
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[0].grid(column=1, row=1)
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[1].grid(column=2, row=1)
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[2].grid(column=3, row=1)
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[3].grid(column=4, row=1)


class CribbagePlayPileWidget(ttk.Labelframe):
    """
    Class represents a tkinter label frame, the wdiget contents of which will represent the pile of played cards visually in the application.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent, text='Play Pile')
        
        # List of buttons representing cards in the play pile
        self._btns_cards = []
        self._btns_cards.append(ttk.Button(self, text='KH'))
        self._btns_cards[0].grid(column=1, row=1)
        self._btns_cards.append(ttk.Button(self, text='5S'))
        self._btns_cards[1].grid(column=2, row=1)
        self._btns_cards.append(ttk.Button(self, text='5D'))
        self._btns_cards[2].grid(column=3, row=1)
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[3].grid(column=4, row=1)
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[4].grid(column=5, row=1)
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[5].grid(column=6, row=1)
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[6].grid(column=7, row=1)
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[7].grid(column=8, row=1)
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[8].grid(column=9, row=1)


class CribbageBoardWidget(ttk.Labelframe):
    """
    Class represents a tkinter label frame, the wdiget contents of which will represent the cribbage board visually in the application.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent, text='Cribbage Board')
        
        self._player1_track = ttk.Labelframe(self, text='Player 1 - Dealer')
        self._player1_track.grid(column=1, row=1)

        # Create a list of checkbuttons with indices 0-61 that represent visually the pegging locations along the player 1 track on the board
        self._player1_holes = []
        for i in range(0,31):
            # TODO: Disable the user clicking the buttons
            # Assign a list of application variables
            self._player1_holes.append(ttk.Checkbutton(self._player1_track))
            self._player1_holes[i].grid(column=1, row=(31-i))
        for i in range(31,62):
            # TODO: Disable the user clicking the buttons
            # Assign a list of application variables
            self._player1_holes.append(ttk.Checkbutton(self._player1_track))
            self._player1_holes[i].grid(column=2, row=(i-30))

        self._player2_track = ttk.Labelframe(self, text='Player 2')
        self._player2_track.grid(column=2, row=1)

        # Create a list of checkbuttons with indices 0-61 that represent visually the pegging locations along the player 2 track on the board
        self._player2_holes = []
        for i in range(0,31):
            # TODO: Disable the user clicking the buttons
            # Assign a list of application variables
            self._player2_holes.append(ttk.Checkbutton(self._player2_track))
            self._player2_holes[i].grid(column=1, row=(31-i))
        for i in range(31,62):
            # TODO: Disable the user clicking the buttons
            # Assign a list of application variables
            self._player2_holes.append(ttk.Checkbutton(self._player2_track))
            self._player2_holes[i].grid(column=2, row=(i-30))


class CribbagePlayShowInfoWidget(ttk.Labelframe):
    """
    Class represents a tkinter label frame, the wdiget contents of which will display text information to the user about
    scoring during play and during show.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent, text='Play / Show Info')
        
        self._txt_info =  tk.Text(self, width=40, height=10)
        self._txt_info.grid(column=1, row=1)
        self._txt_info.insert('end','Player 2 scored 15 for 2: KH 5S\nPlayer 1 scored pair for 2; 5S 5D')

# standard imports
from ast import Lambda
import tkinter as tk
from tkinter import ttk
from functools import partial

# local imports
from CribbageGame import CribbageGame
from CribbagePlayStrategy import InteractiveCribbagePlayStrategy, HoyleishDealerCribbagePlayStrategy, HoyleishPlayerCribbagePlayStrategy


class CribbageApp(ttk.Frame):
    """
    Class represent a Cribbage application built using tkinter.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.grid(column=0, row=0, sticky='NWES') # Grid-0 in Documentation\UI_WireFrame.pptx
        # Weights control the relative "stretch" of each column and row as the frame is resized
        parent.columnconfigure(0, weight=1) # Grid-0 in Documentation\UI_WireFrame.pptx
        parent.rowconfigure(0, weight=1) # Grid-0 in Documentation\UI_WireFrame.pptx
        
        # The CribbageGame object used to play the cribbage game
        self._game = CribbageGame(player_strategy1 = InteractiveCribbagePlayStrategy(), player_strategy2 = HoyleishPlayerCribbagePlayStrategy(),
                                  dealer_strategy2 = HoyleishDealerCribbagePlayStrategy())
        
        # ----- Widgets

        self._board_widget = CribbageBoardWidget(self, self._game.get_player1_name(), self._game.get_player2_name())
        self._board_widget.grid(column=0, row=0, rowspan=4, sticky='NWES') # Grid-1 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(0, weight=1) # Grid-1 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(0, weight=1) # Grid-1 in Documentation\UI_WireFrame.pptx

        self._starter_widget = CribbageStarterCardWidget(self)
        self._starter_widget.grid(column=1, row=0, sticky='NWES') # Grid-1 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(1, weight=1) # Grid-1 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(0, weight=1) # Grid-1 in Documentation\UI_WireFrame.pptx

        self._crib_widget = CribbageCribWidget(self)
        self._crib_widget.grid(column=2, row=0, sticky='NWES') # Grid-1 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(2, weight=1) # Grid-1 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(0, weight=1) # Grid-1 in Documentation\UI_WireFrame.pptx
        
        self._player_hand_widget = CribbagePlayerHandWidget(self, self._game.get_player1_name())
        self._player_hand_widget.grid(column=1, row=1, columnspan=2, sticky='NWES') # Grid-1 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(1, weight=1) # Grid-1 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(1, weight=1) # Grid-1 in Documentation\UI_WireFrame.pptx

        self._play_pile_widget = CribbagePlayPileWidget(self)
        self._play_pile_widget.grid(column=1, row=2, columnspan=2, sticky='NWES') # Grid-1 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(1, weight=1) # Grid-1 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(2, weight=1) # Grid-1 in Documentation\UI_WireFrame.pptx
        
        self._info_widget = CribbagePlayShowInfoWidget(self)
        self._info_widget.grid(column=1, row=3, columnspan=2, sticky='NWES') # Grid-1 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(1, weight=1) # Grid-1 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(3, weight=1) # Grid-1 in Documentation\UI_WireFrame.pptx       

        
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
    def __init__(self, parent, name1='') -> None:
        """
        :parameter parent: tkinter widget that is the parent of this widget
        :parameter name1: Name of player 1 , string
        """
        super().__init__(parent, text=f"{name1} Hand - Click the card you wish to play")
        # TODO: Make the text for the label frame an application variable, so it can be used to instruct the user of when to form crib and when
        # to play cards.
        
        # List of buttons representing cards in the hand
        self._btns_cards = []
        
        # Note: partial is used in order to be able to pass along a button index to the command function, which otherwise takes no arguments
        # TODO: Size the buttons with ['heigth'], ['width'] in text lines and characters
        # TODO: Assign TextVar to buttons for managing their text label
        # See: (https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter)
        self._btns_cards.append(tk.Button(self, text='QH', command=partial(self.OnCardButtonClick, 0)))
        self._btns_cards[0].grid(column=0, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

        self._btns_cards.append(tk.Button(self, text='6C', command=partial(self.OnCardButtonClick, 1)))
        self._btns_cards[1].grid(column=1, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(1, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

        self._btns_cards.append(tk.Button(self, text='--', command=partial(self.OnCardButtonClick, 1)))
        self._btns_cards[2].grid(column=2, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(2, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self._btns_cards[2]['state']=tk.DISABLED

        self._btns_cards.append(tk.Button(self, text='--', command=partial(self.OnCardButtonClick, 1)))
        self._btns_cards[3].grid(column=3, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self._btns_cards[3]['state']=tk.DISABLED
        self.columnconfigure(3, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

        self._btns_cards.append(tk.Button(self, text='--', command=partial(self.OnCardButtonClick, 1)))
        self._btns_cards[4].grid(column=4, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(4, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self._btns_cards[4]['state']=tk.DISABLED

        self._btns_cards.append(tk.Button(self, text='--', command=partial(self.OnCardButtonClick, 1)))
        self._btns_cards[5].grid(column=5, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(5, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self._btns_cards[5]['state']=tk.DISABLED

        for b in self._btns_cards:
             b['height']=8
             b['width']=10
             b['relief']=tk.RIDGE

        self._btn_undo = ttk.Button(self, text='Undo', command=self.OnUndoButtonClick)
        self._btn_undo.grid(column=6, row=0, sticky='E') # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(6, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

    def OnCardButtonClick(self, index):
        # Inform the mediator object which index button was pressed
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
        self._btn_starter.grid(column=0, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

class CribbageCribWidget(ttk.Labelframe):
    """
    Class represents a tkinter label frame, the wdiget contents of which will represent the crib in the application.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent, text='Crib')
        
        # List of buttons representing cards in the crib
        self._btns_cards = []
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[0].grid(column=0, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[1].grid(column=1, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(1, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[2].grid(column=2, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(2, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        
        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[3].grid(column=3, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(3, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx


class CribbagePlayPileWidget(ttk.Labelframe):
    """
    Class represents a tkinter label frame, the wdiget contents of which will represent the pile of played cards visually in the application.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent, text='Play Pile')
        
        # List of buttons representing cards in the play pile
        self._btns_cards = []
        
        self._btns_cards.append(ttk.Button(self, text='KH'))
        self._btns_cards[0].grid(column=0, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

        self._btns_cards.append(ttk.Button(self, text='5S'))
        self._btns_cards[1].grid(column=1, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(1, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

        self._btns_cards.append(ttk.Button(self, text='5D'))
        self._btns_cards[2].grid(column=2, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(2, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[3].grid(column=3, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(3, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[4].grid(column=4, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(4, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[5].grid(column=5, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(5, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[6].grid(column=6, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(6, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[7].grid(column=7, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(7, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

        self._btns_cards.append(ttk.Button(self, text='--'))
        self._btns_cards[8].grid(column=8, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(8, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx


class CribbageBoardWidget(ttk.Labelframe):
    """
    Class represents a tkinter label frame, the wdiget contents of which will represent the cribbage board visually in the application.
    """
    def __init__(self, parent, name1='', name2='') -> None:
        """
        :parameter parent: tkinter widget that is the parent of this widget
        :parameter name1: Name of player 1 , string
        :parameter name2: Name of player 2 , string
        """
        super().__init__(parent, text='Cribbage Board')
        
        self._player1_track = ttk.Labelframe(self, text=f"{name1} - Dealer")
        self._player1_track.grid(column=0, row=0, sticky='NWES') # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

        # Create a list of checkbuttons with indices 0-61 that represent visually the pegging locations along the player 1 track on the board
        self._player1_holes = []
        # Simultaneously, create a list of IntVar control variables that track the state of each checkbutton
        self._player1_pegs = []
        self._player1_track.columnconfigure(0, weight=1) # Grid-3 in Documentation\UI_WireFrame.pptx
        self._player1_track.columnconfigure(1, weight=1) # Grid-3 in Documentation\UI_WireFrame.pptx
        for i in range(0,31):
            self._player1_holes.append(ttk.Checkbutton(self._player1_track, text=str(i)))
            self._player1_holes[i].grid(column=0, row=(31-i)) # Grid-3 in Documentation\UI_WireFrame.pptx
            self._player1_track.rowconfigure((31-i), weight=1) # Grid-3 in Documentation\UI_WireFrame.pptx
            self._player1_holes[i]['state']=tk.DISABLED
            # Create and assign control variables
            self._player1_pegs.append(tk.IntVar())
            self._player1_holes[i]['variable'] = self._player1_pegs[i]
        for i in range(31,62):
            self._player1_holes.append(ttk.Checkbutton(self._player1_track, text=str(i)))
            self._player1_holes[i].grid(column=1, row=(i-30)) # Grid-3 in Documentation\UI_WireFrame.pptx
            self._player1_track.rowconfigure((i-30), weight=1) # Grid-3 in Documentation\UI_WireFrame.pptx
            self._player1_holes[i]['state']=tk.DISABLED
            # Create and assign control variables
            self._player1_pegs.append(tk.IntVar())
            self._player1_holes[i]['variable'] = self._player1_pegs[i]

        self._player2_track = ttk.Labelframe(self, text=f"{name2}")
        self._player2_track.grid(column=1, row=0, sticky='NWES') # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(1, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

        # Create a list of checkbuttons with indices 0-61 that represent visually the pegging locations along the player 2 track on the board
        self._player2_holes = []
        # Simultaneously, create a list of IntVar control variables that track the state of each checkbutton
        self._player2_pegs = []
        self._player2_track.columnconfigure(0, weight=1) # Grid-3 in Documentation\UI_WireFrame.pptx
        self._player2_track.columnconfigure(1, weight=1) # Grid-3 in Documentation\UI_WireFrame.pptx
        for i in range(0,31):
            self._player2_holes.append(ttk.Checkbutton(self._player2_track, text=str(i)))
            self._player2_holes[i].grid(column=0, row=(31-i)) # Grid-3 in Documentation\UI_WireFrame.pptx
            self._player2_track.rowconfigure((31-i), weight=1) # Grid-3 in Documentation\UI_WireFrame.pptx
            self._player2_holes[i]['state']=tk.DISABLED
            # Create and assign control variables
            self._player2_pegs.append(tk.IntVar())
            self._player2_holes[i]['variable'] = self._player1_pegs[i]
        for i in range(31,62):
            self._player2_holes.append(ttk.Checkbutton(self._player2_track, text=str(i)))
            self._player2_holes[i].grid(column=1, row=(i-30)) # Grid-3 in Documentation\UI_WireFrame.pptx
            self._player2_track.rowconfigure((i-30), weight=1) # Grid-3 in Documentation\UI_WireFrame.pptx
            self._player2_holes[i]['state']=tk.DISABLED
            # Create and assign control variables
            self._player2_pegs.append(tk.IntVar())
            self._player2_holes[i]['variable'] = self._player1_pegs[i]
        # Initialize so that both player's pegs start in pre-game positions (0 and 61)
        self.set_pegs_player1()
        self.set_pegs_player2()

    def set_pegs_player1(self, lead=0, trail=61):
        """
        Set the locations of the pegs on the board for player 1. By default places pegs in starting location.
        :parameter lead: Hole location of leading peg, int
        :parameter trail: Hole location of trailing peg, int
        :return None:
        """
        self._player1_pegs[lead].set(1)
        self._player1_pegs[trail].set(1)
        return None

    def set_pegs_player2(self, lead=0, trail=61):
        """
        Set the locations of the pegs on the board for player 2. By default places pegs in starting location.
        :parameter lead: Hole location of leading peg, int
        :parameter trail: Hole location of trailing peg, int
        :return None:
        """
        self._player2_pegs[lead].set(1)
        self._player2_pegs[trail].set(1)
        return None

class CribbagePlayShowInfoWidget(ttk.Labelframe):
    """
    Class represents a tkinter label frame, the wdiget contents of which will display text information to the user about
    scoring during play and during show.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent, text='Play / Show Info')
        
        self._txt_info =  tk.Text(self, width=40, height=10)
        self._txt_info.grid(column=0, row=0, sticky='NWSE') # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self._txt_info.insert('end','Player 2 scored 15 for 2: KH 5S\nPlayer 1 scored pair for 2; 5S 5D')

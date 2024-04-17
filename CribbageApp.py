# standard imports
from ast import Lambda
from quopri import decodestring
import tkinter as tk
from tkinter import ttk
from functools import partial
from threading import Thread
from time import sleep
from queue import Queue

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
        
        # Event queue (FIFO) for communicating with the thread running the Cribbage Game
        self._game_event_queue=Queue(10)
       
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
        
    def CribbageGameOutputEventHandler(self, event):
        """
        Used with StubGame object as PoC of ability for tkinter UI to respond to events where CribbageGame is trying to provide output for it
        to display. Actual implemetation might want this inside of a "controler" or "mediator" rather than in the App?
        """
        # Retrieve an item from the game event queue
        item = self._game_event_queue.get(timeout = 1)
        # Just for testing, we will assume the item is a tuple of leading and trailing peg locations for player 1
        self._board_widget.set_pegs_player1(item[0], item[1])
        # self._info_widget.insert_end(item)

    def CribbageGameQueryEventHandler(self, event):
        """
        Used with StubGame object as PoC of ability for tkinter UI to respond to events where CribbageGame is trying to request input from the user
        from it. Actual implemetation might want this inside of a "controler" or "mediator" rather than in the App?
        """
        # Retrieve an item from the game event queue to determine what type of information we need from the user
        item = self._game_event_queue.get(timeout = 1)
        # For test purposes, we are assuming we are being asked to have the user pick a card to play from the hand
        self._info_widget.insert_end(f"\n{item[0]} : {item[1]}\n")
        self._player_hand_widget._lbls_cards[1].set(item[1])
        # Send message to the game's thread to alert it to check the queue?
        # May not be necessary, may make more sense for the game to wait in a tight loop for an item to appear in the queue,
        # after it has posted it's request for a response to a query to the App.
        # Here for testing, we are actually waiting for the user to click card index = 1 in the player hand, and that handler will
        # insert the resonse in the CribbageGame response queue
        
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
        # List of StringVar control variables for the card labels
        self._lbls_cards = []
        
        # Note: partial is used in order to be able to pass along a button index to the command function, which otherwise takes no arguments
        # TODO: Size the buttons with ['heigth'], ['width'] in text lines and characters
        # TODO: Assign TextVar to buttons for managing their text label
        # See: (https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter)
        self._btns_cards.append(tk.Button(self, command=partial(self.OnCardButtonClick, 0)))
        self._btns_cards[0].grid(column=0, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.rowconfigure(0, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self._lbls_cards.append(tk.StringVar())
        self._lbls_cards[0].set('QH')
        self._btns_cards[0]['textvariable']=self._lbls_cards[0]

        self._btns_cards.append(tk.Button(self, command=partial(self.OnCardButtonClick, 1)))
        self._btns_cards[1].grid(column=1, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(1, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self._lbls_cards.append(tk.StringVar())
        self._lbls_cards[1].set('6C')
        self._btns_cards[1]['textvariable']=self._lbls_cards[1]

        self._btns_cards.append(tk.Button(self, command=partial(self.OnCardButtonClick, 1)))
        self._btns_cards[2].grid(column=2, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(2, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self._btns_cards[2]['state']=tk.DISABLED
        self._lbls_cards.append(tk.StringVar())
        self._lbls_cards[2].set('--')
        self._btns_cards[2]['textvariable']=self._lbls_cards[2]

        self._btns_cards.append(tk.Button(self, command=partial(self.OnCardButtonClick, 1)))
        self._btns_cards[3].grid(column=3, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self._btns_cards[3]['state']=tk.DISABLED
        self.columnconfigure(3, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self._lbls_cards.append(tk.StringVar())
        self._lbls_cards[3].set('--')
        self._btns_cards[3]['textvariable']=self._lbls_cards[3]

        self._btns_cards.append(tk.Button(self, command=partial(self.OnCardButtonClick, 1)))
        self._btns_cards[4].grid(column=4, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(4, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self._btns_cards[4]['state']=tk.DISABLED
        self._lbls_cards.append(tk.StringVar())
        self._lbls_cards[4].set('--')
        self._btns_cards[4]['textvariable']=self._lbls_cards[4]

        self._btns_cards.append(tk.Button(self, command=partial(self.OnCardButtonClick, 1)))
        self._btns_cards[5].grid(column=5, row=0) # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(5, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx
        self._btns_cards[5]['state']=tk.DISABLED
        self._lbls_cards.append(tk.StringVar())
        self._lbls_cards[5].set('--')
        self._btns_cards[5]['textvariable']=self._lbls_cards[5]

        for b in self._btns_cards:
             b['height']=8
             b['width']=10
             b['relief']=tk.RIDGE

        self._btn_undo = ttk.Button(self, text='Undo', command=self.OnUndoButtonClick)
        self._btn_undo.grid(column=6, row=0, sticky='E') # Grid-2 in Documentation\UI_WireFrame.pptx
        self.columnconfigure(6, weight=1) # Grid-2 in Documentation\UI_WireFrame.pptx

    def OnCardButtonClick(self, index):
        # Inform the mediator object which index button was pressed
        
        # Temporarily, for proof-of-concept, if card button 0 is clicked, call play() method of stub app, on a new thread
        if index == 0:
            self.master._game = StubGame(self.master.master, self.master)
            thread = Thread(target=self.master._game.play)
            thread.start()
        # Temporarily, for proof-of-concept, if card button 1 is clicked, it is a response to a request for input from the game, and
        # the response shoudl be injected into the game's response queue
        if index == 1:
            self.master._game._response_queue.put('1', timeout=1)
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
            self._player2_holes[i]['variable'] = self._player2_pegs[i]
        for i in range(31,62):
            self._player2_holes.append(ttk.Checkbutton(self._player2_track, text=str(i)))
            self._player2_holes[i].grid(column=1, row=(i-30)) # Grid-3 in Documentation\UI_WireFrame.pptx
            self._player2_track.rowconfigure((i-30), weight=1) # Grid-3 in Documentation\UI_WireFrame.pptx
            self._player2_holes[i]['state']=tk.DISABLED
            # Create and assign control variables
            self._player2_pegs.append(tk.IntVar())
            self._player2_holes[i]['variable'] = self._player2_pegs[i]
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
        # Clear any existing peg locations
        for p in self._player1_pegs: p.set(0)
        # Set the new peg locatons
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
        # Clear any existing peg locations
        for p in self._player2_pegs: p.set(0)
        # Set the new peg locatons
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
        self.insert_end('Player 2 scored 15 for 2: KH 5S\nPlayer 1 scored pair for 2; 5S 5D')

    def insert_end(self, message=''):
        self._txt_info.insert('end', message)
        return None
        

class StubGame:
    """
    A simple class used as a proxy for the GribbageGame class, for purposes of exploring how I can plumb the game to CribbageApp.
    """
    def __init__(self, destination, queue_owner):
        """
        """
        # The tkinter widget that will generate events when the game has ouput to sent to the CribbageApp
        self._destination = destination
        # The CribbageApp, used to access its _game_event_queue member. In the actual implementation, might just make this a callback
        # since all we need to ever do from this end is a put.
        self._queue_owner = queue_owner
        # The queue where we expect the CribbageApp to place a response to a querey for input from the user
        self._response_queue = Queue(10)
    
    def play(self):
        """
        """
        # Send an event to CribbageApp
        sleep(1)
        self.send_event()
        sleep(1)
        # Request input from CribbageApp
        result = self.request_input()
        return None
    
    def request_input(self):
        """
        """
        # Add a query item to the game event queue
        self._queue_owner._game_event_queue.put(item=('play_card_query','5S'), timeout=1)
        # Generate event that will cause the query item to be picked out of the game event queue and acted on
        self._destination.event_generate('<<CribbageGameQueryEvent>>')
        # Wait in a tight loop for the CribbageApp to provide a response in the response queue
        while self._response_queue.empty():
            sleep(1)
        response = self._response_queue.get(timeout=1)
        return None
    
    def send_event(self):
        """
        """
        # Add an item to the game event queue
        self._queue_owner._game_event_queue.put(item=(35,29), timeout=1)
        # Generate event that will cause the item to be picked out of the game event queue and acted on
        self._destination.event_generate('<<CribbageGameOutputEvent>>')
        
        return False

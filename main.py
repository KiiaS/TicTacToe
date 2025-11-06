from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

from game import TicTacToe

class Board(GridLayout):
    def __init__(self, game: TicTacToe, status_label: Label, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.spacing = 8
        self.padding = 12
        self.game = 12
        self.game = game
        self.status_label = status_label
        self.buttons: dict[int, Button] = {}

        for i in range(1, 10):
            btn = Button(text="", font_size=48)
            btn.bind(on_release=lambda b, pos=i: self.on_press_cell(pos))
            self.buttons[i] = btn
            self.add_widget(btn)
        
        self.refresh()

    def on_press_cell(self, pos: int):
        if self.game.complete:
            return
        moved = self.game.move(pos)
        if moved:
            self.refresh()
    
    def refresh(self):
        for i, btn in self.buttons.items():
            v = self.game.spots[i]
            btn.text = v if v in {'X', 'O'} else ""
            btn.disabled = v in {'X', 'O'} or self.game.complete
        
        if self.game.complete:
            if self.game.winner:
                self.status_label.text = f"Voittaja: {self.game.winner} - Aloita uusi?"
            else:
                self.status_lebel.text = "Tasapeli - Aloita uusi?"
        else:
            self.status_label.text = f"Pelaajan vuoro: {self.game.current_player()}"

class TTTApp(App):
    def build(self):
        Window.size = (420, 720)
        self.game = TicTacToe()

        root = BoxLayout(orientation='vertical', padding=12, spacing=8)

        self.status = Label(text="", font_size=24, size_hint_y=None, height=50)
        board = Board(self.game, self.status)

        controls = BoxLayout(size_hint_y=None, height=60, spacing=8)
        reset_btn = Button(text="Uusi peli")
        reset_btn.bind(on_release=self.on_reset)
        controls.add_widget(reset_btn)

        root.add_widget(self.status)
        root.add_widget(board)
        root.add_widget(controls)

        board.refresh()
        return root
    
    def on_reset(self, *_):
        self.game.reset()
        for child in self.root.children:
            if isinstance(child, Board):
                child.refresh()
        self.status.text = f"Pelaajan vuoro: {self.game.current_player()}"

if __name__ == "__main__":
    TTTApp().run()

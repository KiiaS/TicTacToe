from dataclasses import dataclass, field

@dataclass
class TicTacToe:
    spots: dict = field(default_factory=lambda: {i: str(i) for i in range(1, 10)})
    turn: int = 0
    complete: bool = False
    winner: str | None = None

    def current_player(self) -> str:
        return 'X' if self.turn % 2 == 0 else 'O'
    
    def move(self, pos: int) -> bool:
        if self.complete or pos not in self.spots:
            return False
        if self.spots[pos] in {'X', 'O'}:
            return False
        
        self.spots[pos] = self.current_player()
        self.turn += 1

        if self._check_for_win():
            self.complete = True
            self.winner = self.spots[pos]
        elif self.turn >= 9:
            self.complete = True
            self.winner = None
        return True
    
    def reset(self):
        self.spots = {i: str(i) for i in range(1, 10)}
        self.turn = 0
        self.complete = False
        self.winner = None

    def _check_for_win(self) -> bool:
        s = self.spots
        lines = [
            (1,2,3),(4,5,6),(7,8,9),
            (1,4,7),(2,5,8),(3,6,9),
            (1,5,9),(3,5,7)
        ]
        return any(s[a] == s[b] == s[c] for a,b,c in lines)
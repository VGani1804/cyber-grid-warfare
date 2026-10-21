from card import Deck

class Player:
    def __init__(self, name, color, start_pos):
        self.name = name
        self.color = color          # "blue" hoặc "red"
        self.start_pos = start_pos  # (0, 0) hoặc (9, 9)
        self.deck = Deck()
        self.hand = []
        for _ in range(5):
            self.draw_card()

    def draw_card(self):
        if len(self.hand) < 5:
            card = self.deck.draw()
            if card: self.hand.append(card)
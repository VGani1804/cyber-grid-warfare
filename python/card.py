import random

class Card:
    def __init__(self, card_type, value=0, name=""):
        self.card_type = card_type  # "NUMBER" hoặc "EFFECT"
        self.value = value          # 1-9
        self.name = name            # "NEGATE", "LOCK", "SWAP"

    def __repr__(self):
        return f"[{self.value}]" if self.card_type == "NUMBER" else f"[{self.name}]"

class Deck:
    def __init__(self):
        self.cards = []
        self._build_deck()
        self.shuffle()

    def _build_deck(self):
        for val in [1, 2, 3]:
            for _ in range(4): self.cards.append(Card("NUMBER", value=val))
        for val in [4, 5, 6, 7]:
            for _ in range(2): self.cards.append(Card("NUMBER", value=val))
        for _ in range(2): self.cards.append(Card("NUMBER", value=8))
        self.cards.append(Card("NUMBER", value=9))
        for _ in range(2):
            self.cards.append(Card("EFFECT", name="NEGATE"))
            self.cards.append(Card("EFFECT", name="LOCK"))
            self.cards.append(Card("EFFECT", name="SWAP"))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None
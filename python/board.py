class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[{"value": 0, "owner": None, "color": None, "locked": False} for _ in range(size)] for _ in range(size)]

    def is_valid_position(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def has_adjacent_ownership(self, x, y, player_name):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_position(nx, ny):
                if self.grid[nx][ny]["owner"] == player_name:
                    return True
        return False

    def can_place_number(self, x, y, card, player):
        if not self.is_valid_position(x, y): return False, "Ngoài bàn cờ!"
        cell = self.grid[x][y]
        if cell["locked"]: return False, "Ô đã bị khóa!"
        if cell["owner"] is None and (x, y) == player.start_pos: return True, "Hợp lệ"
        if not self.has_adjacent_ownership(x, y, player.name): return False, "Phải đặt liền kề lãnh thổ!"
        if cell["owner"] is None: return True, "Hợp lệ"
        if cell["owner"] != player.name:
            if card.value > cell["value"]: return True, "Hợp lệ (Đè quân)"
            return False, f"Cần số lớn hơn {cell['value']}!"
        return False, "Ô đã thuộc về bạn!"

    def place_card(self, x, y, card, player):
        valid, msg = self.can_place_number(x, y, card, player)
        if valid:
            self.grid[x][y]["value"] = card.value
            self.grid[x][y]["owner"] = player.name
            self.grid[x][y]["color"] = player.color
            player.hand.remove(card)
            player.draw_card()
            return True, msg
        return False, msg
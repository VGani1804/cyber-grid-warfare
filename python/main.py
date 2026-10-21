from pyscript import document
from board import Board
from player import Player
from ai import get_ai_move

# Khởi tạo game state
board = Board(10)
player = Player("Player", "blue", (0, 0))
ai = Player("AI", "red", (9, 9))
selected_card_index = None


def render_board():
    board_div = document.querySelector("#board")
    board_div.innerHTML = ""
    for r in range(10):
        for c in range(10):
            cell_data = board.grid[r][c]
            cell_div = document.createElement("div")
            cell_div.className = "cell"
            if cell_data["color"]:
                cell_div.classList.add(cell_data["color"])
            if cell_data["locked"]:
                cell_div.classList.add("locked")

            if cell_data["value"] > 0:
                cell_div.innerText = str(cell_data["value"])

            # Gắn sự kiện click vào ô trên bàn cờ
            def make_click(row, col):
                def handler(event):
                    on_cell_click(row, col)

                return handler

            cell_div.onclick = make_click(r, c)
            board_div.appendChild(cell_div)


def render_hand():
    hand_div = document.querySelector("#hand")
    hand_div.innerHTML = ""
    for i, card in enumerate(player.hand):
        card_div = document.createElement("div")
        card_div.className = "card-item"
        if i == selected_card_index:
            card_div.classList.add("selected")
        card_div.innerText = str(card.value) if card.card_type == "NUMBER" else card.name[0]

        def make_card_click(index):
            def handler(event):
                global selected_card_index
                selected_card_index = index
                render_hand()

            return handler

        card_div.onclick = make_card_click(i)
        hand_div.appendChild(card_div)


def on_cell_click(r, c):
    global selected_card_index
    if selected_card_index is None:
        document.querySelector("#status").innerText = "Vui lòng chọn lá bài trước!"
        return

    card = player.hand[selected_card_index]
    if card.card_type == "NUMBER":
        success, msg = board.place_card(r, c, card, player)
        if success:
            selected_card_index = None
            render_board()
            render_hand()
            document.querySelector("#status").innerText = "Lượt AI đang tính toán..."

            # Lượt AI đi
            ai_move = get_ai_move(board, ai)
            if ai_move:
                ar, ac, acard = ai_move
                board.place_card(ar, ac, acard, ai)
                render_board()
                document.querySelector("#status").innerText = "Lượt của bạn - Chọn bài:"
            else:
                document.querySelector("#status").innerText = "AI hết nước đi! Bạn thắng!"
        else:
            document.querySelector("#status").innerText = f"Lỗi: {msg}"


# Khởi chạy ban đầu
render_board()
render_hand()
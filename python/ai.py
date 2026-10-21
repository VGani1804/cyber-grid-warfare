import random


def evaluate_move(board, r, c, card, ai_player, human_player_name="Player"):
    """
    Hàm chấm điểm nước đi tiềm năng của AI tại vị trí (r, c) với lá bài card.
    Điểm càng cao -> Nước đi càng mang tính chiến thuật.
    """
    score = 0
    cell = board.grid[r][c]

    # 1. ĐẤU TRÍ ĐÈ QUÂN: Cướp lãnh thổ của người chơi
    if cell["owner"] == human_player_name:
        stolen_value = cell["value"]
        # Thưởng lớn cho việc cướp ô, đặc biệt là cướp ô số to của đối thủ
        score += 30 + (stolen_value * 5)

    # 2. MỞ RỘNG TỰ DO: Chiếm ô trống
    elif cell["owner"] is None:
        score += 15

    # 3. QUẢN LÝ TÀI NGUYÊN: Bảo tồn lá bài mạnh
    if card.card_type == "NUMBER":
        val = card.value
        # Nếu dùng lá 8 hoặc 9 quá sớm vào ô trống nhỏ -> Trừ điểm phạt
        if val >= 8 and cell["owner"] is None:
            score -= 20
        # Ưu tiên dùng lá nhỏ (1-3) để rải đường
        elif val <= 3 and cell["owner"] is None:
            score += 10

    # 4. TÍNH TOÁN PHÂN VÙNG SECTOR (Mỗi góc 5x5)
    # Xác định ô (r, c) thuộc Sector nào (0,0), (0,1), (1,0), (1,1)
    sector_r = r // 5
    sector_c = c // 5
    ai_sector_score = 0
    player_sector_score = 0

    # Quét nhanh Sector 5x5 hiện tại
    for i in range(sector_r * 5, (sector_r + 1) * 5):
        for j in range(sector_c * 5, (sector_c + 1) * 5):
            curr_cell = board.grid[i][j]
            if curr_cell["owner"] == ai_player.name:
                ai_sector_score += curr_cell["value"]
            elif curr_cell["owner"] == human_player_name:
                player_sector_score += curr_cell["value"]

    # Nếu AI đang tranh chấp quyết liệt hoặc thua hẹp ở Sector này -> Thưởng điểm để chiếm quyền Root Access
    if 0 < (player_sector_score - ai_sector_score) <= 10:
        score += 25

    # 5. PHONG TỎA ĐỐI THỦ: Kiểm tra các ô xung quanh người chơi
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if board.is_valid_position(nr, nc):
            adj_cell = board.grid[nr][nc]
            # Nếu đặt ô này giúp chặn đường mở rộng của Người chơi
            if adj_cell["owner"] == human_player_name:
                score += 8

    # Bổ sung yếu tố ngẫu nhiên nhỏ (0-3 điểm) để AI không bị lối đi rập khuôn
    score += random.uniform(0, 3)
    return score


def get_ai_move(board, ai_player):
    """
    Thuật toán AI duyệt qua tất cả nước đi hợp lệ,
    chấm điểm từng nước và chọn ra nước đi chiến thuật nhất.
    """
    best_move = None
    best_score = -9999

    # Quét toàn bộ bàn cờ 10x10
    for r in range(board.size):
        for c in range(board.size):
            # Duyệt từng lá bài trên tay AI
            for card in ai_player.hand:
                if card.card_type == "NUMBER":
                    valid, _ = board.can_place_number(r, c, card, ai_player)
                    if valid:
                        # Tính điểm chiến thuật cho nước đi này
                        move_score = evaluate_move(board, r, c, card, ai_player)

                        if move_score > best_score:
                            best_score = move_score
                            best_move = (r, c, card)

    return best_move
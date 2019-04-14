from board import Board
from phase import Phase


class Moderator:
    """
    対局の管理を行うクラス
    Todo:
        双掌繚乱・眼前構築もここで行う
    """
    def __init__(self, first_deck, second_deck):
        self.board = Board(first_deck, second_deck)
        self.turn = 0

    def start_battle(self):
        """
        決闘を開始する
        
        カードを3枚ドロー
        マリガン（未実装）
        先手の開始フェーズ実行
        """
        # 決闘開始前の3枚ドローとマリガン
        Phase.setup_phase(self.board)

        # 決闘開始
        self.turn = 1
        Phase.main_phase(self.board)
        Phase.closing_phase(self.board)
        while True:
            self.turn += 1
            Phase.opening_phase(self.board)
            Phase.main_phase(self.board)
            Phase.closing_phase(self.board)

    def do_basic_action(self, action_type, use_vigor, down_card_index=None):
        pass

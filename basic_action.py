"""
基本動作を定義する
Todo:
    * 選択可能かの判定（前進と離脱など）
    * Transformの追加基本動作
"""
from exception import *
from board import Board, PlayerType
from area import Area


class BasicAction:
    """
    基本動作を集めたクラス
    """
    @staticmethod
    def step_forward(board: Board, player_type: PlayerType):
        if board.distance.removable() == 0 or \
                board.players[player_type].aura.receivable() == 0:
            raise BasicActionException('前進できません！')
        if board.distance() <= board.expert_distance:
            raise DistanceException('前進できません！')
        Area.move_flowers(board.distance, board.players[player_type].aura, 1)

    @staticmethod
    def step_backward(board: Board, player_type: PlayerType):
        if board.players[player_type].aura.removable() == 0 or \
                board.distance.receivable() == 0:
            raise BasicActionException('後退できません！')
        Area.move_flowers(board.players[player_type].aura, board.distance, 1)

    @staticmethod
    def protect(board: Board, player_type: PlayerType):
        if board.dust.removable() == 0 or \
                board.players[player_type].aura.receivable() == 0:
            raise BasicActionException('纏えません！')
        Area.move_flowers(board.dust, board.players[player_type].aura, 1)

    @staticmethod
    def charge(board: Board, player_type: PlayerType):
        if board.players[player_type].aura.removable() == 0:
            raise BasicActionException('宿せません！')
        Area.move_flowers(board.players[player_type].aura,
                          board.players[player_type].flare, 1)

    @staticmethod
    def withdraw(board: Board):
        if board.dust.removable() == 0 or board.distance.receivable() == 0:
            raise FlowerLackException('離脱できません！')
        if board.distance() > board.expert_distance:
            raise DistanceException('離脱できません！')
        Area.move_flowers(board.dust, board.distance(), 1)

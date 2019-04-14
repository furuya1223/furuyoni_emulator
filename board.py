"""
局面クラス
"""
from area import Distance, Dust, OutOfGame
from player import PlayerType, Player
from collections import deque


class Board:
    """
    局面を表すクラス
    もっと役割を外部に投げるべきな気がする
    
    Attributes:
        distance (Distance): 間合エリア
        dust (Dust): ダスト
        out_of_game (OutOfGame): ゲーム外領域の桜花結晶
        expert_distance (int): 達人の間合
        turn_player (PlayerType): 現在のターンプレイヤー
        start_distance (int): ターン開始時の間合
        finished (bool): ゲームが終了したか否か
        players (Player): プレイヤー（先攻と後攻）
    """
    def __init__(self, first_deck, second_deck):
        self.distance = Distance()
        self.dust = Dust()
        self.out_of_game = OutOfGame()
        self.expert_distance = 2
        self.turn_player = PlayerType.FIRST
        self.start_distance = 10  # 開始時間合い
        self.finished = False
        self.attacks = deque()
        self.players = {PlayerType.FIRST: Player(PlayerType.FIRST, first_deck),
                        PlayerType.SECOND: Player(PlayerType.SECOND, second_deck)}

    def distance(self):
        return self.distance()

    def show_board(self):
        """
        局面情報を表示する
        """
        print('========================')
        print('間合: {}（達人の間合: {}）'
              .format(str(self.distance),
                      self.expert_distance))
        for player_type in PlayerType:
            print(self.players[player_type])
        print('ダスト: {}'.format(self.dust.flowers))
        print('手札: {}'.format(self.players[self.turn_player].hand))
        print('========================')

    def show_unused_trump(self, player_type):
        # 未使用の切札を表示
        for i, trump in enumerate(self.players[player_type].trumps):
            if not trump.used:
                print('[1{}]: {}, '.format(i, trump.card), end='')
        print()

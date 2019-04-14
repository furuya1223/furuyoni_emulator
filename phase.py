from board import Board
from player import PlayerType, Player
from basic_action import BasicAction
from exception import *


class Phase:
    @staticmethod
    def setup_phase(board):
        # 決闘開始前の3枚ドローとマリガン
        for player_type in PlayerType:
            board.players[player_type].draw(3)
            # TODO: マリガン

    @staticmethod
    def opening_phase(board: Board):
        # 開始フェイズ
        player_type = board.turn_player
        print('{}のターン'.format(str(player_type)))
        # 開始時の間合のセット
        board.start_distance = board.distance
        # TODO: 間合にある造花結晶の処理
        # 集中力+1
        board.players[player_type].vifor.recover()

        # TODO: 付与札の結晶の移動と破棄時効果の解決

        # 再構成するかどうか聞く
        print('山札の再構成を行いますか？[y/n]')
        if input() == 'y':
            Phase.reconstruction(board, player_type)

        # 2枚ドロー
        board.players[player_type].draw(2)

    @staticmethod
    def reconstruction(board, player_type):
        # 山札の再構成
        board.players[player_type].reconstruction()

    @staticmethod
    def main_phase(board: Board):
        # メインフェイズ
        board.show_board()
        player_type = board.turn_player
        print('[0]: 標準行動, [1]: 全力行動')
        if input() == '0':
            # 標準行動
            while True:
                try:
                    board.show_board()
                    print('ターンを終了しますか？[y/n]')
                    if input() == 'y':
                        break
                    print('[0]: 基本行動, [1]: カードの使用')
                    if input() == '0':
                        # 基本行動
                        if board.players[player_type].vigor() == 0:
                            if len(board.players[player_type].hand) == 0:
                                raise BasicActionException('基本行動のリソースがありません！')
                            # 集中力が0なので手札を伏せる
                            select_vigor = False
                        elif len(board.players[player_type]) == 0:
                            # 手札が0枚なので集中力を使用する
                            select_vigor = True
                        else:
                            print('[0]: 集中力を使用, [1]: 手札を伏せる')
                            select_vigor = (input() == '0')
                        if select_vigor:
                            # 集中力を1消費して基本行動
                            board.players[player_type].vigor -= 1
                        else:
                            # 手札を1枚伏せて基本行動
                            print('伏せる手札を選択してください')
                            board.players[player_type].show_hand()
                            index = int(input())
                            # TODO: ここで伏せたら不正な行動を選んだときに伏せっぱなしになる
                            board.players[player_type].down(index)
                        print('行動を選んでください')
                        # TODO: 前進・離脱の切り替え
                        print('[0]: 前進, [1]: 後退, [2]: 纏い, [3]: 宿し, [4]: 離脱')
                        selection = int(input())
                        if selection == 0:
                            BasicAction.step_forward(board, player_type)
                        elif selection == 1:
                            BasicAction.step_backward(board, player_type)
                        elif selection == 2:
                            BasicAction.protect(board, player_type)
                        elif selection == 3:
                            BasicAction.charge(board, player_type)
                        elif selection == 4:
                            BasicAction.withdraw(board)
                    else:
                        # カードの使用
                        print('使用するカードを選択してください')
                        board.players[player_type].show_hand()
                        board.players[player_type].show_unused_trumps()
                        index = int(input())
                        if index < 10:
                            board.players[player_type].hand.play(index, board, player_type)
                            board.players[player_type].discard(index)
                        else:
                            index -= 10
                            # 切札の使用
                            board.players[player_type].trumps.play(index, board, player_type)
                except (DistanceException, FlowerLackException, BasicActionException) as e:
                    print(e)
                    continue
                except IndexError:
                    print('番号の指定が不正です！')
                    continue

        else:
            # 全力行動
            pass

    @staticmethod
    def closing_phase(board):
        # 終了フェイズ
        player_type = board.turn_player
        # TODO: 手札上限の処理
        if len(board.players[player_type].hand):
            print('手札の数が上限を超えています．伏せる手札を選んでください')
            board.show_hand(player_type)
            index = list(map(int, input().split(' ')))
            board.down(player_type, index)
        # TODO: 傘の開閉判定
        # TODO: 切札の再起判定
        # TODO: 効果切れの判定
        board.turn_player = player_type.opponent()

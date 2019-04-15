from board import Board
from player import PlayerType
from basic_action import BasicAction
from exception import *
from util import generator
from constants import NORMAL_ACTION, FULL_POWER_ACTION, BASIC_ACTION,\
    USE_CARD, FINISH_TURN, CANCEL, PAY_VIGOR, DOWN_HAND, STEP_FORWARD,\
    WITHDRAW, STEP_BACKWARD, PROTECT, CHARGE, COMPLETED, CANCELED


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
        player_type = board.turn_player_type
        print('{}のターン'.format(str(player_type)))
        # 開始時の間合のセット
        board.start_distance = board.distance
        # TODO: 間合にある造花結晶の処理
        # 集中力+1
        board.players[player_type].vigor.recover()

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
    @generator
    def main_phase(board: Board):
        # メインフェイズ
        board.show_board()
        while True:
            action_type = yield '[{}]: 標準行動, [{}]: 全力行動, [{}]: ターンを終了' \
                .format(NORMAL_ACTION, FULL_POWER_ACTION, FINISH_TURN)
            if action_type in [NORMAL_ACTION, FULL_POWER_ACTION, FINISH_TURN]:
                break
            else:
                print('入力が不正です！')
        if action_type == FINISH_TURN:
            raise StopIteration
        elif action_type == NORMAL_ACTION:
            # 標準行動
            yield from Phase.normal_action(board)
        elif action_type == FULL_POWER_ACTION:
            # 全力行動
            pass

    @staticmethod
    def normal_action(board):
        while True:
            try:
                board.show_board()
                while True:
                    normal_action_type = yield '[{}]: 基本行動, ' \
                                               '[{}]: カードの使用, ' \
                                               '[{}]: ターンを終了' \
                        .format(BASIC_ACTION, USE_CARD, FINISH_TURN)
                    if normal_action_type in [BASIC_ACTION, USE_CARD,
                                              FINISH_TURN]:
                        break
                    else:
                        print('入力が不正です！')
                if normal_action_type == FINISH_TURN:
                    break
                elif normal_action_type == BASIC_ACTION:
                    # 基本行動
                    result = yield from Phase.basic_action(board)
                    if result == CANCELED:
                        continue
                elif normal_action_type == '1':
                    # カードの使用
                    yield from Phase.use_card(board)
            except (DistanceException, FlowerLackException,
                    BasicActionException) as e:
                print(e)
                continue
            except IndexError:
                print('番号の指定が不正です！')
                continue

    @staticmethod
    def basic_action(board):
        # 基本行動
        # 消費するリソースの種類の選択
        if board.turn_player().vigor() == 0:
            if len(board.turn_player().hand) == 0:
                raise BasicActionException('基本行動のリソースがありません！')
            # 集中力が0なので手札を伏せる
            resource_selection = DOWN_HAND
        elif len(board.turn_player().hand) == 0:
            # 手札が0枚なので集中力を使用する
            resource_selection = PAY_VIGOR
        else:
            while True:
                resource_selection = yield '[{}]: 集中力を使用, ' \
                                           '[{}]: 手札を伏せる, ' \
                                           '[{}]: キャンセル' \
                    .format(PAY_VIGOR, DOWN_HAND, CANCEL)
                if resource_selection in [PAY_VIGOR, DOWN_HAND,
                                          CANCEL]:
                    break
                else:
                    print('入力が不正です！')
            if resource_selection == CANCEL:
                print('キャンセルします')
                return CANCELED

        # リソースの消費
        if resource_selection == PAY_VIGOR:
            # 集中力を1消費して基本行動
            board.turn_player().vigor -= 1
        elif resource_selection == DOWN_HAND:
            # 手札を1枚伏せて基本行動
            print('伏せる手札を選択してください')
            index = yield board.turn_player().show_hand() + \
                ', [{}]: キャンセル'.format(CANCEL)
            if index == CANCEL:
                print('キャンセルします')
                return CANCELED
            index = int(index)
            # TODO: ここで伏せたら不正な行動を選んだときに伏せっぱなしになる
            board.turn_player().down(index)

        # 行動の選択
        print('行動を選んでください')
        while True:
            basic_action_selection = yield '[{}]: {}, [{}]: 後退, ' \
                                           '[{}]: 纏い, [{}]: 宿し' \
                .format(STEP_FORWARD,
                        ('離脱' if board.is_close() else '前進'),
                        STEP_BACKWARD, PROTECT, CHARGE)
            if basic_action_selection in [
                (WITHDRAW if board.is_close() else STEP_FORWARD),
                    STEP_BACKWARD, PROTECT, CHARGE]:
                break
            else:
                print('入力が不正です！')

        # 行動の実行
        if basic_action_selection == (
                WITHDRAW if board.is_close() else STEP_FORWARD):
            if board.is_close():
                BasicAction.withdraw(board)
            else:
                BasicAction.step_forward(board,
                                         board.turn_player_type)
        elif basic_action_selection == 1:
            BasicAction.step_backward(board,
                                      board.turn_player_type)
        elif basic_action_selection == 2:
            BasicAction.protect(board, board.turn_player_type)
        elif basic_action_selection == 3:
            BasicAction.charge(board, board.turn_player_type)
        elif basic_action_selection == 4:
            BasicAction.withdraw(board)
        return COMPLETED

    @staticmethod
    def use_card(board):
        # カードの使用
        print('使用するカードを選択してください')
        index = yield \
            board.turn_player().show_hand() + '\n' + \
            board.turn_player().show_unused_trumps()
        index = int(index)
        if index < 10:
            board.turn_player().hand.play(index, board,
                                          board.turn_player_type)
            board.turn_player().discard(index)
        else:
            index -= 10
            # 切札の使用
            board.turn_player().trumps.play(index, board,
                                            board.turn_player_type)

    @staticmethod
    def closing_phase(board):
        # 終了フェイズ
        player_type = board.turn_player
        # TODO: 手札上限の処理
        if len(board.players[player_type].hand) > 2:
            print('手札の数が上限を超えています．伏せる手札を選んでください')
            board.players[player_type].show_hand()
            index = list(map(int, input().split(' ')))
            board.players[player_type].down(index)
        # TODO: 傘の開閉判定
        # TODO: 切札の再起判定
        # TODO: 効果切れの判定（"このターンの終わりまで"のもの）
        board.turn_player = player_type.opponent()


# ==============================================================================
# 345678901234567890123456789012345678901234567890123456789012345678901234567890
# ==============================================================================
"""
EasyAIに基づくReversi対戦プログラム

    2021-05-19 IIJIMA, Tadashi
    (Original: Copyright (c) 2013 Zulko The MIT License)

  * 本来は，pip install easyAIで使用可能になるが...
    * 今回はこの先の改良のためにあえてソースコードを取り込んでいる．
    * https://pypi.org/project/easyAI/
  * ソースコード入手元:
    * https://github.com/Zulko/easyAI
"""
 
# ==============================================================================
import numpy as np
# ==============================================================================
#from easyAI import TwoPlayersGame
#from easyAI import Human_Player, AI_Player
#from easyAI import Negamax
# ==============================================================================
from Game     import TwoPlayersGame
from Player   import Human_Player, AI_Player
from Negamax  import Negamax
# ==============================================================================

# ==============================================================================
to_string = lambda a : "ABCDEFGH"[a[0]] + str(a[1]+1)
to_array  = lambda s : np.array(["ABCDEFGH".index(s[0]),int(s[1])-1])
# ==============================================================================
 
# ==============================================================================
# ===== [クラス] リバーシ ======================================================
# ==============================================================================
class Reversi( TwoPlayersGame ):
    """ Revesiクラス.

    """
    # ==========================================================================
 
    # ==========================================================================
    # ===== [イニシャライザ] 初期化する ======================================== 
    # ==========================================================================
    def __init__(self, players, board = None):
        """ 初期化する.
        """
        # ======================================================================
        # ===== プレイヤーのリスト
        self.players = players
        # ===== ボード (8x8)
        self.board = np.zeros( (8,8), dtype=int )
        # ===== 初期配置
        self.board[3,[3,4]] = [1,2]
        self.board[4,[3,4]] = [2,1]
        # ===== 手番
        self.nplayer = 1
        # ======================================================================
 
  
    # ==========================================================================
    # ===== [メソッド] 次に打つことが可能な手のリストを返す ====================
    # ==========================================================================
    def possible_moves(self):
        """ 次に打つことが可能な手のリストを返す.
        """
        # ======================================================================
        return [to_string((i,j)) for i in range(8) for j in range(8)
            if (self.board[i,j] == 0)
            and (pieces_flipped(self.board, (i,j), self.nplayer) != [])]
        # ======================================================================
  
    # ==========================================================================
    # ===== [メソッド] 指定した手を打つ ========================================
    # ==========================================================================
    def make_move(self, pos):
        """ 指定した手を打つ.
        """
        # ======================================================================
        pos= to_array(pos)
        flipped = pieces_flipped(self.board, pos, self.nplayer)
        for i,j in flipped:
            self.board[i,j] = self.nplayer
        self.board[pos[0],pos[1]] = self.nplayer
        # ======================================================================
  
    # ==========================================================================
    # ===== [メソッド] ==========================================
    # ==========================================================================
    def show(self):
        """ .
        """
        # ======================================================================
        print('\n'+'\n'.join(['  1 2 3 4 5 6 7 8']+ ['ABCDEFGH'[k] +
                ' '+' '.join([['.','1','2','X'][self.board[k][i]]
                for i in range(8)]) for k in range(8)]+['']))
        # ======================================================================
  
    # ==========================================================================
    # ===== [メソッド] 勝敗判定 ================================================
    # ==========================================================================
    def is_over( self ):
        """ 勝敗判定.
        """
        # ======================================================================
        return( self.possible_moves() == [] )
        # ======================================================================
  
    # ==========================================================================
    # ===== [メソッド] 評価値を返す ============================================
    # ==========================================================================
    def scoring( self ):
        """ 評価値 .
        """
        # ======================================================================
        if np.sum(self.board==0) > 32: # less than half the board is full

            player   = self.board==self.nplayer
            opponent = self.board==self.nopponent
            #print( player )
            #print( opponent )
            
            # return ((player-opponent)*BOARD_SCORE).sum()
            return ((player^opponent)*BOARD_SCORE).sum()
        else:
            npieces_player = np.sum(self.board==self.nplayer)
            npieces_opponent = np.sum(self.board==self.nopponent)
            return  npieces_player - npieces_opponent
        # ======================================================================

# ==============================================================================
# This board is used by the AI to give more importance to the border
BOARD_SCORE = np.array( [[9,3,3,3,3,3,3,9],
                         [3,1,1,1,1,1,1,3],
                         [3,1,1,1,1,1,1,3],
                         [3,1,1,1,1,1,1,3],
                         [3,1,1,1,1,1,1,3],
                         [3,1,1,1,1,1,1,3],
                         [3,1,1,1,1,1,1,3],
                         [9,3,3,3,3,3,3,9]])
# ==============================================================================

# ==============================================================================
DIRECTIONS = [ np.array([i,j]) for i in [-1,0,1] for j in [-1,0,1]
                               if (i!=0 or j!=0)]
# ==============================================================================

# ==============================================================================
# ===== [関数] ひっくり返される石の数 ==========================================
# ==============================================================================
def pieces_flipped( board, pos, nplayer ):
    """ ひっくり返される石の数.
    """
    # ==========================================================================
 
    flipped = []
 
    for d in DIRECTIONS:
        ppos = pos + d
        streak = []
        while (0<=ppos[0]<=7) and (0<=ppos[1]<=7):
            if board[ppos[0],ppos[1]] == 3 - nplayer:
                streak.append(+ppos)
            elif board[ppos[0],ppos[1]] == nplayer:
                flipped += streak
                break
            else:
                break
            ppos += d
    # ==========================================================================
    return flipped
    # ==========================================================================

# ==============================================================================
# ===== [関数] メイン関数 ======================================================
# ==============================================================================
def main():
    """ .
    """
    # ==========================================================================
    # ===== コンピュータ vs コンピュータ =======================================
    game = Reversi( [ AI_Player( Negamax( 4 ) ), AI_Player( Negamax( 4 ) ) ] )
    # ===== ゲームをプレイする =================================================
    game.play()
    # ===== 結果を表示する =====================================================
    if game.scoring() > 0:
        print( "player) wins." % game.nplayer )
    elif game.scoring() < 0:
        print( "player %d wins." % game.nopponent )
    else:
        print( "Draw." )
    # ==========================================================================

# ==============================================================================
# ===== [スクリプト] メイン・スクリプト ========================================
# ==============================================================================
if __name__ == "__main__":
    main()
# ==============================================================================

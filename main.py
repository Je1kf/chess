# Python chess player

# ToDo
# - Actual movement
# - Taking a piece out
# - Coronacion del peón
# - function for checking mate
# - function for checking draw
# - function for checking o-o and o-o-o
# - function for checking stalemate
# - function for en-passant
#
# Pieces:
#    pawn   : p
#    Knight : N
#    Bishop : B
#    Rook   : R
#    Queen  : Q
#    King   : K
#
# Teams: 
#    White : 0
#    Black : 1
#
# Board is defined by a dictionary using conventional
# chess notation

class chess:
    def __init__(self):
        self.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.rows = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.back_rank = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        self.pieces = self.back_rank[0:5]
        self.pieces.append('p')
        self.pieces_names = {'p': 'Pawn', 'R': 'Rook', 'N': 'Knight',
                             'B': 'Bishop', 'Q': 'Queen', 'K': 'King'}
        self.pieces_points = {'R': 5, 'N': 2, 'B': 3, 'Q': 9, 'K': 4, 'p': 1}
        self.black = '\033[40m'
        self.white = '\033[44m'
        self.black_pieces = '\033[33m'
        self.to_move = 0  # First move, white to move
        self.mate = False
        self.to_move = 0  # White begins
        self.white_rooked = False
        self.black_rooked = False
        self.legal_movement = False

    def play(self):
        self.make_board()
        self.init_board()
        self.visualize_board()
        self.store_pieces_positions()

        # Begin the game
        print("> Remember to use algebraic notation: PieceColumnRow.")
        print("  > Example: Nf3")
        print("  > For pawns is not neccesary to specify the piece.")
        print("> Don't use extra characters like +, ++, ?, ??, !, or !!.")

        # Main loop
        while self.mate==False:
            if self.to_move == 0:
                print("\nWhite to move!")
            else:
                print("\nBlack to move!")


            mov = str(input())

            if mov == 'exit':
                print(f'Nice game. See you later!')
                break

            if self.check_move(mov) == False:
                print('Invalid movement, try again')
                continue

            self.alg2mov(mov)
            self.check_movement_legal()

            if self.legal_movement == False:
                print('Not a legal movement, try again')
                continue
            else:
                self.degeneracy()
                self.move_piece()


            self.store_pieces_positions()
            self.visualize_board()


            self.to_move = abs(self.to_move - 1)  # Changing turn

            # Checkmate's checking must be at the end of the turn

        # if f_pos[0] > 7 or f_pos[0] < 0 or f_pos[1] > 7 or f_pos[1] < 0:


    def make_board(self):
        # ["Piece", team]
        self.board = [[["", 0] for j in range(8)] for i in range(8)]

    def init_board(self):
        # Initial board configuration
        for i in range(8):
            self.board[i][1] = ['p', 0]  # Whites 0
            self.board[i][6] = ['p', 1]  # Blacks 1
            self.board[i][0] = [self.back_rank[i], 0]  # Whites 0
            self.board[i][7] = [self.back_rank[i], 1]  # Blacks 1

    def visualize_board(self):
        # CLI visualization of the board
        long_top = 7 * (+ 7*'\u2500' + '\u252C') + 7*'\u2500'
        long_mid = 7 * (7*'\u2500' + '\u253C') + 7*'\u2500'
        long_bot = 7 * (7*'\u2500' + '\u2534') + 7*'\u2500'
        aux = ''
        eux = ''
        perp_lines_even = '    \u2502' + 4 * (self.white + '       ' + \
                          self.black + '\u2502' + '       \u2502')
        perp_lines_odd = '    \u2502' + 4 * (self.black + '       ' +  \
                         self.black + '\u2502' + self.white + '       ' + \
                         self.black + '\u2502')
        for i in range(9):
            for j in range(9):
                if i == 0:
                    if j == 0:
                        print(end='\t')
                    else:
                        print(self.columns[j-1], end='\t')
                elif j == 0:
                    print(9-i, end='   \u2502')
                else:
                    if abs(j - i - 1) % 2 == 0:
                        aux = self.black
                        eux = self.white
                    else:
                        aux = self.white
                        eux = self.black

                    if self.board[j-1][-i][0] == '':
                        print(aux + '   \u00B7',
                              end=aux + '   '+ self.black + '\u2502')
                    else:
                        print(aux + \
                              self.board[j-1][-i][1]*self.black_pieces + \
                              '   \033[1m' + self.board[j-1][-i][0] + \
                              '\033[0m',
                              end=aux + '   ' + self.black + '\u2502' + eux)
                    if j == 8:
                        print(self.black, end='')

            if i == 0:
                print('\n\n    \u250C' + long_top + '\u2510\n' + perp_lines_even)
            elif i == 8:
                print('\n' + perp_lines_odd + '\n    \u2514' + long_bot + \
                      '\u2518\n')
            else:
                if i % 2 == 0:
                    print('\n' + perp_lines_odd + '\n    \u251C' + long_mid + \
                          '\u2524\n' + perp_lines_even)
                else:
                    print('\n' + perp_lines_even + '\n    \u251C' + long_mid + \
                          '\u2524\n' + perp_lines_odd)

        print('', end='\t')
        for col in self.columns:
            print(col, end='\t')

        print('\n')


    def get_position(self, piece, team):
        # get the position of an specific piece of one team (white 0, black 1)
        position = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == [piece, team]:
                    position.append([i, j])


        return position

    def store_pieces_positions(self):
        self.pieces_positions = [
                {piece: self.get_position(piece, 0) for piece in self.pieces},
                {piece: self.get_position(piece, 1) for piece in self.pieces},
                                ]

    def coords2alg(self, coord):
        # Transform algebraic position of squares into list's indices
        return [self.columns[coord[0]] + self.rows[coord[1]]]

    def alg2coords(self, alg):
        # Transform algebraic position of squares into list's indices
        return [self.columns.index(alg[0]), self.rows.index(alg[1])]

    def alg2mov(self, alg):
        if alg == 'o-o':
            if self.to_move == 0:
                self.piece_to_move = 'o-o'
            else:
                self.piece_to_move = 'o-o'
        elif alg == 'o-o-o':
            if self.to_move == 0:
                self.piece_to_move = 'o-o-o'
            else:
                self.piece_to_move = 'o-o-o'
        elif len(alg) == 2:
            self.piece_to_move = 'p'                  # Piece to be moved
            self.f_pos = self.alg2coords(alg[-2:])    # Final position
        else:
            self.piece_to_move = alg[0]           # Piece to be moved
            self.f_pos = self.alg2coords(alg[-2:])    # Final position


    def check_move(self, move):

        if move == 'o-o-o':
            return True
        elif move == 'o-o':
            return True
        elif len(move) > 3 or len(move) < 2:
            return False


        try:
            self.rows.index(move[-1])
        except:
            return False


        try:
            self.columns.index(move[-2])
        except:
            return False

        return True


    def check_movement_legal(self):
        # Checking if the movement is legal
        self.legal_movement = False

        if self.piece_to_move == 'o-o' or self.piece_to_move == 'o-o-o':
            if self.to_move == 0 and self.white_rooked == True:
                self.legal_movement = False
            elif self.to_move == 1 and self.black_rooked == True:
                self.legal_movement = False
            else:
                self.legal_movement = True
        elif self.piece_to_move == 'p':
            self.pawn_movement()
        elif self.piece_to_move == 'R':
            self.rook_movement()
        elif self.piece_to_move == 'B':
            self.bishop_movement()
        elif self.piece_to_move == 'Q':
            self.queen_movement()
        elif self.piece_to_move == 'K':
            self.king_movement()
        elif self.piece_to_move == 'N':
            self.knight_movement()

        # Check if self.f_pos given by player is in self.possible_movements
        for i, imov in enumerate(self.possible_movements):
            for jmov in imov:
                if jmov == self.f_pos:
                    self.i_pos = \
                    self.pieces_positions[self.to_move][self.piece_to_move][i]
                    self.legal_movement = True




        # ToDo p, R, N, B, Q, K

    def degeneracy(self):
        aux = []
        for i in range(len(self.possible_movements)):
            aux.append(self.possible_movements[i].count(self.f_pos))


        x = False
        print(aux)

        if aux.count(1) > 1:
            print("Degenerated movement.")
            while x == False:
                print(f"Which {self.pieces_names[self.piece_to_move]}", end="")
                print(" do you want to move?")
                alg = []

                for i in range(len(aux)):
                    if aux[i] == 1:
                        alg.append(self.coords2alg(self.pieces_positions[self.to_move]\
                                                   [self.piece_to_move]\
                                                   [i]))

                for i in range(len(alg)):
                        print(f"\t{i}. {alg[i][0]}")

                mov = int(input())
                print(alg[mov][0][0])
                try:
                    mov = self.alg2coords(alg[mov][0])
                except:
                    print("Try again.")
                else:
                    x = True

            self.i_pos = mov


    def move_piece(self):
        # move pieces in position i_pos to position f_pos
        self.board[self.f_pos[0]][self.f_pos[1]] = \
                                  self.board[self.i_pos[0]][self.i_pos[1]]
        self.board[self.i_pos[0]][self.i_pos[1]] = ["", 0]


    # Pieces Movements:
    def pawn_movement(self):
        p_pos = self.pieces_positions[self.to_move]['p']  # Pawns' positions
        self.possible_movements = []
        x = (-1) ** self.to_move  # for distinguishing black and white pawns

        for i, pos in enumerate(p_pos):
            self.possible_movements.append([])
            if pos[1]+x<8 and pos[1]+x>=0:
                if self.board[pos[0]][pos[1]+x][0] == '':
                    # one step forward
                    self.possible_movements[i].append([pos[0], pos[1]+x])
                if pos[0]+1<8:
                    if (self.board[pos[0]+1][pos[1]+x][0] != ''
                       and self.board[pos[0]+1][pos[1]+x][1] != self.to_move
                       ):
                        # right-hand side capture
                        self.possible_movements[i].append([pos[0]+1, pos[1]+x])
                if pos[0]-1>=0:
                    if (self.board[pos[0]-1][pos[1]+x][0] != ''
                       and self.board[pos[0]-1][pos[1]+x][1] != self.to_move
                       ):
                        # left-hand side capture
                        self.possible_movements[i].append([pos[0]-1, pos[1]+x])

            if pos[1]+2*x < 8 and pos[1]+2*x >= 0:
                if (
                    self.board[pos[0]][pos[1]+2*x][0] == ''
                    and pos[1] == abs((7/2 * x) - 5/2)
                   ):
                    # two steps forward
                    self.possible_movements[i].append([pos[0], pos[1]+2*x])


    def rook_movement(self):
        p_pos = self.pieces_positions[self.to_move]['R']  # Rook's positions
        self.possible_movements = []

        for i, pos in enumerate(p_pos):
            self.possible_movements.append([])
            ix = 1

            # Possible positions increasing and decreasing rows
            for j in [1, -1]:
                ix = j
                while (pos[1] + ix) < 8 and (pos[1] + ix) >= 0:
                    if (
                        self.board[pos[0]][pos[1]+ix][0] == ''
                        or self.board[pos[0]][pos[1]+ix][1] != self.to_move
                        ):
                        self.possible_movements[i].append([pos[0], pos[1]+ix])
                    if self.board[pos[0]][pos[1]+ix][0] != '':
                        break


                    ix = ix + j


            # Possible positions increasing and decreasing columns
            for j in [1, -1]:
                ix = j
                while (pos[0] + ix) < 8 and (pos[0] + ix) >= 0:
                    if (
                        self.board[pos[0]+ix][pos[1]][0] == ''
                        or self.board[pos[0]+ix][pos[1]][1] != self.to_move
                        ):
                        self.possible_movements[i].append([pos[0]+ix, pos[1]])
                    if self.board[pos[0]+ix][pos[1]][0] != '':
                        break


                    ix = ix + j


    def bishop_movement(self):
        p_pos = self.pieces_positions[self.to_move]['B']  # Bishop's positions
        self.possible_movements = []

        for i, pos in enumerate(p_pos):
            self.possible_movements.append([])
            ix = 1

            # Possible positions increasing and decreasing \
            for j in [1, -1]:
                ix = j
                while (
                       (pos[1] + ix) < 8 and (pos[1] + ix) >= 0
                       and (pos[0] - ix) < 8 and (pos[0] - ix) >= 0
                      ):
                    if (
                        self.board[pos[0]-ix][pos[1]+ix][0] == ''
                        or self.board[pos[0]-ix][pos[1]+ix][1] != self.to_move
                        ):
                        self.possible_movements[i].append([pos[0]-ix,
                                                           pos[1]+ix])
                    if self.board[pos[0]-ix][pos[1]+ix][0] != '':
                        break


                    ix = ix + j


            # Possible positions increasing and decreasing /
            for j in [1, -1]:
                ix = j
                while (
                       (pos[1] + ix) < 8 and (pos[1] + ix) >= 0
                       and (pos[0] + ix) < 8 and (pos[0] + ix) >= 0
                      ):
                    if (
                        self.board[pos[0]+ix][pos[1]+ix][0] == ''
                        or self.board[pos[0]+ix][pos[1]+ix][1] != self.to_move
                        ):
                        self.possible_movements[i].append([pos[0]+ix,
                                                           pos[1]+ix])
                    if self.board[pos[0]+ix][pos[1]+ix][0] != '':
                        break


                    ix = ix + j


    def queen_movement(self):
            p_pos = self.pieces_positions[self.to_move]['Q']  # Queen's positions
            self.possible_movements = []

            for i, pos in enumerate(p_pos):
                self.possible_movements.append([])
                ix = 1

                # Possible positions increasing and decreasing rows
                for j in [1, -1]:
                    ix = j
                    while (pos[1] + ix) < 8 and (pos[1] + ix) >= 0:
                        if (
                            self.board[pos[0]][pos[1]+ix][0] == ''
                            or self.board[pos[0]][pos[1]+ix][1] != self.to_move
                            ):
                            self.possible_movements[i].append([pos[0], pos[1]+ix])
                        if self.board[pos[0]][pos[1]+ix][0] != '':
                            break


                        ix = ix + j


                # Possible positions increasing and decreasing columns
                for j in [1, -1]:
                    ix = j
                    while (pos[0] + ix) < 8 and (pos[0] + ix) >= 0:
                        if (
                            self.board[pos[0]+ix][pos[1]][0] == ''
                            or self.board[pos[0]+ix][pos[1]][1] != self.to_move
                            ):
                            self.possible_movements[i].append([pos[0]+ix, pos[1]])
                        if self.board[pos[0]+ix][pos[1]][0] != '':
                            break


                        ix = ix + j


                # Possible positions increasing and decreasing \
                for j in [1, -1]:
                    ix = j
                    while (
                           (pos[1] + ix) < 8 and (pos[1] + ix) >= 0
                           and (pos[0] - ix) < 8 and (pos[0] - ix) >= 0
                          ):
                        if (
                            self.board[pos[0]-ix][pos[1]+ix][0] == ''
                            or self.board[pos[0]-ix][pos[1]+ix][1] != self.to_move
                            ):
                            self.possible_movements[i].append([pos[0]-ix,
                                                               pos[1]+ix])
                        if self.board[pos[0]-ix][pos[1]+ix][0] != '':
                            break


                        ix = ix + j


                # Possible positions increasing and decreasing /
                for j in [1, -1]:
                    ix = j
                    while (
                           (pos[1] + ix) < 8 and (pos[1] + ix) >= 0
                           and (pos[0] + ix) < 8 and (pos[0] + ix) >= 0
                          ):
                        if (
                            self.board[pos[0]+ix][pos[1]+ix][0] == ''
                            or self.board[pos[0]+ix][pos[1]+ix][1] != self.to_move
                            ):
                            self.possible_movements[i].append([pos[0]+ix,
                                                               pos[1]+ix])
                        if self.board[pos[0]+ix][pos[1]+ix][0] != '':
                            break


                        ix = ix + j


    def king_movement(self):
            p_pos = self.pieces_positions[self.to_move]['K']  # King's positions
            self.possible_movements = []

            for i, pos in enumerate(p_pos):
                self.possible_movements.append([])

                for ix in [-1, 0, 1]:
                    for jx in [-1, 0, 1]:
                        if (
                            pos[0]+ix < 8 and pos[0]+ix >= 0
                            and pos[1]+jx < 8 and pos[1]+jx >= 0
                            and [ix, jx] != [0, 0]
                            # Checking checks would be here
                           ):
                            if (
                                self.board[pos[0]+ix][pos[1]+jx][0] == ''
                                or self.board[pos[0]+ix][pos[1]+jx][1] != self.to_move
                               ):
                                self.possible_movements[i].append([pos[0]+ix,
                                                                   pos[1]+jx])


    def knight_movement(self):
            p_pos = self.pieces_positions[self.to_move]['N']  # Knight's positions
            self.possible_movements = []

            for i, pos in enumerate(p_pos):
                self.possible_movements.append([])

                for ix in [1, -1, 2, -2]:
                    for jx in [3-abs(ix), abs(ix)-3]:
                        if (
                            pos[0]+ix < 8 and pos[0]+ix >= 0
                            and pos[1]+jx < 8 and pos[1]+jx >= 0
                           ):
                            if (
                                self.board[pos[0]+ix][pos[1]+jx][0] == ''
                                or self.board[pos[0]+ix][pos[1]+jx][1] != self.to_move
                               ):
                                self.possible_movements[i].append([pos[0]+ix,
                                                                   pos[1]+jx])




game1 = chess()
game1.play()
print(game1.pieces_positions)

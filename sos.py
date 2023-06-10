import constants

class SOSEnv:   # Game environment
    def start(self):    # Starting the game, creates and returnes board array
        self.board = self.createboard()
        self.turn = 0
        return self.board

    def createboard(self):
        board = []
        for y in range(6):
            row = []
            for x in range(6):
                row.append((""))
            board.append(row)
        return board

    def getLegalMoves(self, state): # Getting list of empty squares which can be playable, and returning the list
        legal_moves = []
        for x, row in enumerate(state):
            for y, square in enumerate(row):
                if square == "":
                    legal_moves.append(((x, y)))
        return legal_moves

    def move(self, square, piece):
        square = constants.ACTION_LIST[square] # Getting square in (x,y) from index list
                                               # Example: player input square is 9, then square = (1,3)

        self.board[square[0]][square[1]] = piece    # Changing the moved squre in board to moved piece

        score = self.CheckScore(square, piece)  # Checking move score
        done = self.gameEnd()   # Checking if game done
        
        if score == 0:  # If player doesn't get any scores, changing the turn
            if self.turn == 0:
                self.turn = 1
            else:
                self.turn = 0

        reward = score*constants.SCORE_REWARD   # Getting move's reward by multiplying move score and SCORE_REWARD parameter

        return self.board, score, reward, done, self.turn

    def gameEnd(self):  # Checking if game done. If done, returns True else False
        for row in self.board:
            for square in row:
                if square == "":
                    return False
        return True
    
    def CheckScore(self, square, piece):    # Checking scores on columns, rows, diagonals
        score = 0
        check_list = [] # Creating a list to append squares variants to be checked

        # Checking on columns
        flipedBoard = []
        for x in range(6):  # Flipping the board 90 degree in order to check score from columns easily
            subList = []
            for i in self.board:
                subList.append(i[x])
            flipedBoard.append(subList)
        column = flipedBoard[square[1]]
        column_check = []
        for i in range(-2,3):   # Finding all 3 squares variants on columns that can be scored, and appending to column check list
            try:
                if square[0]+i >= 0:
                    column_check.append(column[square[0]+i])
                else:
                    column_check.append("")
            except Exception:
                column_check.append("")
        check_list.append(column_check) # Appending column check list to check list

        # Checking on rows. (Same as checking on columns except flipping board)
        row = self.board[square[0]]
        row_check = []
        for i in range(-2,3):
            try:
                if square[1]+i >= 0:
                    row_check.append(row[square[1]+i])
                else:
                    row_check.append("")
            except Exception:
                row_check.append("")
        check_list.append(row_check)

        # Checking on diagnals
        diagnal1_check = []
        for i in range(-2,3):
            try:
                if square[0]+i >= 0 and square[1]+i >= 0:
                    diagnal1_check.append(self.board[square[0]+i][square[1]+i])
                else:
                    diagnal1_check.append("")
            except Exception:
                diagnal1_check.append("")
        check_list.append(diagnal1_check)

        diagnal2_check = []
        for i in range(-2,3):
            try:
                if square[0]+i >= 0 and square[1]-i >= 0:
                    diagnal2_check.append(self.board[square[0]+i][square[1]-i])
                else:
                    diagnal2_check.append("")
            except Exception:
                diagnal2_check.append("")
        check_list.append(diagnal2_check)

        ### Checking is there scored variants in check list
        for i in check_list:
            if piece == "S":
                if i[0]=="S" and i[1]=="O":
                    score += 1
                if i[3]=="O" and i[4]=="S":
                    score += 1
            if piece == "O":
                if i[1]=="S" and i[3]=="S":
                    score += 1
        return score    # Returning the score

    def getMask(self, state=None):  # Masking the legal moves to set model's q values easily
                                    # Returning a list of moves if move is legal move = 1, else 0
        if state == None:
            state = self.board
        legalMoves = self.getLegalMoves(state)
        mask = []
        for move in constants.ACTION_LIST:
            if not move in legalMoves:
                mask.append(0)
            else:
                mask.append(1)
        return mask

    def isLegal(self, move):    # Checking is a move legal in masked moves. If legal returnes True else False
        if self.getMask()[move] == 1:
            return  True
        return False

    def __repr__(self): # String representation of our model is current board.
                        # If you want to display the board in the console, class object can directly print
        string = ""
        for i in self.board:
            for x in i:
                if x == "S":
                    string += 'S '
                elif x == "O":
                    string += 'O ' 
                else:
                    string += '- ' 
            string += '\n'
        return string
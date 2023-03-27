import chess
import random as rand

def randMove():
    board = chess.Board()
    whiteForAI = True
    playerColor = input("Do you want to play as (w)hite or (b)lack? ")
    if playerColor == "w":
        whiteForAI = False
    moveNum = 1
    done = False
    while not done:
        if whiteForAI:
            move = getRandLegalMove(board)
            if playMove(board, move, True):
                break
        playerMove = input("Type in desired move to play: ")
        if playMove(board, playerMove, False):
            break
        if not whiteForAI:
            print(board, end="\n\n")
            move = getRandLegalMove(board)
            if playMove(board, move, True):
                break
        print("Move", str(moveNum), "complete\n")
        moveNum += 1

def playMove(board, sanMove, cpuMove):
    board.push_san(sanMove)
    playerStr = "Player"
    if cpuMove:
        playerStr = "CPU"
    print(playerStr, "plays", sanMove + "\n")
    print(board, end="\n\n")
    outcome = board.outcome()
    done = False
    if outcome != None:
        done = True
        if outcome.winner != None:
            winner = "White"
            if outcome.winner == chess.BLACK:
                winner = "Black"
            print(str(winner), "wins")
        else:
            draw = "stalemate"
            if outcome.termination == Termination.INSUFFICIENT_MATERIAL:
                draw = "insufficient material"
            print("Draw by", draw)
    return done

def getRandLegalMove(board):
    choice = rand.randrange(board.legal_moves.count())
    ind = 0
    allLegalMoves = list(board.legal_moves)
    move = board.san(allLegalMoves[choice])
    return move

randMove()


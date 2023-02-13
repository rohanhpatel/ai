import chess

def main():
    board = chess.Board()
    legalMoves = list()
    for move in board.legal_moves:
        legalMoves.append(board.san(move))
    print(legalMoves)
    print(board)
    board.push_san("e4")
    print(board)

main()

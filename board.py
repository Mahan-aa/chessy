import pygame
import chess
import sys
import os


pygame.init()
board = chess.Board()


WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT = (255, 255, 0)
MOVE_DOT = (50, 50, 50)
RED= (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess UI")


PIECES = {}
for color in ['w', 'b']:
    for name in ['p', 'r', 'n', 'b', 'q', 'k']:
        key = color + name
        img_path = os.path.join("assets", f"{key}.svg")
        if os.path.exists(img_path):
            image = pygame.image.load(img_path)
            PIECES[key] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
        else:
            print(f"Missing image: {img_path}")


def draw_board(selected=None, moves=[]):
    for row in range(8):
        for col in range(8):
            square_color = LIGHT if (row + col) % 2 == 0 else DARK
            square = chess.square(col, 7 - row)


            if selected == square:
                square_color = HIGHLIGHT

            pygame.draw.rect(screen, square_color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



            if square in moves:
                if board.piece_at(square):
                    pygame.draw.rect(screen,RED , (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.circle(screen, MOVE_DOT, center, 10)

def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            img = PIECES[
                ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().lower()
            ]
            screen.blit(img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_square_under_mouse():
    mx, my = pygame.mouse.get_pos()
    col = mx // SQUARE_SIZE
    row = my // SQUARE_SIZE
    return chess.square(col, 7 - row)

dic={1:"White",0:"Black"}
selected_square = None
highlight_moves = []

while True:
    draw_board(selected_square, highlight_moves)
    draw_pieces()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if board.legal_moves.count()==0:
            print(f"{dic[not board.turn]} chek mate's {dic[board.turn]}")
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            square = get_square_under_mouse()

            if selected_square is None:
                piece = board.piece_at(square)
                if piece and piece.color == board.turn:
                    selected_square = square
                    highlight_moves = [m.to_square for m in board.legal_moves if m.from_square == square]
            else:
                is_pawn = board.piece_at(selected_square).piece_type == chess.PAWN
                rank = chess.square_rank(square)

                if is_pawn and (rank == 0 or rank == 7):
                    move = chess.Move(selected_square, square, promotion=chess.QUEEN)
                else:
                    move = chess.Move(selected_square, square)

                if move in board.legal_moves:
                    board.push(move)

                selected_square = None
                highlight_moves = []

from Chessboard_Detection.Difference_Detection import generate_moves
from stockfish import Stockfish
import cv2
import keyboard

ENGINE_PATH = 'C:/Users/Tobias/Chess_Engines/stockfish_15/stockfish_15_x64_avx2'
THREADS = 8
DEPTH = 20
HASH = 4069 # allows stockfish to use 4069MB of ram (amt has to be a power of 2 here 4069 = 2^12)
PATH = 'C:/Users/Tobias/PycharmProjects/robotic-arm-for-chess/src/Chessboard_Detection/imgs'
STARTPOS = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

stream = cv2.VideoCapture('http://192.168.178.28:8080/video')

stockfish = Stockfish(path=ENGINE_PATH, depth=DEPTH, parameters={"Threads": THREADS, "Hash": HASH})
stockfish.set_fen_position(STARTPOS)

def main():
    
    input()
    print('Key Pressed')
    _, curr_frame = stream.read()
    #curr_frame = cv2.rotate(curr_frame, cv2.ROTATE_90_CLOCKWISE)
    curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY)
    curr_frame = cv2.resize(curr_frame, (720, 720))
    curr_frame[45:685,45:685] # specify actual board area
    
    while True:
        
        # Opponent makes move #
        _, fol_frame = stream.read()
        
        if keyboard.is_pressed(' '): # Opponent has made their move
            fol_frame = cv2.cvtColor(fol_frame, cv2.COLOR_RGB2GRAY)
            fol_frame = cv2.resize(fol_frame, (720, 720))
            #fol_frame = cv2.rotate(fol_frame, cv2.ROTATE_90_CLOCKWISE)
            fol_frame = fol_frame[45:685,45:685] 
            
            diff = cv2.absdiff(curr_frame, fol_frame)

            moves = generate_moves(diff) # find the move that the opponent made
            if len(moves) != 2:
                print('Couldnt detect a move, shutting down')
                return
            
            for move in moves:
                if stockfish.is_move_correct(move):
                    stockfish.make_moves_from_current_position([move]) # make the move on the virtual board
                    print(f'made move: {move}')
                    break
            
            eval = stockfish.get_evaluation()
            if eval['type'] == 'mate' and eval['value'] == 0: # if the game is over, terminate
                print('You won!')
                return # stockfish lost     

            stockfish_move = stockfish.get_best_move()
            stockfish.make_moves_from_current_position([stockfish_move]) # make best move on virtual board
            
            ######## Visualization bcs the arm isnt integrated yet ##############
            print(stockfish.get_board_visual())
            #####################################################################
            
            # robotic arm makes move on real board, user presses space when its done
        
            while True:
               _, curr_frame = stream.read()
               if keyboard.is_pressed(' '):
                   break

            curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY)
            curr_frame = cv2.resize(curr_frame, (720, 720))
            #curr_frame = cv2.rotate(curr_frame, cv2.ROTATE_90_CLOCKWISE)
            curr_frame = curr_frame[45:685,45:685]

        
if __name__ == '__main__':
    main()
    

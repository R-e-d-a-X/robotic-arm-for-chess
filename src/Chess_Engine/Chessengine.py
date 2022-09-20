from stockfish import Stockfish

ENGINE_PATH = 'C:/Users/Tobias/Chess_Engines/stockfish_15/stockfish_15_x64_avx2'
THREADS = 8
DEPTH = 20
HASH = 4069 # allows stockfish to use 4069MB of ram (amt has to be a power of 2 here 4069 = 2^12)
STARTPOS = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

'''
For eval:
            Value > 0: advantage white
            Value = 0: no advantage
            Value < 0: advantage black
            
            Type = cp (centipawns): divide by 100 to get decimal value  
            Type = mate: number x means there is checkmate in x moves (pos x = mate for white; neg x = mate for black)
'''

# Engine initialization and reset of the board
stockfish = Stockfish(path=ENGINE_PATH, depth=DEPTH, parameters={"Threads": THREADS, "Hash": HASH})
stockfish.set_fen_position(STARTPOS)

def get_nicer_eval(eval: dict): 
    res = ""
    if eval['type'] == 'cp':
        if eval['value'] >= 0:
            advantage = 'white'
        elif eval['value'] < 0:
            advantage = 'black'
        res = abs(eval['value']) / 100
        return f'+{res:.2f} for {advantage}'
    elif eval['type'] == 'mate':
        val = eval['value']
        if val >= 0:
            return f'M{val} for white'
        else:
            return f'M{val} for black'
    else:
        raise ValueError
    
# temporary interface since the computervision part is not done yet
if __name__ == '__main__':
    print('Move input format: algebraic f.e. e2e4 for moving a piece from e2 to e4')
    print('You play as white')
    print(stockfish.get_board_visual())
    while True:
        move = [input('Your move: ')]
        if stockfish.is_move_correct(move[0]):
            stockfish.make_moves_from_current_position(move)
            print('calculating')
            eval = stockfish.get_evaluation()
            if eval['type'] == 'mate' and eval['value'] == 0:
                print('You have won')
                break
            
            stockfish_move = stockfish.get_best_move()
            stockfish.make_moves_from_current_position([stockfish_move])
            
            print(stockfish.get_board_visual())
            
            print(f"Stockfish plays: {stockfish_move}")
            eval = stockfish.get_evaluation()
            if eval['type'] == 'mate' and eval['value'] == 0:
                print('You have lost')
                break
        else:
            print('That is not a legal move')

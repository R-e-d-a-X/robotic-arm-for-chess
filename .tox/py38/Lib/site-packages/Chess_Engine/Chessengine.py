from stockfish import Stockfish

ENGINE_PATH = 'C:/Users/Tobias/Chess_Engines/stockfish_15/stockfish_15_x64_avx2'
THREADS = 8
DEPTH = 32 
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
    
mate_in_one = '7k/8/6R1/5R2/8/2K5/8/8 w - - 0 69'    
mate_in_three = '7k/8/5R2/5R2/8/2K5/8/8 w - - 0 69'  

stockfish.set_fen_position(mate_in_three)
print(stockfish.get_board_visual())
    
res_eval = stockfish.get_evaluation()    

print(f'Default: {res_eval}')
print(f'Custom: {get_nicer_eval(res_eval)}')
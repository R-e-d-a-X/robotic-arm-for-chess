import cv2
import numpy as np

WIDTH = HEIGHT = 720
SQUARE = 80
ROWS = ['8', '7', '6', '5', '4', '3', '2', '1']
COLS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
PATH = 'C:/Users/Tobias/PycharmProjects/robotic-arm-for-chess/src/Chessboard_Detection/imgs'
CHANGE_THRESH = 7.75
MOVE_TYPE = { 2 : 'normal', 3 : 'en passent', 4 : 'castle' }

im1 = cv2.resize(cv2.imread(f'{PATH}/1.jpg', 0), (720, 720))[45:685,45:685]
im2 = cv2.resize(cv2.imread(f'{PATH}/2.jpg', 0), (720, 720))[45:685,45:685]
im3 = cv2.resize(cv2.imread(f'{PATH}/3.jpg', 0), (720, 720))[45:685,45:685]
im4 = cv2.resize(cv2.imread(f'{PATH}/4.jpg', 0), (720, 720))[45:685,45:685]

sobel1 = cv2.Sobel(src=im1, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
_, thresh1 = cv2.threshold(sobel1, 90, 255, cv2.THRESH_BINARY)

sobel2 = cv2.Sobel(src=im2, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
_, thresh2 = cv2.threshold(sobel2, 90, 255, cv2.THRESH_BINARY)

sobel3 = cv2.Sobel(src=im3, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
_, thresh3 = cv2.threshold(sobel3, 90, 255, cv2.THRESH_BINARY)

sobel4 = cv2.Sobel(src=im4, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
_, thresh4 = cv2.threshold(sobel4, 90, 255, cv2.THRESH_BINARY)

diff = cv2.absdiff(im1, im2)

#cv2.imshow('thresh1', thresh3)
#cv2.waitKey(0)
#cv2.imshow('thresh2', thresh4)
#cv2.waitKey(0)
#cv2.imshow('diff', diff)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

take1 = cv2.resize(cv2.imread(f'{PATH}/take1.jpg', 0), (720, 720))[45:685,45:685]
take2 = cv2.resize(cv2.imread(f'{PATH}/take2.jpg', 0), (720, 720))[45:685,45:685]
castle1 = cv2.resize(cv2.imread(f'{PATH}/castle1.jpg', 0), (720, 720))[45:685,45:685]
castle2 = cv2.resize(cv2.imread(f'{PATH}/castle2.jpg', 0), (720, 720))[45:685,45:685]

sobelt1 = cv2.Sobel(src=take1, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
_, thresht1 = cv2.threshold(sobelt1, 90, 255, cv2.THRESH_BINARY)

sobelt2 = cv2.Sobel(src=take2, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
_, thresht2 = cv2.threshold(sobelt2, 90, 255, cv2.THRESH_BINARY)

sobelc1 = cv2.Sobel(src=castle1, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
_, threshc1 = cv2.threshold(sobelc1, 90, 255, cv2.THRESH_BINARY)

sobelc2 = cv2.Sobel(src=castle2, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
_, threshc2 = cv2.threshold(sobelc2, 90, 255, cv2.THRESH_BINARY)

difft = cv2.absdiff(take1, take2)
diffc = cv2.absdiff(castle1, castle2)

#cv2.imshow('thresh1', thresh1)
#cv2.waitKey(0)
#cv2.imshow('thresh2', thresh2)
#cv2.waitKey(0)
#cv2.imshow('diff', diff)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

def generate_moves(diff):
    squares = __find_different_squares(diff)
    if squares[0] == MOVE_TYPE[2]: # normal move 
        i = 1
        j = 2   
    elif squares[0] == MOVE_TYPE[3]: # en passent
        row1 = int(squares[1][-1])
        row2 = int(squares[2][-1])
        row3 = int(squares[3][-1])
        i = __get_unique(row1, row2, row3)
        
        col1 = squares[1][0]
        col2 = squares[2][0]
        col3 = squares[3][0]
        j = __get_unique(col1, col2, col3)
            
    elif squares[0] == MOVE_TYPE[4]: # castle
        if 'e1' in squares:
            i = squares.index('e1')
            if 'g1' in squares:
                j = squares.index('g1')
            else:
                j = squares.index('c1')
        else:
            i = squares.index('e8')
            if 'g8' in squares:
                j = squares.index('g8')
            else:
                j = squares.index('c8')
    else:
        raise ValueError() 
    
    return [f'{squares[i]}{squares[j]}', f'{squares[j]}{squares[i]}']

# function that finds the two squares with the most changes from difference image
def __find_different_squares(diff):
    count = __get_square_change_count(diff)
    squares = [''] * (count + 1)
    squares[0] = MOVE_TYPE[count]
    highest_means = np.zeros(count + 1)
    highest_means[0] = 10000
    
    for i in range(8): # rows
        for j in range(8): # cols
            square = diff[i*SQUARE:(i+1)*SQUARE, j*SQUARE:(j+1)*SQUARE]
            mean = np.mean(square) 
            if mean > np.min(highest_means):
                squares[np.argmin(highest_means)] = f'{COLS[j]}{ROWS[i]}'
                highest_means[np.argmin(highest_means)] = mean
    
    return squares

def __get_square_change_count(diff):
    count = 0
    for i in range(8): # rows
            for j in range(8): # cols
                square = diff[i*SQUARE:(i+1)*SQUARE, j*SQUARE:(j+1)*SQUARE]
                mean = np.mean(square) 
                if mean > CHANGE_THRESH:
                    count += 1
    return count

def __get_unique(a, b, c):
    if a == b:
        return 3
    else:
        if a == c:
           return 2
        return 1 

if __name__ == '__main__':
    curr_img = im1
    follow_imgs = [im2, im3, im4]
    for im in follow_imgs:
        
        diff = cv2.absdiff(curr_img, im)
        moves = generate_moves(diff)
        print(f'1: {moves[0]}  2:{moves[1]}')
        curr_img = im

    moves = generate_moves(difft)
    print(f'1: {moves[0]}  2:{moves[1]}')
    moves = generate_moves(diffc)
    print(f'1: {moves[0]}  2:{moves[1]}')

    
            
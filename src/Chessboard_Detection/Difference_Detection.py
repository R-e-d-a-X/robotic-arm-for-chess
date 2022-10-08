import cv2
import numpy as np

WIDTH = HEIGHT = 720
ROWS = ['8', '7', '6', '5', '4', '3', '2', '1']
COLS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


im1 = cv2.imread('C:/Users/Tobias/PycharmProjects/robotic-arm-for-chess/src/Chessboard_Detection/imgs/1.jpeg', 0)
im2 = cv2.imread('C:/Users/Tobias/PycharmProjects/robotic-arm-for-chess/src/Chessboard_Detection/imgs/2.jpeg', 0)

diff = cv2.subtract(im1, im2)

cv2.imshow('Difference', diff)
cv2.waitKey(0)
cv2.destroyAllWindows()

# function that finds the two squares with the most pixel changes from difference image
def find_different_squares(img):
    squares = ['', '']
    pixel_counts = np.zeros(2)
    for i in range(8): # rows
        for j in range(8): # cols
            square = img[i*90:(i+1)*90, j*90:(j+1)*90] 
            pixel_count = square[square > 0].shape[0] # number of pixel that changed in the images
            if pixel_count > np.min(pixel_counts):
                min_index = np.argmin(pixel_counts)
                squares[min_index] = f'{COLS[j]}{ROWS[i]}'
                pixel_counts[min_index] = pixel_count
    return squares

def generate_possible_moves(img):
    squares = find_different_squares(img)
    return [f'{squares[0]}{squares[1]}', f'{squares[1]}{squares[0]}']

for i, move in enumerate(generate_possible_moves(diff)):
    print(f'move {i}:\t{move}')
    
            
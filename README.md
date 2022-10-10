## Overview
![Tests](https://github.com/R-e-d-a-X/robotic-arm-for-chess/actions/workflows/tests.yml/badge.svg)

This project contains the source code for a robotic arm with integrated chess engine and computer vision to detect a real chess board and play. 

## Chess engine

The chess engine that is used is [stockfish15](https://stockfishchess.org), which is a free chess engine that is distributed under the [GNU General Public License version 3](https://github.com/R-e-d-a-X/robotic-arm-for-chess/blob/master/LICENSE). If you are interested in specific details, you can checkout the [official stockfish github](https://github.com/official-stockfish/Stockfish).

## Board detection

The board detection takes a snapshot of the current board situation before and after the opponent has made a move. The **absolut difference** of these to snapshots then gets calculated. Areas that pass a certain threshhold of change are classified as squares that changed. The amount of squares that changed is determined by the type of move that has been made.

| Amount | Movetype |
| ----------- | ----------- |
| 2 | normal move |
| 3 | en passent | 
| 4 | castle |

Depending on what type of move has been made, the correct engine instructions are generated from the squares that changed. The engine then calculates the best move for the given board position and it is translated into path instructions for the robotic arm, which then performs the given move on the real board.

## Robotic arm specs

*NOT YET ADDED*
# Exapunks Automation

This repository solves Exapunk's Solitaire minigame, ПАСЬЯНС. This repository is useable, but only with specific display conditions (more on that below under Usage)

# How it works
`main.py` contains the `Board` class, which is responsible for reading your screen and creating a `Game` object from it. The `Game` object is a programatic version of the game board that contains an array of `Rank` objects. Ranks are containers for each column in the game, but instead of containing an array of `Card` objects, they contain a list of `Stack` objects, which only know their front card, back card, and their length. When `Board` generates `Game`, it combines all pre-existing stacks that are able to merge (that is to say: Stacks in the same Rank that can be combined, are combined). `Game.solve` checks the front stack in each rank against all other front stacks, seeing if the back card and front card are compatible. If they are, that particular move is added to the state space to further investigate.

The solver is breadth-first and it finds **all** possible solutions for the particular puzzle. `Game.move_stack` is a `collections.deque` that stores each possible set of moves. Every `Game.iteration`, a list of consecutive moves is popped off of the move stack and checked for child moves. If a child move is found, it's appended to the end of a copy of the move list, then the new move list is appended to the back of the move stack. If there are no moves left, we check if the board we're looking at is a winning board. If it is, append that particular move list to `Game.winning_moves`. Win or not, the move stack shrinks until it's empty and we know we've searched all possible states.

# Example of solution
![Gif 0](https://i.imgur.com/mjwmnwt.gif)
![Gif 1](https://i.imgur.com/ToIFprx.mp4)

# Usage & Installation
This code wasn't really made with other people using it mind. That said, if your monitor resolution is 1920x1080 and Exapunks is full screen, this should work for you. You'll just need to fork this repository and run `main.py`. There are some things you can change to tailor this for yourself.

This project uses Pillow and pyautogui
```
python -m pip install Pillow
python -m pip install pyautogui
```

Under `main.py`'s `main` function, there is a function call for `board.play_games(n)` or `board.play_quick_games(n)`. A quick game doesn't look at moves that involve moving cards to the hand and it generally solves the board on the order of ~2 seconds. There is no guarentee that the game will be possible without the hand (maybe ~50% to 60% are completable without it?), but it's very fast and it'll redeal the board until it completes `n` games. A normal game looks at the hand as a last resort and it's success rate is 100%, but it takes maybe ~20 seconds to solve and it'll keep playing until it reaches `n` games completed.

If your screen dimensions aren't 1920x1080, it's ***technically*** possible to modify this code to work for you, but it'll be a pain. Your game will still need to be fullscreen. You'll need to recreate all of the images in `res/` and edit the constants in the `Board` class. Here are some steps to help you out:
1. Recreate the images in `res/`. These images are special - their names matter (so keep red 10s as 0R, for example) and they're square and equidistant. Recreate these images and make sure you don't get any pixels from the face cards in their images (I noticed the texture for the Ace & Queen get near the suit icon, so make sure those aren't in them). Remember - it needs to be the same square relative to the card for all these images.
2. Measure the distance between the squares both horizontally and vertically, along with the distance between the top row of squares and the top of your screen, and the left column and the left of your screen. Also, you'll need the size of the square. These are the `Board.square_size`, `Board.vertical_spacing_with_square`, `Board.horizontal_spacing_with_square`, `Board.left_offset`, and `Board.top_offset`.
3. Measure a card's height and width for `Board.card_width` and `Board.card_height`
4. Get coordinates for the newgame button for `newgame_x` and `newgame_y`
5. Calculate `hand_x` and `hand_y`. `hand_x` is the middle of the hand horizontally and `hand_y` is maybe 10% of the height from the top (it's not terribly sensitive).

I can't guarentee this will work for you, but there are no magic numbers and it *should* work.

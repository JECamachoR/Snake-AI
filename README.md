# Snake-AI
Hi! With this project I'm trying to learn about the evolution of neural networks. I know there are ways of making a perfect snake AI with some mathematical models, but that is not the main idea here. 

## snake.py
snake.py is the place where the objects Game, Snake, Fruit and Field. These will be used in all other modules. The Game object serves a the base object for the AITrainingGame, AIGame and HumanGame objects. It has one Snake, one Field and one Fruit generated at random in the field's available places.

## play.py
This scripts allows the user to play snake.

#### Usage
```bash
python play.py NGRIDS ROWS COLS
```
NGRIDS is 1 if the user just wants to play game, and two if they want to also see what the AI "see".
ROWS and COLS are the number of rows and columns to have in the field's grid. (recommended above 9 9)

## train.py
This scripts allows the user to train a snake with a given name.

#### Usage
```bash
python train.py GENOME_NAME ROWS COLS
```
## watch.py
This scripts allows the user see how a genome turns out in action.

#### Usage
```bash
python watch.py GENOME_NAME ROWS COLS
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

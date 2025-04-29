# Monte Carlo Simulator

## Metadata
**Author:** Cameron Her  
**Project:** Monte Carlo Simulator

## Synopsis:

This package contains the modules necessary to perform a Monte Carlo simulation. This simulation allows users to define the faces for the dice, alter the weights of each face, simulate games with a custom number of rolls and dice, and analyze the results of the game.

### Installation

```bash
pip install .
```

### Example Usage

```python
import numpy as np
from montecarlo import MonteCarlo
from montecarlo import Die, Game, Analyzer

# Example 1. Create dice
faces = np.array([1, 2, 3, 4, 5, 6])
die = Die(faces)
die.change_weight('1', 10.0)

# 2. Play a game
game = Game([die, die, die])
game.play(5)
results = game.show(form='wide')

# 3. Analyze the game
analyzer = Analyzer(game)
jackpot_count = analyzer.jackpot()
face_counts = analyzer.face_counts_per_roll()
combo_counts = analyzer.combo_count()
permutation_counts = analyzer.permutation_count()
```

## API Description

### Class: `Die`

A die has 𝑁 sides, or “faces”, and  𝑊 weights, and can be rolled to select a face.

#### `def __init__(self, faces):`

PURPOSE: This method initializes the Die object and saves both faces and weights in a private data frame with faces in the index.  
        
INPUT:This method takes a NumPy array of faces as an argument. The array’s data type dtype may be strings or numbers, but the array’s values must be distinct.
        
OUTPUT: None.

#### `def change_weight(self, face, new_weight):`

PURPOSE: This method changes the weight of a single side. 
        
INPUT: Takes two arguments: the face value to be changed and the new weight.
        
OUTPUT: None.

#### `def roll_dice(self, n_rolls=1):`

PURPOSE: This method rolls the die/dice using random sample with replacement, from the private die data frame, that applies the weights.
        
INPUT: a parameter of how many times the die is to be rolled; defaults to  1.
        
OUTPUT: pd.Series(results), a series with the results of the dice roll.


#### `def show(self):`

PURPOSE: This method shows the die’s current state.
        
INPUT: None.

OUTPUT: Returns a copy of the private die data frame.



### Class: `Game`

#### `def __init__(self, dice_list):`

PURPOSE: This method initializes the Game object with a list of dice objects. 
        
INPUT: This method a single parameter, a list of already instantiated similar dice.
        
OUTPUT: None.
        
#### `def play(self, n_rolls):`

PURPOSE: This method simulate rolling a number of similar dice a specific number of times.
        
INPUT: This method takes an integer parameter to specify how many times the dice should be rolled.
        
OUTPUT: This method saves the result of the play to a private data frame.

#### `def show(self, form='wide'):`

PURPOSE: This method shows the user the results of the most recent play.  
        
INPUT: This method takes a parameter to return the data frame in narrow or wide form which defaults to wide form.
        
OUTPUT: This method outputs pandas.DataFrame of the results from the game.
        • The wide format will have the roll number as a named index, columns for each die number and the face rolled in that instance in each cell.
        • The narrow form will have a MultiIndex, comprising the roll number and the die number (in that order), and a single column with the outcomes.
        
        
       
### Class: `Analyzer`

#### `def __init__(self, game):`

PURPOSE: This method initializes the Analyzer object.
        
INPUT: This method takes a game object as its input parameter.
        
OUTPUT: None.

#### `def jackpot(self):`

PURPOSE: This method computes how many times the game resulted in a jackpot. 
        
INPUT: None
        
OUTPUT: This method returns an integer for the number of jackpots.

#### `def face_counts_per_roll(self):`

PURPOSE: This method computes how many times a given face is rolled in each event.
        
INPUT: None
        
OUTPUT: This method returns a data frame of results.

#### `def combo_count(self):`

PURPOSE: This method computes the distinct combinations of faces rolled, along with their counts.
        
INPUT: None
        
OUTPUT: This method returns a data frame of results which has a MultiIndex of distinct combinations and a column for the associated counts.

#### `def permutation_count(self):`

PURPOSE: This method computes the distinct permutations of faces rolled, along with their counts.
        
INPUT: None
        
OUTPUT: This method returns a data frame of results which has a MultiIndex of distinct permutations and a column for the associated counts.

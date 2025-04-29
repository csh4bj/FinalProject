import numpy as np
import pandas as pd

class Die:
    """
    A die has 𝑁 sides, or “faces”, and  𝑊 weights, and can be rolled to select a face.
    
    Each side contains a unique symbol. Symbols may be all alphabetic or all numeric.
    
    𝑊 defaults to  1.0 for each face but can be changed after the object is created.
    The weights are just positive numbers (integers or floats, including  0), not a normalized probability distribution.
    
    This Die class has 4 methods: 
    • An initializer.
    • A method to change the weight of a single side. 
    • A method to roll the die one or more times.
    • A method to show the die’s current state.
    
    """
    def __init__(self, faces):
        """
        PURPOSE: This method initializes the Die object and saves both faces and weights in a private data frame with faces in the index.  
        
        INPUT:This method takes a NumPy array of faces as an argument. The array’s data type dtype may be strings or numbers, but the array’s values must be distinct.
        
        OUTPUT: None.

        """
        if type(faces) !=  np.ndarray:
            raise TypeError("Faces is not a NumPy array.")
        if len(faces) != len(np.unique(faces)):
            raise ValueError("Faces values must be distinct.")
        
        self.my_die = pd.DataFrame({'face': faces,'weight': [1.0] * len(faces)}).set_index('face')

        
    def change_weight(self, face, new_weight):
        """
        PURPOSE: This method changes the weight of a single side. 
        
        INPUT: Takes two arguments: the face value to be changed and the new weight.
        
        OUTPUT: None.

        """
        if face not in self.my_die.index:
            raise IndexError("Face is not on this Die.")
        try:
            new_weight = float(new_weight)
            if new_weight < 0:
                raise ValueError("Weight cannot be a negative value.")
        except ValueError:
                raise TypeError("Weight is not a valid type.")
        self.my_die.loc[face, 'weight'] = new_weight
    
    def roll_dice(self, n_rolls=1):
        """
        PURPOSE: This method rolls the die/dice using random sample with replacement, from the private die data frame, that applies the weights.
        
        INPUT: a parameter of how many times the die is to be rolled; defaults to  1.
        
        OUTPUT: pd.Series(results), a series with the results of the dice roll.

        """
        results = []
        for i in range(n_rolls):
            result = self.my_die.sample(weights=self.my_die['weight']).index.values[0]
            results.append(result)
        return pd.Series(results)
    
    def show(self):
        """
        PURPOSE: This method shows the die’s current state.
        
        INPUT: None.

        OUTPUT: Returns a copy of the private die data frame.
        
        """
        return self.my_die.copy()

    
    
class Game:
    """
    A game consists of rolling of one or more similar dice one or more times.
    
    Similar dice are Die objects that have the same number of sides and associated faces,
    though each die object may have its own weights. Game objects keep only the results
    of their most recent play.
    
    This Game class has 3 methods: 
    • An initializer.
    • A play method to simulate rolling a number of similar dice a specific number of times.
    • A method that shows the user the results of the most recent play.  
    """
    
    def __init__(self, dice_list):
        
        """
        PURPOSE: This method initializes the Game object with a list of dice objects. 
        
        INPUT: This method a single parameter, a list of already instantiated similar dice.
        
        OUTPUT: None.

        """
        self.dice_list = dice_list
        self.results = None
        
        
    def play(self, n_rolls):
        """
        PURPOSE: This method simulate rolling a number of similar dice a specific number of times.
        
        INPUT: This method takes an integer parameter to specify how many times the dice should be rolled.
        
        OUTPUT: This method saves the result of the play to a private data frame.

        """

        result_data = {}
        for i, dice in enumerate(self.dice_list):
            result_data[i] = dice.roll_dice(n_rolls).values
        self.results = pd.DataFrame(result_data)
        self.results.index.name = 'roll_number'
        
        
    def show(self, form='wide'):

        """
        PURPOSE: This method shows the user the results of the most recent play.  
        
        INPUT: This method takes a parameter to return the data frame in narrow or wide form which defaults to wide form.
        
        OUTPUT: This method outputs pandas.DataFrame of the results from the game.
        • The wide format will have the roll number as a named index, columns for each die number and the face rolled in that instance in each cell.
        • The narrow form will have a MultiIndex, comprising the roll number and the die number (in that order), and a single column with the outcomes.

        """
        
        if self.results is None:
            return None

        if form == 'wide':
            return self.results.copy()

        elif form == 'narrow':
            narrow_results = self.results.stack()
            narrow_results.index.names = ['roll_number', 'die_number']
            return narrow_results.to_frame('outcome')

        
        else:
            raise ValueError("Form must be either 'wide' or 'narrow'")
            

class Analyzer:
    """
    An Analyzer object takes the results of a single game and computes various descriptive statistical properties about it.
    
    This Analyzer class has 5 methods: 
    • An initializer.
    • A method that computes how many times the game resulted in a jackpot.
    • A method that computes how many times a given face is rolled in each event.
    • A method that computes the distinct combinations of faces rolled, along with their counts.
    • A method that computes the distinct permutations of faces rolled, along with their counts.
    
    """
    def __init__(self, game):
        """
        PURPOSE: This method initializes the Analyzer object.
        
        INPUT: This method takes a game object as its input parameter.
        
        OUTPUT: This method throws a ValueError if the passed value is not a Game object. Saves the result of show() on the game object.

        """
        if type(game) is not Game:
            raise ValueError("Value is not a Game object")
            
        self.game = game
        self.results = game.show(form='wide')
        self.jackpot_count = 0
        self.face_counts = None
        self.combo_counts = None
        self.permutation_counts = None

    def jackpot(self):
        
        """
        PURPOSE: This method computes how many times the game resulted in a jackpot. 
        
        INPUT: None
        
        OUTPUT: This method returns an integer for the number of jackpots.

        """
        
        count = 0
        for i in self.results.index:
            row = self.results.loc[i]
            if len(row.unique()) == 1:
                count += 1
        self.jackpot_count = count
        
        return self.jackpot_count

    def face_counts_per_roll(self):
        
        """
        PURPOSE: This method computes how many times a given face is rolled in each event.
        
        INPUT: None
        
        OUTPUT: This method returns a data frame of results.

        """
        
        counts_list = []
        
        for i in self.results.index:
            row = self.results.loc[i].values
            face_count = {}
            
            for face in row:
                face_count[face] = face_count.get(face, 0) + 1
                
            counts_list.append(face_count)
        
        counts_df = pd.DataFrame(counts_list).fillna(0).astype(int)
        counts_df.index = self.results.index
        
        self.face_counts = counts_df
        return self.face_counts

    def combo_count(self):
            
        """
        PURPOSE: This method computes the distinct combinations of faces rolled, along with their counts.
        
        INPUT: None
        
        OUTPUT: This method returns a data frame of results which has a MultiIndex of distinct combinations and a column for the associated counts.

        """
        
        combo_list = []
        
        for i in self.results.index:
            row = self.results.loc[i].values
            
            sorted_combo = tuple(sorted(row)) 
            
            combo_list.append(sorted_combo)
        
        combo_series = pd.Series(combo_list)
        combo_counts = combo_series.value_counts().to_frame(name='count')
        combo_counts.index.name = 'combo'
        
        self.combo_counts = combo_counts
        return self.combo_counts

    def permutation_count(self):
        
        """
        PURPOSE: This method computes the distinct permutations of faces rolled, along with their counts.
        
        INPUT: None
        
        OUTPUT: This method returns a data frame of results which has a MultiIndex of distinct permutations and a column for the associated counts.

        """
        perm_list = []

        for i in self.results.index:
            row = self.results.loc[i].values
            permutation = tuple(row) 
            perm_list.append(permutation)

        perm_series = pd.Series(perm_list)
        perm_counts = perm_series.value_counts().to_frame(name='count')
        perm_counts.index.name = 'permutation'

        self.permutation_counts = perm_counts
        return self.permutation_counts
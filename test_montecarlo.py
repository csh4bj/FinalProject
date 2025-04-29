import unittest
import numpy as np
import pandas as pd
from MonteCarlo import Die, Game, Analyzer

class DieGameAnalyzerTestSuite(unittest.TestCase):
    
     # Die method tests
    def test_die_init(self):
        faces = np.array(['H', 'T'])
        die = Die(faces)
        self.assertListEqual(list(die.my_die.index), list(faces))
        self.assertTrue((die.my_die['weight'] == 1.0).all())

    def test_die_change_weight(self):
        faces = np.array(['H', 'T'])
        die = Die(faces)
        die.change_weight('H', 5.0)
        result = die.show()
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.loc['H', 'weight'], 5.0)

    def test_die_roll_dice(self):
        faces = np.array(['H', 'T'])
        die = Die(faces)
        results = die.roll_dice(3)
        
        self.assertIsInstance(results, pd.Series)
        self.assertEqual(len(results), 3)

    def test_die_show(self):
        faces = np.array(['H', 'T'])
        die = Die(faces)
        df = die.show()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn('weight', df.columns)

    # Game method tests
    
    def test_game_init(self):
        faces = np.array(['H', 'T'])
        die = Die(faces)
        game = Game([die, die])
        
        self.assertEqual(len(game.dice_list), 2)

    def test_game_play(self):
        faces = np.array(['H', 'T'])
        die = Die(faces)
        game = Game([die, die])
        game.play(5)
        
        self.assertIsInstance(game.results, pd.DataFrame)
        self.assertEqual(game.results.shape[0], 5)
        
    def test_game_show_wide(self):
        faces = np.array(['H', 'T'])
        die = Die(faces)
        game = Game([die, die])
        game.play(5)
        
        df = game.show(form='wide')
        self.assertEqual(df.shape, (5, 2))
        self.assertIsInstance(df, pd.DataFrame)

    def test_game_show_narrow(self):
        faces = np.array(['H', 'T'])
        die = Die(faces)
        game = Game([die, die])
        game.play(5)
        df = game.show(form='narrow')
        
        self.assertEqual(df.shape, (10, 1))
        self.assertIsInstance(df, pd.DataFrame)
        
        
        # Analyzer method tests
        
    def test_analyzer_init(self):
        faces = np.array(['H', 'T'])
        die = Die(faces)
        game = Game([die, die])
        game.play(5)
        analyzer = Analyzer(game)
        
        self.assertEqual(analyzer.jackpot_count, 0)
        self.assertIsNone(analyzer.face_counts)
        self.assertIsNone(analyzer.combo_counts)
        self.assertIsNone(analyzer.permutation_counts)

    def test_analyzer_jackpot(self):
        faces = np.array(['H', 'T'])
        die = Die(faces)
        game = Game([die, die])
        game.play(5)
        analyzer = Analyzer(game)
        count = analyzer.jackpot()
        
        self.assertIsInstance(count, int)
        self.assertLessEqual(count, len(game.results))

    def test_analyzer_face_counts_per_roll(self):
        faces = np.array(['H', 'T'])
        die = Die(faces)
        game = Game([die, die])
        game.play(5)
        analyzer = Analyzer(game)
        df = analyzer.face_counts_per_roll()
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 5)
        self.assertTrue(df.index.equals(game.results.index))
        
    def test_analyzer_combo_count(self):
        faces = np.array(['H', 'T'])
        die = Die(faces)
        game = Game([die, die])
        game.play(5)
        analyzer = Analyzer(game)
        df = analyzer.combo_count()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertLessEqual(len(df), 5)
        self.assertIn('count', df.columns)


    def test_analyzer_permutation_count(self):
        faces = np.array(['H', 'T'])
        die = Die(faces)
        game = Game([die, die])
        game.play(5)
        analyzer = Analyzer(game)
        df = analyzer.permutation_count()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertLessEqual(len(df), 5)
        self.assertIn('count', df.columns)

if __name__ == '__main__':
    unittest.main(verbosity=3)
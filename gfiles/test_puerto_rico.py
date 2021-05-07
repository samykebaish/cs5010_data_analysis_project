import unittest
import pandas as pd
from pandas._testing import assert_frame_equal
from remove_puerto_rico import remove_puerto_rico

class PuertoRicoTestCase(unittest.TestCase): # inherit from unittest.TestCase
    
    def test_can_remove_puerto_rico(self):
        data_removed = [['Kansas', 54], ['Utah', 14]]
        correct_df = pd.DataFrame(data_removed, columns = ['State', 'STATEFIP'])
        
        data = [['Puerto Rico', 72], ['Kansas', 54], ['Utah', 14]]
        test_df = pd.DataFrame(data, columns = ['State', 'STATEFIP'])
        test_df.reset_index()
        
        new_df = remove_puerto_rico(test_df)
        
        assert_frame_equal(correct_df, new_df) 
                
            
if __name__ == '__main__':
    unittest.main()            
import unittest
import pandas as pd
from pandas._testing import assert_frame_equal


#Function in the jupyter notebook that is being tested
#this is tested inside the notebook for better visiblity, in this file due to 
#project requirements. 
def remove_puerto_rico(df):
    df = df[df['STATEFIP'] != 72]
    df = df.reset_index(drop=True)
    return df

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

#Testing datatypes
def coltypes(self): #function is also in Jupyter notebook
    categories = ['YEAR', 'EDUC', 'ETHNIC', 'RACE', 'GENDER', 'SPHSERVICE',
       'CMPSERVICE', 'OPISERVICE', 'RTCSERVICE', 'IJSSERVICE', 'MH1', 'MH2',
       'MH3', 'SUB', 'MARSTAT', 'SMISED', 'SAP', 'EMPLOY', 'DETNLF', 'VETERAN',
       'LIVARAG', 'NUMMHS', 'TRAUSTREFLG', 'ANXIETYFLG', 'ADHDFLG',
       'CONDUCTFLG', 'DELIRDEMFLG', 'BIPOLARFLG', 'DEPRESSFLG', 'ODDFLG',
       'PDDFLG', 'PERSONFLG', 'SCHIZOFLG', 'ALCSUBFLG', 'OTHERDISFLG',
       'STATEFIP', 'DIVISION', 'REGION', 'CASEID', 'AGEFLAG'] #list of the columns that have categorial data
    cld[categories] = cld[categories].astype('category') #casting the categorical columns

class coltypestestcase(unittest.TestCase): #Setting up test case
    def test_coltypes(self): #Initializing
        categories = ['YEAR', 'EDUC', 'ETHNIC', 'RACE', 'GENDER', 'SPHSERVICE',
       'CMPSERVICE', 'OPISERVICE', 'RTCSERVICE', 'IJSSERVICE', 'MH1', 'MH2',
       'MH3', 'SUB', 'MARSTAT', 'SMISED', 'SAP', 'EMPLOY', 'DETNLF', 'VETERAN',
       'LIVARAG', 'NUMMHS', 'TRAUSTREFLG', 'ANXIETYFLG', 'ADHDFLG',
       'CONDUCTFLG', 'DELIRDEMFLG', 'BIPOLARFLG', 'DEPRESSFLG', 'ODDFLG',
       'PDDFLG', 'PERSONFLG', 'SCHIZOFLG', 'ALCSUBFLG', 'OTHERDISFLG',
       'STATEFIP', 'DIVISION', 'REGION', 'CASEID', 'AGEFLAG'] #list of the columns that have categorial data
        cld[categories] = cld[categories].astype('category') #casting as categorical dtype
        self.assertEqual(cld['YEAR'].dtypes, 'category') #testing one of my categories columns

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

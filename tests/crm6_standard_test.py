import os
import unittest
import sys
import tempfile

sys.path.append('../fightchurn')
sys.path.append('../churnsim')
from fightchurn import run_churn_listing
from fightchurn.churnsim import churndb


class TestFightChurnWIthData(unittest.TestCase):
    def test_run_entire_book(self):
        database=username=password='churn'
        test_ouput_dir = os.path.join(tempfile.gettempdir(),'fightchurn_test_output')
        print(f'TestFightChurnWIthData writing to temporary output directory {test_ouput_dir}')
        run_churn_listing.set_churn_environment(database,username,password)
        churndb.drop_schema('socialnet7')
        self.assertEqual(True, run_churn_listing.run_everything(database, username, password,
                                                                schema='scoialnet7', output_dir=test_ouput_dir))


if __name__ == '__main__':
    unittest.main()

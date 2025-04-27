import os
import unittest
import sys
import tempfile

sys.path.append('../fightchurn')
sys.path.append('../churnsim')
from fightchurn import run_churn_listing
from fightchurn.churnsim import churndb


class TestFightChurnWithDataCRM(unittest.TestCase):
    @unittest.skip("TestFightChurnWithDataCRM Slow test - comment line 13 to run")
    def test_crm_run_entire_book(self):
        database='churn'
        username=password='postgres'
        test_ouput_dir = os.path.join(tempfile.gettempdir(),'fightchurn_test_output')
        print(f'TestFightChurnWIthData writing to temporary output directory {test_ouput_dir}')
        run_churn_listing.set_churn_environment(database,username,password)
        churndb.drop_schema('crm6')
        self.assertEqual(True, run_churn_listing.run_everything(database, username, password,
                                                                schema='crm6', output_dir=test_ouput_dir, n_parallel=-1))


if __name__ == '__main__':
    unittest.main()

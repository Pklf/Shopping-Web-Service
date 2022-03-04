import unittest
import test_buy, test_query, test_replenish, test_server_common # unittest files

# you can comment out unit test that you don't want

testcase_buy = unittest.TestLoader().loadTestsFromModule(test_buy)
unittest.TextTestRunner(verbosity=2).run(testcase_buy)

testcase_query = unittest.TestLoader().loadTestsFromModule(test_query)
unittest.TextTestRunner(verbosity=2).run(testcase_query)

testcase_replenish = unittest.TestLoader().loadTestsFromModule(test_replenish)
unittest.TextTestRunner(verbosity=2).run(testcase_replenish)

testcase_common = unittest.TestLoader().loadTestsFromModule(test_server_common)
unittest.TextTestRunner(verbosity=2).run(testcase_common)

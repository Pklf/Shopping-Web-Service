import subprocess, unittest, time, os
from lib.lib_tests import ws_client
from os import environ, path
from dotenv import load_dotenv

# get .env 
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(path.dirname(basedir), ".env"))

# get Flask host and port
FLASK_RUN_HOST = environ.get("FLASK_RUN_HOST")
FLASK_RUN_PORT = environ.get("FLASK_RUN_PORT")

# get server host and port for ws_client
SERVER = f"{FLASK_RUN_HOST}:{FLASK_RUN_PORT}"

class TestShoppingServer_common(unittest.TestCase):

    def setUp(self):
        self.product_id_valid = 0
        self.buy_quantity = 5
        self.credit_card_valid = "0123456789123456"
        self.server_proc = subprocess.Popen(
            ["python", "./src/main.py"])
        time.sleep(0.5)

    def tearDown(self):
        os.system('taskkill /t /f /pid {}'.format(self.server_proc.pid))
        self.server_proc.terminate()
        # a server more frequently than once every 4 seconds may be considered as attempting a denial-of-service attack.
        time.sleep(5) 

    def test_data_persistence(self):
        # get stock quantity before buy operation
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        stock_before_buy = query["quantity"]

        # check if return expected 
        response = ws_client(f"http://{SERVER}/api/product/buy/{self.product_id_valid}","PUT",
        {"quantity": self.buy_quantity, "credit_card": self.credit_card_valid})

        self.assertEqual(response["status"], "success")
        self.assertIsInstance(response["exe_id"], str)

        # get stock quantity after buy operation
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        stock_after_buy = query["quantity"]

        # check if stock quantity reduced
        self.assertEqual(stock_before_buy - self.buy_quantity, stock_after_buy)

        # close the server
        os.system('taskkill /t /f /pid {}'.format(self.server_proc.pid))
        self.server_proc.terminate()
        # a server more frequently than once every 4 seconds may be considered as attempting a denial-of-service attack.
        time.sleep(5)

        # re-open the server
        self.server_proc = subprocess.Popen(["python", "./src/main.py"])
        time.sleep(0.5)

        # check if the stock quantity same as last time
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        stock_after_reopen = query["quantity"]

        self.assertEqual(stock_after_reopen , stock_after_buy)

        # replenish bought product quantity
        ws_client(f"http://{SERVER}/api/product/replenish/{self.product_id_valid}","PUT", 
        {"quantity": self.buy_quantity})

    def test_exe_id_reopen_different(self):
        # get stock quantity before reopen server
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        exe_id_before_reopen = query["exe_id"]

        # close the server
        os.system('taskkill /t /f /pid {}'.format(self.server_proc.pid))
        self.server_proc.terminate()
        # a server more frequently than once every 4 seconds may be considered as attempting a denial-of-service attack.
        time.sleep(5)

        # re-open the server
        self.server_proc = subprocess.Popen(["python", "./src/main.py"])
        time.sleep(0.5)

        # check is the execution ID different from last time
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        exe_id_after_reopen = query["exe_id"]

        self.assertNotEqual(exe_id_before_reopen, exe_id_after_reopen)

if __name__ == "__main__":
    unittest.main(verbosity=2)
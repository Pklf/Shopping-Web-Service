import json, subprocess, unittest, time
from urllib.error import HTTPError
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

class TestShoppingServer_replenish(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_proc = subprocess.Popen(
            ["python", "./src/main.py"])
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.server_proc.terminate()

    def setUp(self):
        self.product_id_valid = 5
        self.product_id_error = 999
        self.replenish_quantity = 5
        self.credit_card = "0123456789123456"
        self.str_error = "ABC"
        self.neg_error = -100

    def test_replenish_valid_success(self):
        # get stock quantity before replenish operation
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        stock_before_replenish = query["quantity"]

        # check if response as expected 
        response = ws_client(f"http://{SERVER}/api/product/replenish/{self.product_id_valid}","PUT", 
        {"quantity": self.replenish_quantity})

        self.assertEqual(response["status"], "success")
        self.assertEqual(response["id"], self.product_id_valid)
        self.assertEqual(response["current_quantity"], stock_before_replenish + self.replenish_quantity)
        self.assertIsInstance(response["exe_id"], str)

        # get stock quantity after replenish operation
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        stock_after_replenish = query["quantity"]

        # check if stock quantity added
        self.assertEqual(stock_after_replenish, stock_before_replenish + self.replenish_quantity)

        # buy product in replenished product quantity
        ws_client(f"http://{SERVER}/api/product/buy/{self.product_id_valid}","PUT", 
        {"quantity": self.replenish_quantity, "credit_card": self.credit_card})

    # input missing 
    def test_replenish_missing_id_error(self):
        try:
            ws_client(f"http://{SERVER}/api/product/replenish/","PUT", 
            {"quantity": self.replenish_quantity})

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(404, e.code) 

    def test_replenish_missing_quantity_error(self):
        try:
            ws_client(f"http://{SERVER}/api/product/replenish/{self.product_id_valid}","PUT")

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "missing quantity")

    # input invalid (not missing) 
    def test_replenish_id_not_integer_error(self):
        try:
            ws_client(f"http://{SERVER}/api/product/replenish/{self.str_error}","PUT", 
            {"quantity": self.replenish_quantity})

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "id is not zero or a positive integer")

    def test_replenish_quantity_not_positive_integer_error_str(self):
        try:
            ws_client(f"http://{SERVER}/api/product/replenish/{self.product_id_valid}","PUT", 
            {"quantity": self.str_error})

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "quantity is not a positive integer")

    def test_replenish_quantity_not_positive_integer_error_negative_number(self):
        try:
            ws_client(f"http://{SERVER}/api/product/replenish/{self.product_id_valid}","PUT", 
            {"quantity": self.neg_error})

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "quantity is not a positive integer")

    # product ID does not exist
    def test_buy_id_not_found_error(self):
        try:
            ws_client(f"http://{SERVER}/api/product/replenish/{self.product_id_error}","PUT", 
            {"quantity": self.replenish_quantity}) 

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(404, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "product ID does not exist")

if __name__ == "__main__":
    unittest.main(verbosity=2)

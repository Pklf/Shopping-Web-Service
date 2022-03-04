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

class TestShoppingServer_query(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_proc = subprocess.Popen(
            ["python", "./src/main.py"])
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.server_proc.terminate()

    def setUp(self):
        self.product_id_valid = 0
        self.product_id_error = 999
        self.str_error = "ABC"
        self.neg_error = -100
        self.buy_quantity = 5
        self.credit_card_valid = "0123456789123456"

    def test_query_valid(self):
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        stock_before_second_query = query["quantity"]

        print(query)
        self.assertEqual(query["id"], 0)
        self.assertEqual(query["desc"], "apple")
        self.assertEqual(query["price"], 10)
        self.assertIsInstance(query["exe_id"], str)

        # buy product
        ws_client(f"http://{SERVER}/api/product/buy/{self.product_id_valid}","PUT",
        {"quantity": self.buy_quantity, "credit_card": self.credit_card_valid})

        # check if query correct
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        self.assertEqual(query["quantity"], stock_before_second_query - self.buy_quantity)

        # replenish product
        ws_client(f"http://{SERVER}/api/product/replenish/{self.product_id_valid}","PUT",
        {"quantity": self.buy_quantity})

        # check if query correct
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        self.assertEqual(query["quantity"], stock_before_second_query)


    def test_query_not_exist_id_error(self):
        try:
            ws_client(f"http://{SERVER}/api/product/query/{self.product_id_error}")
            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(404, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "product ID does not exist")

    def test_query_id_error_str(self):
        try:
            ws_client(f"http://{SERVER}/api/product/query/{self.str_error}")
            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "id is not zero or a positive integer")

    def test_query_id_error_negative(self):
        try:
            ws_client(f"http://{SERVER}/api/product/query/{self.neg_error}")
            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "id is not zero or a positive integer")

    def test_query_missing_id_error(self):
        try:
            ws_client(f"http://{SERVER}/api/product/query/")
            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(404, e.code)

if __name__ == "__main__":
    unittest.main(verbosity=2)

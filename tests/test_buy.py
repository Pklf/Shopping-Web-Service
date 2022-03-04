import json, subprocess, unittest, time, concurrent.futures
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

class TestShoppingServer_buy(unittest.TestCase):
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
        self.product_id_not_found_error = 999
        self.buy_quantity = 5
        self.credit_card_valid = "0123456789123456"
        self.credit_card_error = "Not_16_length_digit"
        self.str_error = "ABC"
        self.negative_error = -100

    def test_buy_valid_success(self):
        # get stock quantity before buy operation
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        stock_before_buy = query["quantity"]
        product_price = query["price"]

        # check if return expected 
        response = ws_client(f"http://{SERVER}/api/product/buy/{self.product_id_valid}","PUT",
         {"quantity": self.buy_quantity, "credit_card": self.credit_card_valid})

        self.assertEqual(response["status"], "success")
        self.assertEqual(response["amount_deducted"], self.buy_quantity*product_price)
        self.assertIsInstance(response["exe_id"], str)

        # get stock quantity after buy operation
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        stock_after_buy = query["quantity"]

        # check if stock quantity reduced
        self.assertEqual(stock_before_buy - self.buy_quantity, stock_after_buy)

        # replenish bought product quantity
        ws_client(f"http://{SERVER}/api/product/replenish/{self.product_id_valid}","PUT", 
        {"quantity": self.buy_quantity})

    def test_buy_valid_fail(self):
        # get stock quantity before buy operation
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        stock_before_buy = query["quantity"]
        insufficient_stock_amount = stock_before_buy + 1

        # check if return expected 
        response = ws_client(f"http://{SERVER}/api/product/buy/{self.product_id_valid}",
        "PUT", {"quantity": insufficient_stock_amount, "credit_card": self.credit_card_valid})

        self.assertEqual(response["status"], "failure (insufficient quantity in stock)")
        self.assertIsInstance(response["exe_id"], str)

        # get stock quantity after buy operation
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        stock_after_buy = query["quantity"]

        # check if stock quantity reduced
        self.assertEqual(stock_before_buy , stock_after_buy)

    # input missing 
    def test_buy_missing_id_error(self):
        try:
            ws_client(f"http://{SERVER}/api/product/buy/","PUT", 
            {"quantity": self.buy_quantity, "credit_card": self.credit_card_valid})

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(404, e.code)  
    
    def test_buy_missing_quantity_error(self):
        try:
            ws_client(f"http://{SERVER}/api/product/buy/{self.product_id_valid}","PUT", 
            {"credit_card": self.credit_card_valid})

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "missing quantity")
        
    def test_buy_missing_credit_card_error(self):
        try:
            ws_client(f"http://{SERVER}/api/product/buy/{self.product_id_valid}","PUT", 
            {"quantity": self.buy_quantity})

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "missing credit card number")

    def test_buy_missing_quantity_and_card_error(self):
        try:
            ws_client(f"http://{SERVER}/api/product/buy/{self.product_id_valid}","PUT")

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "missing quantity, missing credit card number")

    # input invalid (not missing) 
    def test_buy_id_not_integer_error_str(self):
        try:
            ws_client(f"http://{SERVER}/api/product/buy/{self.str_error}","PUT", {"quantity": self.buy_quantity, 
            "credit_card": self.credit_card_valid})

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "id is not zero or a positive integer")
    
    def test_buy_id_not_integer_error_negative_number(self):
        try:
            ws_client(f"http://{SERVER}/api/product/buy/{self.negative_error}","PUT", {"quantity": self.buy_quantity, 
            "credit_card": self.credit_card_valid})

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "id is not zero or a positive integer")

    def test_buy_quantity_not_positive_integer_error_str(self):
        try:
            ws_client(f"http://{SERVER}/api/product/buy/{self.product_id_valid}","PUT", 
            {"quantity": self.str_error, "credit_card": self.credit_card_valid})

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "quantity is not a positive integer")

    def test_buy_quantity_not_positive_integer_error_negative_number(self):
        try:
            ws_client(f"http://{SERVER}/api/product/buy/{self.product_id_valid}","PUT", 
            {"quantity": self.negative_error, "credit_card": self.credit_card_valid})

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "quantity is not a positive integer")

    def test_buy_credit_card_error(self):
        try:
            ws_client(f"http://{SERVER}/api/product/buy/{self.product_id_valid}","PUT", 
            {"quantity": self.buy_quantity, "credit_card": self.credit_card_error})

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(400, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "incorrect credit card format (isn't 16 digits)")

    # product ID does not exist
    def test_buy_id_not_found_error(self):
        try:
            ws_client(f"http://{SERVER}/api/product/buy/{self.product_id_not_found_error}","PUT", 
            {"quantity": self.buy_quantity, "credit_card": self.credit_card_valid}) 

            self.assertTrue(False)
        except HTTPError as e:
            self.assertEqual(404, e.code)
            result = json.loads(e.read().decode("utf-8"))
            self.assertEqual(result["error"], "product ID does not exist")

    # simultaneously buy requests
    def test_buy_simultaneously_and_insufficient_for_second(self):
        """
        two requests for buying the same product arrive almost simultaneously and the quantity in stock is insufficient
        for the second request
        """
        # get stock quantity before buy operation
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        stock_before_buy = query["quantity"]
        product_price = query["price"]

        N_THREADS = 2

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(ws_client, *param) for param in 
            [(f"http://{SERVER}/api/product/buy/{self.product_id_valid}","PUT", 
            {"quantity": stock_before_buy, "credit_card": self.credit_card_valid})]*N_THREADS]

        # check if first request success to buy and second request fail to buy
        response_set = set() # a set to save response status (should be one success and one fail)
        for response in [f.result() for f in futures]:
            # print(response)
            response_set.add(response["status"])
            self.assertIsInstance(response["exe_id"], str)
            if response["status"] == "success":
                self.assertEqual(response["status"], "success")
                self.assertEqual(response["amount_deducted"], stock_before_buy*product_price)

        self.assertSetEqual(response_set, {"failure (insufficient quantity in stock)", "success"})

        # get stock quantity after buy operation
        query = ws_client(f"http://{SERVER}/api/product/query/{self.product_id_valid}")
        stock_after_buy = query["quantity"]

        # check if stock quantity reduced to 0
        self.assertEqual(stock_after_buy, 0)

        # replenish bought product quantity
        ws_client(f"http://{SERVER}/api/product/replenish/{self.product_id_valid}",
        "PUT", {"quantity": stock_before_buy})

if __name__ == "__main__":
    unittest.main(verbosity=2)

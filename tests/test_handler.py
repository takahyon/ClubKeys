import unittest
import lambda_function


class TestHandlerCase(unittest.TestCase):

    def test_response(self):
        print("testing response.")
        result = lambda_function.lambda_handler(None, None)
        print(result)
        #self.assertEqual(result['statusCode'], 200)
        #self.assertEqual(result['headers']['Content-Type'], 'application/json')
        #self.assertIn('Hello World', result['body'])



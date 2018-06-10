import requests
import base64 
import datetime
import json
import unittest
# import nosetest

API = 'https://apiplus-api-sandbox-testnet.factom.com/v1'

KEY = 'GUWiB4x3JwrOiaWyFMYLlRmfJr7YfFFGDMzwYG80sdtL4BDT'

HEADERS = {'Content-Type': 'application/json', 'factom-provider-token': KEY }

# Return base 64 encoding of a string
def _b64encode(str):
    return base64.b64encode(str.encode('utf-8')).decode('utf-8')

# Return base 64 decoding of a string
def _b64decode(str):
    return base64.b64decode(str.encode('utf-8')).decode('utf-8')

# Return unix timestamp at current moment
def _unix_timestamp():
    return '{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())

# Create json payload for a block using external_ids and content
def _json_block_payload(external_ids, content):
    payload = dict()
    payload['external_ids'] = [_b64encode(_id) for _id in external_ids]
    payload['content'] = _b64encode(content)
    return payload

# Create new blockchain and return the chain id
def create_new_chain(external_ids, content):
    response = requests.post("{}/chains".format(API),
               json=_json_block_payload(external_ids, content), headers=HEADERS)
    return response.json()["chain_id"]

# Unit tests 
class FactomAPITest(unittest.TestCase):

    # Test base 64 encode
    def test_b64encode(self):
        data = "foobar"
        expected = "Zm9vYmFy"
        output = _b64encode(data)
        print("\nInput = {} \nOutput = {}".format(data, output))
        self.assertEqual(expected, output)

    # Test base 64 decode
    def test_b64decode(self):
        data = "Zm9vYmFy"
        expected = "foobar"
        output = _b64decode(data)
        print("\nInput = {} \nOutput = {}".format(data, output))
        self.assertEqual(expected, output)
    
    # Test unix timestamp
    def test_unix_timestamp(self):
        print("\nDateTime = {}".format(_unix_timestamp()))
        self.assertTrue(True)

    # Test json block payload
    def test_json_block_payload(self):
        data = (["foo", "bar"], "content")
        expected = {"external_ids" : ["Zm9v", "YmFy"], "content" : "Y29udGVudA=="}
        output = _json_block_payload(*data)
        print("\nInput = {} \nOutput = {}".format(data, output))
        self.assertEqual(expected, output)

    def test_create_new_chain(self):
        data = (["foo", "bar"], "content")
        chain_id = create_new_chain(*data)
        print("\nChain ID = {}".format(chain_id))
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()

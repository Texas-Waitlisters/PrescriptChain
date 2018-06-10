import requests
import base64 
import datetime
import json
import unittest
# import nosetest

API = 'https://apiplus-api-sandbox-testnet.factom.com/v1/'

KEY = 'GUWiB4x3JwrOiaWyFMYLlRmfJr7YfFFGDMzwYG80sdtL4BDT'

HEADER  = {'Content-Type': 'application/json', 'factom-provider-token': KEY }

def _base64(str):
    return base64.b64encode(str.encode('utf-8')).decode('utf-8')

def unix_timestamp():
    return "{:%Y-%m-%d-%H-%M-%S}".format(datetime.datetime.now())

def _json_block_payload(external_ids, content):
    payload = dict()
    payload["external_ids"] = [_base64(_id) for _id in external_ids]
    payload["content"] = _base64(content)
    return json.dumps(payload)

# Create new blockchain and return the chain id
def create_new_chain(external_ids, temp):
    response = requests.post("{}/chains".format(API),
               json=_json_block_payload(external_ids, content), headers=headers)
    return response.json()["chain_id"]

class FactomAPITest(unittest.TestCase):

    def test_base64(self):
        expected = "Zm9vYmFy"
        output = _base64("foobar")
        self.assertEqual(expected, output)
    
    def test_unix_timestamp(self):
        print("datetime = {}".format(unix_timestamp()))
        self.assertTrue(True)

    def test_json_block_payload(self):
        expected = {"external_ids" : ["Zm9v", "YmFy"], "content" : "Y29udGVudA=="}
        output = _json_block_payload(["foo", "bar"], "content")
        self.assertEqual(expected, json.loads(output))

if __name__ == "__main__":
    unittest.main()


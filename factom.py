import requests
import base64 
import datetime
import json
import unittest

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

# Create payload for a block using external_ids and content
def _block_payload(external_ids, content):
    payload = dict()
    payload['external_ids'] = [_b64encode(_id) for _id in external_ids]
    payload['content'] = _b64encode(content)
    return payload

# Create new blockchain and return the chain_id and entry_hash
def create_new_chain(external_ids, content):
    response = requests.post("{}/chains".format(API),
               json=_block_payload(external_ids, content), headers=HEADERS)
    return response.json()

# Add to block chain with chain_id and return entry_hash
def get_chain(chain_id):
    response = requests.get("{}/chains/{}/entries".format(API, chain_id),
               headers=HEADERS)
    return response.json()

# Add to block chain with chain_id and return entry_hash
def add_to_chain(chain_id, external_ids, content):
    response = requests.post("{}/chains/{}/entries".format(API, chain_id),
               json=_block_payload(external_ids, content), headers=HEADERS)
    return response.json()

# Get entry specified entry_hash of block, can specify hash, first, or last by default
# If block not found, return None
def get_entry(chain_id, entry_hash="last"):
    response = requests.get("{}/chains/{}/entries/{}".format(API, chain_id, entry_hash), 
               headers=HEADERS)
    if response.status_code == 200:
        result = response.json()
        result["content"] = _b64decode(result["content"])
        return result
    return { "entry_hash" : None, "content" : None }

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

    # Test block payload
    def test_block_payload(self):
        data = (["foo", "bar"], "content")
        expected = {"external_ids" : ["Zm9v", "YmFy"], "content" : "Y29udGVudA=="}
        output = _block_payload(*data)
        print("\nInput = {} \nOutput = {}".format(data, output))
        self.assertEqual(expected, output)

    def test_create_chain(self):
        data = ("foobar", "content")
        output = create_new_chain(*data)
        chain_id = output["chain_id"]
        print("\nChain ID = {}\nEntry Hash = {}".format(chain_id, output["entry_hash"]))
        print("\nThis Entry In Chain = {}".format(get_entry(chain_id, output["entry_hash"])))
        data = (chain_id,"foobar", "more content")
        output = add_to_chain(*data)
        print("\nEntry Hash = {}".format(output["entry_hash"]))
        print("\nThis Entry In Chain = {}".format(get_entry(chain_id, output["entry_hash"])))
        data = (chain_id,"foobar", "last content")
        output = add_to_chain(*data)
        print("\nEntry Hash = {}".format(output["entry_hash"]))
        print("\nLast Entry In Chain = {}".format(get_entry(chain_id)))
        print("\nChain Entries = {}".format(get_chain(chain_id)))
        print("\nThis Entry In Chain = {}".format(get_entry(chain_id, output["entry_hash"])))
        print("\nFake Entry In Chain = {}".format(get_entry(chain_id, 926379234)))
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()


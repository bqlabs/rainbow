import unittest
from rainbow import app, register


class RainbowTest(unittest.TestCase):

    def setUp(self):
        # Register functions
        @register('subtract')
        def subtract(minuend, subtrahend):
            return minuend - subtrahend

    def test_subtract_args(self):
        request = '{"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}'
        response = '{"jsonrpc": "2.0", "result": 19, "id": 1}'
        self.assertEqual(app.json_rpc(request), app.json_str(response))

    def test_subtract_kwargs(self):
        request = '{"jsonrpc": "2.0", "method": "subtract", ' \
                  '"params": {"subtrahend": 23, "minuend": 42}, "id": 3}'
        response = '{"jsonrpc": "2.0", "result": 19, "id": 3}'
        self.assertEqual(app.json_rpc(request), app.json_str(response))

    def test_notification(self):
        request = '{"jsonrpc": "2.0", "method": "update", "params": [1,2,3,4,5]}'
        response = '{"jsonrpc": "2.0", "method": "foobar"}'
        self.assertEqual(app.json_rpc(request), app.json_str(response))

    def test_non_existent_method(self):
        request = '{"jsonrpc": "2.0", "method": "foobar", "id": "1"}'
        response = '{"jsonrpc": "2.0", "error": {"code": -32601, ' \
                   '"message": "Method not found"}, "id": "1"}'
        self.assertEqual(app.json_rpc(request), app.json_str(response))

    def test_invalid_json(self):
        request = '{"jsonrpc": "2.0", "method": "foobar, "params": "bar", "baz]'
        response = '{"jsonrpc": "2.0", "error": {"code": -32700, ' \
                   '"message": "Parse error"}, "id": null}'
        self.assertEqual(app.json_rpc(request), app.json_str(response))

    def test_invalid_request(self):
        request = '{"jsonrpc": "2.0", "method": 1, "params": "bar"}'
        response = '{"jsonrpc": "2.0", "error": {"code": -32600, ' \
                   '"message": "Invalid Request"}, "id": null}'
        self.assertEqual(app.json_rpc(request), app.json_str(response))

    def test_batch_invalid_json(self):
        request = '[{"jsonrpc": "2.0", "method": "sum", "params": [1,2,4], "id": "1"},' \
                  '{"jsonrpc": "2.0", "method"]'
        response = '{"jsonrpc": "2.0", "error": {"code": -32700, ' \
                   '"message": "Parse error"}, "id": null}'
        self.assertEqual(app.json_rpc(request), app.json_str(response))

    def test_batch_emtpy_array(self):
        request = '[]'
        response = '{"jsonrpc": "2.0", "error": {"code": -32600, ' \
                   '"message": "Invalid Request"}, "id": null}'
        self.assertEqual(app.json_rpc(request), app.json_str(response))

    def test_batch_invalid_not_empty(self):
        request = '[1]'
        response = '[{"jsonrpc": "2.0", "error": {"code": -32600, ' \
                   '"message": "Invalid Request"}, "id": null}]'
        self.assertEqual(app.json_rpc(request), app.json_str(response))

    def test_batch_invalid(self):
        request = '[1,2,3]'
        response = '[' \
            '{"jsonrpc": "2.0", "error": {"code": -32600, ' \
            '"message": "Invalid Request"}, "id": null},' \
            '{"jsonrpc": "2.0", "error": {"code": -32600, ' \
            '"message": "Invalid Request"}, "id": null},' \
            '{"jsonrpc": "2.0", "error": {"code": -32600, ' \
            '"message": "Invalid Request"}, "id": null}]'
        self.assertEqual(app.json_rpc(request), app.json_str(response))

    def test_call_batch(self):
        request = '[' \
            '{"jsonrpc": "2.0", "method": "sum", "params": [1,2,4], "id": "1"},' \
            '{"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},' \
            '{"jsonrpc": "2.0", "method": "subtract", "params": [42,23], "id": "2"},' \
            '{"foo": "boo"},' \
            '{"jsonrpc": "2.0", "method": "foo.get", "params": {"name": "myself"}, "id": "5"},' \
            '{"jsonrpc": "2.0", "method": "get_data", "id": "9"}]'
        response = '[' \
            '{"jsonrpc": "2.0", "result": 7, "id": "1"},' \
            '{"jsonrpc": "2.0", "result": 19, "id": "2"},' \
            '{"jsonrpc": "2.0", "error":{"code": -32600, "message": "Invalid Request"}, "id": null},' \
            '{"jsonrpc": "2.0", "error":{"code": -32601, "message": "Method not found"}, "id": "5"},' \
            '{"jsonrpc": "2.0", "result": ["hello", 5], "id": "9"}]'
        self.assertEqual(app.json_rpc(request), app.json_str(response))

    def test_call_batch_notification(self):
        request = '[{"jsonrpc": "2.0", "method": "notify_sum", "params": [1,2,4]},' \
                  '{"jsonrpc": "2.0", "method": "notify_hello", "params": [7]}]'
        response = ''
        self.assertEqual(app.json_rpc(request), app.json_str(response))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()

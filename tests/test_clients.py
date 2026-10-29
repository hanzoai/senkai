import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError
from sekai_cookbook import Worlds


class Mock(BaseHTTPRequestHandler):
    """Transport fixture only: no model, predictions or benchmark measurements."""
    def log_message(self, *args): pass
    def do_POST(self):
        if self.headers.get('Authorization')!='Bearer test-only-key':
            self.send_error(401);return
        body=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        if self.path=='/v1/worlds':
            if body!={'model':'sekai-1-alpha','domain':'simulation'}:
                self.send_error(422);return
            data={'id':'world_mock','model':'sekai-1-alpha','release_stage':'alpha','mock':True}
        elif self.path=='/v1/worlds/world_mock/events':
            data={'accepted':True,'mock':True}
        elif self.path=='/v1/worlds/world_mock/plans':
            data={'execution':'disabled','mock':True}
        else:
            self.send_error(404);return
        raw=json.dumps(data).encode();self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)


class Clients(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Mock)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.base=f'http://127.0.0.1:{cls.server.server_port}/v1'
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def test_alpha_create(self):
        result=Worlds(self.base,'test-only-key').create()
        self.assertEqual(result['model'],'sekai-1-alpha');self.assertTrue(result['mock'])
    def test_auth_refused(self):
        with self.assertRaises(HTTPError) as error:Worlds(self.base,'wrong').create()
        self.assertEqual(error.exception.code,401)
    def test_events_and_plans_are_remote(self):
        client=Worlds(self.base,'test-only-key')
        self.assertTrue(client.event('world_mock',{'event_id':'e'})['mock'])
        self.assertEqual(client.plan('world_mock',{'candidates':[]})['execution'],'disabled')
    def test_credential_transport_refused(self):
        for base in ['http://example.com/v1','https://key:secret@example.com/v1','https://example.com/other']:
            with self.assertRaises(ValueError):Worlds(base,'test-key')
    def test_unrelated_route_refused(self):
        with self.assertRaises(ValueError):Worlds(self.base,'test-only-key').request('POST','/admin',{})


if __name__=='__main__':unittest.main()

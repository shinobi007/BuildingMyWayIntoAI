"""Offline regression suite for the additive, read-only role explorer.

Run from FinalVersion: python -m unittest discover -s tests -p test_role_explorer.py -v
"""
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import threading
import unittest
from urllib.request import urlopen

MODULE = Path(__file__).resolve().parents[1] / 'app' / 'proofloop_explorer.py'
S = importlib.util.spec_from_file_location('proofloop_explorer', MODULE)
explorer = importlib.util.module_from_spec(S)
S.loader.exec_module(explorer)


class ExplorerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.db = Path(cls.tmp.name) / 'demo.sqlite3'
        con = sqlite3.connect(cls.db)
        try:
            con.execute('CREATE TABLE roles ('
                        'id TEXT PRIMARY KEY,title TEXT,team TEXT,department TEXT,location TEXT,'
                        'workplace_type TEXT,is_remote INTEGER,published_at TEXT,job_url TEXT,apply_url TEXT,'
                        'description_plain TEXT,raw_json TEXT,canonical_json TEXT,provenance_json TEXT)')
            rows = [
                ('a','Technical Support','IT','IT','Seattle','OnSite',0,'2026-10-01','https://example.org/a','https://example.org/a/app','Troubleshooting APIs', '{}','{}','{"source":"test"}'),
                ('b','Security Engineer','Security','Infra','US - Remote','Remote',1,'2026-10-02','https://example.org/b',None,'Security audits','{}','{}','{}'),
                ('c','Hybrid Support','IT','IT','San Francisco','Hybrid',1,'2026-10-03','https://example.org/c',None,'Support and scripting','{}','{}','{}'),
                ('d','<img src=x onerror=alert(1)>','Other','Other','Unknown',None,None,'2026-10-04',None,None,'This is user provided','{}','{}','{}'),
            ]
            con.executemany('INSERT INTO roles VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', rows)
            con.commit()
        finally:
            con.close()
        cls.server = explorer.create_server(cls.db, port=0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = 'http://127.0.0.1:' + str(cls.server.server_address[1])

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=5)
        cls.server.server_close()
        cls.tmp.cleanup()

    def test_full_total(self):
        self.assertEqual(explorer.get_stats(self.db)['total'], 4)

    def test_default_query(self):
        result = explorer.query_roles(self.db)
        self.assertEqual(result['total'], 4)
        self.assertEqual(len(result['roles']), 4)

    def test_location_filter(self):
        self.assertEqual(explorer.query_roles(self.db, location='Seattle')['roles'][0]['id'], 'a')

    def test_team_filter(self):
        self.assertEqual(explorer.query_roles(self.db, team='IT')['total'], 2)

    def test_unknown_remote(self):
        result = explorer.query_roles(self.db, remote='unknown')
        self.assertEqual([r['id'] for r in result['roles']], ['d'])

    def test_remote_flag_not_equated_to_workplace(self):
        result = explorer.query_roles(self.db, remote='true')
        self.assertEqual(result['total'], 2)
        self.assertEqual({r['workplace_type'] for r in result['roles']}, {'Remote','Hybrid'})

    def test_literal_sql_search_wildcard(self):
        self.assertEqual(explorer.query_roles(self.db, search='%')['total'], 0)

    def test_sql_injection_is_not_executed(self):
        self.assertEqual(explorer.query_roles(self.db, search="' OR 1=1 --")['total'], 0)
        self.assertEqual(explorer.get_stats(self.db)['total'], 4)

    def test_sort_whitelist(self):
        result = explorer.query_roles(self.db, sort='title; DROP TABLE roles;--')
        self.assertEqual(result['total'], 4)
        self.assertEqual(explorer.get_stats(self.db)['total'], 4)

    def test_page_limited(self):
        result = explorer.query_roles(self.db, page=1, page_size=2)
        self.assertEqual(len(result['roles']), 2)
        self.assertEqual(explorer.query_roles(self.db, page=2, page_size=2)['total'],4)

    def test_detail_provenance(self):
        self.assertEqual(explorer.get_role(self.db, 'a')['provenance_json']['source'], 'test')

    def test_missing_role(self):
        self.assertIsNone(explorer.get_role(self.db, 'nonexistent'))

    def test_read_only_connection(self):
        with explorer.closing(explorer.connect_db(self.db)) as con:
            with self.assertRaises(sqlite3.OperationalError):
                con.execute('DELETE FROM roles')

    def test_web_stats(self):
        with urlopen(self.base+'/api/stats') as response:
            self.assertEqual(response.status,200)
            self.assertEqual(json.load(response)['total'],4)
            self.assertIn('no-store',response.headers['Cache-Control'])

    def test_web_search(self):
        with urlopen(self.base+'/api/roles?q=Support') as response:
            self.assertEqual(json.load(response)['total'],2)

    def test_web_role_detail(self):
        with urlopen(self.base+'/api/roles/a') as response:
            self.assertIn('Troubleshooting APIs',json.load(response)['description_plain'])

    def test_frontend_uses_textcontent_for_data(self):
        code = (MODULE.parent/'app.js').read_text('utf-8')
        self.assertIn('textContent',code)
        self.assertNotIn('innerHTML',code)

    def test_html_has_security_headers(self):
        with urlopen(self.base+'/') as r:
            self.assertIn("script-src 'self'",r.headers['Content-Security-Policy'])
            self.assertIn('Role Explorer',r.read().decode())

    def test_schema_rejected(self):
        bad = Path(self.tmp.name)/'bad.db'
        con = sqlite3.connect(bad)
        con.execute('CREATE TABLE roles (id TEXT)')
        con.close()
        with self.assertRaisesRegex(ValueError,'missing'):
            explorer.validate_db(bad)


if __name__ == '__main__':
    unittest.main(verbosity=2)

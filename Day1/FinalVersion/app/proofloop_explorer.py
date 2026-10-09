"""Read-only, localhost ProofLoop role explorer for the Stage 3 SQLite dataset.

Python 3.10+ standard library only. No API keys, network fetch, or DB mutations.
"""
from __future__ import annotations

import argparse
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import json
import sqlite3
import threading
import webbrowser

ROOT = Path(__file__).resolve().parent
DEFAULT_DB = (ROOT.parent / 'runs' / 'openai_live_sqlite_001' / 'db' / 'jobs.sqlite3')
SORTS = {
    'title': 'title COLLATE NOCASE ASC, id ASC',
    'title_desc': 'title COLLATE NOCASE DESC, id ASC',
    'newest': 'published_at DESC, id ASC',
    'team': 'team COLLATE NOCASE ASC, title COLLATE NOCASE ASC',
    'location': 'location COLLATE NOCASE ASC, title COLLATE NOCASE ASC',
}
REQUIRED = {'id', 'title', 'team', 'location', 'workplace_type', 'is_remote',
            'published_at', 'job_url', 'apply_url', 'description_plain',
            'raw_json', 'canonical_json', 'provenance_json'}


def connect_db(db: Path) -> sqlite3.Connection:
    """Never connect in read-write/create mode; callers MUST close the handle."""
    con = sqlite3.connect(db.resolve().as_uri() + '?mode=ro', uri=True, timeout=5)
    con.row_factory = sqlite3.Row
    con.execute('PRAGMA query_only=ON')
    return con


def validate_db(db: Path) -> None:
    if not db.is_file():
        raise ValueError(f'Database not found: {db}')
    with closing(connect_db(db)) as con:
        found = {r['name'] for r in con.execute('PRAGMA table_info(roles)')}
        missing = REQUIRED - found
        if missing:
            raise ValueError('Incompatible database: roles columns missing: ' + ', '.join(sorted(missing)))
        con.execute('SELECT COUNT(*) FROM roles').fetchone()


def _like(value: str) -> str:
    return ('%' + value.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_') + '%')


def query_roles(db: Path, *, search: str = '', team: str = '', location: str = '',
                workplace: str = '', remote: str = '', sort: str = 'title',
                page: int = 1, page_size: int = 20) -> dict:
    if sort not in SORTS:
        sort = 'title'
    page = max(1, min(page, 100000))
    page_size = max(1, min(page_size, 50))
    search, team, location = search[:120], team[:120], location[:120]
    terms, params = [], []
    if search:
        terms.append("(title LIKE ? ESCAPE '\\' OR team LIKE ? ESCAPE '\\' OR description_plain LIKE ? ESCAPE '\\')")
        params.extend([_like(search)] * 3)
    if team:
        terms.append('team = ?')
        params.append(team)
    if location:
        terms.append('location LIKE ? ESCAPE \'\\\'')
        params.append(_like(location))
    if workplace:
        terms.append('workplace_type = ?')
        params.append(workplace)
    if remote == 'true':
        terms.append('is_remote = 1')
    elif remote == 'false':
        terms.append('is_remote = 0')
    elif remote == 'unknown':
        terms.append('is_remote IS NULL')
    where = ' WHERE ' + ' AND '.join(terms) if terms else ''
    with closing(connect_db(db)) as con:
        total = con.execute('SELECT COUNT(*) FROM roles' + where, params).fetchone()[0]
        rows = con.execute(
            'SELECT id,title,team,department,location,workplace_type,is_remote,'
            'published_at,job_url FROM roles' + where +
            ' ORDER BY ' + SORTS[sort] + ' LIMIT ? OFFSET ?',
            [*params, page_size, (page - 1) * page_size]
        ).fetchall()
    return {'total': total, 'page': page, 'page_size': page_size,
            'roles': [dict(row) for row in rows]}


def get_role(db: Path, role_id: str) -> dict | None:
    if len(role_id) > 100:
        return None
    with closing(connect_db(db)) as con:
        row = con.execute('SELECT id,title,team,department,location,workplace_type,'
                          'is_remote,published_at,job_url,apply_url,description_plain,'
                          'raw_json,canonical_json,provenance_json FROM roles WHERE id=?', (role_id,)).fetchone()
    if not row:
        return None
    data = dict(row)
    for key in ('raw_json', 'canonical_json', 'provenance_json'):
        try:
            data[key] = json.loads(data[key])
        except (ValueError, TypeError):
            data[key] = {'parse_warning': f'{key} unavailable'}
    return data


def get_stats(db: Path) -> dict:
    with closing(connect_db(db)) as con:
        count = con.execute('SELECT COUNT(*) FROM roles').fetchone()[0]
        teams = [r['team'] for r in con.execute(
            'SELECT DISTINCT team FROM roles WHERE team IS NOT NULL AND TRIM(team) != "" ORDER BY team COLLATE NOCASE')]
        workplace = [dict(r) for r in con.execute(
            'SELECT COALESCE(workplace_type,"Unknown") label, COUNT(*) count FROM roles '
            'GROUP BY COALESCE(workplace_type,"Unknown") ORDER BY count DESC')]
        remotes = [dict(r) for r in con.execute(
            'SELECT COALESCE(CAST(is_remote AS TEXT),"Unknown") label,COUNT(*) count '
            'FROM roles GROUP BY COALESCE(CAST(is_remote AS TEXT),"Unknown") ORDER BY count DESC')]
    return {'total': count, 'teams': teams, 'workplace': workplace, 'remote_flags': remotes,
            'notice': 'Remote metadata is not proof of Utah eligibility or actual offsite permission.'}


class ExplorerHandler(BaseHTTPRequestHandler):
    db_path: Path  # supplied through handler factory

    def _send(self, body: bytes, content_type: str, status: int = 200):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; object-src 'none'; base-uri 'none'")
        self.send_header('X-Frame-Options', 'DENY')
        self.end_headers()
        self.wfile.write(body)

    def json(self, obj, status=200):
        self._send(json.dumps(obj, ensure_ascii=False, default=str).encode('utf-8'),
                   'application/json; charset=utf-8', status)

    def do_GET(self):
        route = urlsplit(self.path)
        try:
            if route.path == '/' or route.path == '/index.html':
                self._send((ROOT / 'index.html').read_bytes(), 'text/html; charset=utf-8')
            elif route.path == '/app.css':
                self._send((ROOT / 'app.css').read_bytes(), 'text/css; charset=utf-8')
            elif route.path == '/app.js':
                self._send((ROOT / 'app.js').read_bytes(), 'application/javascript; charset=utf-8')
            elif route.path == '/api/stats':
                self.json(get_stats(self.db_path))
            elif route.path == '/api/roles':
                q = parse_qs(route.query)
                one = lambda k, d='': q.get(k, [d])[0]
                try:
                    page = int(one('page', '1'))
                except ValueError:
                    page = 1
                self.json(query_roles(self.db_path, search=one('q'), team=one('team'),
                                      location=one('location'), workplace=one('workplace'),
                                      remote=one('remote'), sort=one('sort', 'title'), page=page))
            elif route.path.startswith('/api/roles/'):
                role_id = route.path[len('/api/roles/'):]
                role = get_role(self.db_path, role_id)
                if role:
                    self.json(role)
                else:
                    self.json({'error': 'Role not found'}, 404)
            else:
                self.json({'error': 'Not found'}, 404)
        except (OSError, sqlite3.Error, ValueError) as exc:
            self.json({'error': 'Data unavailable', 'detail': str(exc)}, 500)

    def log_message(self, fmt, *args):
        pass


def create_server(db: Path, host: str = '127.0.0.1', port: int = 8765) -> ThreadingHTTPServer:
    validate_db(db)
    class Handler(ExplorerHandler):
        db_path = db
    return ThreadingHTTPServer((host, port), Handler)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Run the read-only, localhost ProofLoop role explorer')
    ap.add_argument('--db', type=Path, default=DEFAULT_DB)
    ap.add_argument('--port', type=int, default=8765)
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--open', action='store_true', help='Open browser automatically')
    args = ap.parse_args(argv)
    if args.host not in ('127.0.0.1', 'localhost'):
        ap.error('The portfolio demo binds to localhost only; no authentication is provided')
    try:
        server = create_server(args.db, args.host, args.port)
    except (ValueError, OSError, sqlite3.Error) as exc:
        ap.error(str(exc))
    url = f'http://127.0.0.1:{server.server_address[1]}/'
    print(f'ProofLoop Role Explorer: {url}', flush=True)
    print(f'Read-only SQLite: {args.db.resolve()}', flush=True)
    print('Press Ctrl+C to stop. This demo makes no network requests.', flush=True)
    if args.open:
        threading.Timer(0.3, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

"""End-to-end self-test for the server-game template.

Covers: HTTP admin login/permission pages, full TCP game protocol
(register/login/hb/maps/move/walk/say/who), GM flows with live pushes
(grant gold, level-up, ban, kick), announce push, tick-flush persistence
and capped offline settlement -- 42 assertions. Stdlib urllib/socket only.

Usage (run from the SERVER directory, so it can open data/app.db):
  1. stop the server, then delete data/app.db* for a fresh database
  2. start the server:  ./server-game.exe   (127.0.0.1:8099 / 7100)
  3. run:               python tools/e2e.py

The probe registers fresh game accounts (alice / bob) over the TCP
protocol, so it needs the seeded admin (admin/admin1234) and an empty
game_player table -- rerunning against a used database fails at register.
"""
import sys
import time
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8099"

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **kw):
        return None

opener = urllib.request.build_opener(NoRedirect)
GAME = ("127.0.0.1", 7100)
checks = 0

def ok(cond, label):
    global checks
    checks += 1
    mark = "PASS" if cond else "FAIL"
    print(f"[{mark}] {label}")
    if not cond:
        sys.exit(1)

def http(path, data=None, cookie=None):
    req = urllib.request.Request(BASE + path)
    if cookie:
        req.add_header("Cookie", cookie)
    body = None
    if data is not None:
        body = urllib.parse.urlencode(data).encode()
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        resp = opener.open(req, body, timeout=10)
        text = resp.read().decode("utf-8", "replace")
        return resp.status, text, resp.headers.get_all("Set-Cookie") or []
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), e.headers.get_all("Set-Cookie") or []

class Client:
    def __init__(self):
        self.sock = socket.create_connection(GAME, timeout=10)
        self.buf = ""

    def send(self, obj):
        self.sock.sendall((json.dumps(obj) + "\n").encode())

    def recv(self, timeout=5.0):
        self.sock.settimeout(timeout)
        deadline = time.time() + timeout
        while "\n" not in self.buf:
            remain = deadline - time.time()
            if remain <= 0:
                return None
            try:
                chunk = self.sock.recv(4096)
            except socket.timeout:
                return None
            if not chunk:
                return None
            self.buf += chunk.decode("utf-8", "replace")
        line, self.buf = self.buf.split("\n", 1)
        return json.loads(line)

    def drain(self, seconds=1.5):
        out = []
        while True:
            m = self.recv(timeout=seconds)
            if m is None:
                return out
            out.append(m)

    def expect_closed(self, seconds=5.0):
        deadline = time.time() + seconds
        while time.time() < deadline:
            m = self.recv(timeout=1.0)
            if m is None:
                return True
            if m.get("ev") == "kick":
                continue
        return False

def main():
    # --- HTTP admin surface -------------------------------------------------
    status, html, _ = http("/")
    ok(status == 200 and "游戏服务器运行中" in html, "landing page renders")
    status, html, _ = http("/admin")
    ok(status in (301, 302, 303) or "登录" in html, "/admin redirects to login")
    status, html, cookies = http("/admin/login", data={"user": "admin", "pass": "admin1234"})
    cookie = cookies[0].split(";")[0] if cookies else ""
    ok(status == 302 and cookie != "", "admin login sets session cookie")
    for path, marker in [
        ("/admin", "在线会话"),
        ("/admin/game/players", "玩家管理"),
        ("/admin/game/online", "当前在线"),
        ("/admin/game/announces", "公告管理"),
        ("/admin/monitor", "运行监控"),
        ("/admin/system/users", "账号管理"),
    ]:
        status, html, _ = http(path, cookie=cookie)
        ok(status == 200 and marker in html, f"GET {path} shows {marker}")

    # --- TCP game protocol --------------------------------------------------
    alice = Client()
    hello = alice.recv()
    ok(hello and hello.get("ev") == "hello", "gateway greets on connect")
    alice.send({"op": "register", "user": "alice", "pass": "secret1", "nick": "爱丽丝"})
    r = alice.recv()
    ok(r and r.get("ok") == 1, "register alice")
    alice.send({"op": "register", "user": "alice", "pass": "secret1"})
    r = alice.recv()
    ok(r and r.get("ok") == 0, "duplicate register rejected")
    alice.send({"op": "login", "user": "alice", "pass": "wrongpw"})
    r = alice.recv()
    ok(r and r.get("ok") == 0 and "不正确" in r.get("err", ""), "wrong password rejected")
    alice.send({"op": "login", "user": "alice", "pass": "secret1"})
    r = alice.recv()
    ok(r and r.get("ok") == 1 and r.get("self", {}).get("name") == "爱丽丝", "login alice with self state")
    ok(len(r.get("maps", [])) == 5, "login carries open map list")
    ok(r.get("announce", {}).get("title", "") != "", "login carries latest announce")
    uid_alice = r["self"]["uid"]

    alice.send({"op": "hb"})
    r = alice.recv()
    ok(r and r.get("ok") == 1 and r.get("online") == 1, "heartbeat reports online count")
    alice.send({"op": "say", "text": "大家好"})
    alice.send({"op": "walk", "x": 30, "y": 40})
    walked = False
    for m in alice.drain(1.5):
        if m.get("ev") == "walk" and m.get("x") == 30:
            walked = True
    ok(walked, "walk echoes to same-map players")

    bob = Client()
    bob.recv()
    bob.send({"op": "register", "user": "bob", "pass": "secret2", "nick": "鲍勃"})
    bob.recv()
    bob.send({"op": "login", "user": "bob", "pass": "secret2"})
    r = bob.recv()
    ok(r and r.get("ok") == 1, "login bob")
    uid_bob = r["self"]["uid"]

    bob.send({"op": "say", "text": "你们好"})
    chat = alice.recv()
    ok(chat and chat.get("ev") == "chat" and chat.get("from") == "鲍勃", "world chat reaches other sessions")
    alice.send({"op": "who"})
    r = alice.recv()
    names = [row["name"] for row in r.get("rows", [])]
    ok("鲍勃" in names and "爱丽丝" in names, "who lists same-map players")

    def reply_for(client, send_obj=None, seconds=3.0):
        if send_obj:
            client.send(send_obj)
        deadline = time.time() + seconds
        while time.time() < deadline:
            m = client.recv(timeout=1.0)
            if m is not None and ("ok" in m or "err" in m):
                return m
        return None

    bob.drain(1.0)
    r = reply_for(bob, {"op": "move", "map": 5})
    ok(r and r.get("ok") == 0, "level gate blocks high map")
    r = reply_for(bob, {"op": "move", "map": 2})
    ok(r and r.get("ok") == 0, "level gate blocks mid map")
    # GM levels bob up; the online session must see the new level immediately
    status, html, _ = http("/admin/game/players/save", cookie=cookie, data={
        "id": str(uid_bob), "nickname": "鲍勃", "job": "1",
        "level": "8", "gold": "50", "gems": "0",
        "mapId": "1", "status": "1", "banReason": ""})
    ok(status == 200, "gm level edit accepted")
    lvl, gld = None, None
    for m in bob.drain(2.0):
        if m.get("ev") == "state":
            lvl, gld = m["self"]["level"], m["self"]["gold"]
    ok(lvl == 8 and gld == 50, "gm edit pushes level and gold to the online client")
    r = reply_for(bob, {"op": "move", "map": 2})
    ok(r and r.get("ok") == 1 and r["self"]["map"] == 2, "move to allowed map")
    moved = False
    for m in alice.drain(2.0):
        if m.get("ev") == "move" and "沃玛森林" in m.get("text", ""):
            moved = True
    ok(moved, "move broadcast reaches other players")
    alice.send({"op": "who"})
    r = alice.recv()
    ok("鲍勃" not in [row["name"] for row in r.get("rows", [])], "who no longer shows bob after map change")

    # --- GM actions ----------------------------------------------------------
    status, html, _ = http("/admin/game/online", cookie=cookie)
    ok(status == 200 and "爱丽丝" in html, "online page lists live sessions")

    # grant gold to online alice (form save applies delta via World and pushes state)
    status, html, _ = http("/admin/game/players/form?id=%d" % uid_alice, cookie=cookie)
    ok(status == 200 and "在线" in html, "form marks online player")
    gold_now = None
    alice.send({"op": "state"})
    for m in alice.drain(1.5):
        if m.get("ev") == "state":
            gold_now = m["self"]["gold"]
    status, html, _ = http("/admin/game/players/save", cookie=cookie, data={
        "id": str(uid_alice), "nickname": "爱丽丝", "job": "0",
        "level": "8", "gold": str((gold_now or 0) + 777), "gems": "5",
        "mapId": "1", "status": "1", "banReason": ""})
    ok(status == 200, "players/save accepts grant")
    got = None
    for m in alice.drain(2.0):
        if m.get("ev") == "state" and m["self"]["gold"] == (gold_now or 0) + 777:
            got = m["self"]["gold"]
    ok(got is not None, "online grant pushes new gold to the client")

    # broadcast + announce push
    status, html, _ = http("/admin/game/online/broadcast", cookie=cookie, data={"text": "全服活动开启"})
    ok(status == 200, "broadcast accepted")
    seen = {"alice": False, "bob": False}
    for m in alice.drain(1.5):
        if m.get("ev") == "chat" and m.get("text") == "全服活动开启":
            seen["alice"] = True
    for m in bob.drain(1.5):
        if m.get("ev") == "chat" and m.get("text") == "全服活动开启":
            seen["bob"] = True
    ok(seen["alice"] and seen["bob"], "broadcast reaches all sessions")

    # kick bob via online page (cid)
    status, html, _ = http("/admin/game/online", cookie=cookie)
    import re
    mrow = re.search(r'data-args="cid=(\d+)"', html)
    cid = int(mrow.group(1)) if mrow else 0
    ok(cid > 0, "online page exposes session cid")
    status, html, _ = http("/admin/game/online/kick", cookie=cookie, data={"cid": str(cid)})
    ok(status == 200, "kick accepted")
    ok(bob.expect_closed(), "kicked session is closed")

    # ban alice (must close her session too)
    status, html, _ = http("/admin/game/players/save", cookie=cookie, data={
        "id": str(uid_alice), "nickname": "爱丽丝", "job": "0",
        "level": "8", "gold": "1000", "gems": "5",
        "mapId": "1", "status": "0", "banReason": "测试封禁"})
    ok(status == 200, "ban accepted")
    ok(alice.expect_closed(), "banned online session is closed")
    banned = Client()
    banned.recv()
    banned.send({"op": "login", "user": "alice", "pass": "secret1"})
    r = banned.recv()
    ok(r and r.get("ok") == 0 and "封禁" in r.get("err", ""), "banned login refused with reason")

    # persistence: gold survived the kick/ban cycle (flush 10s) — check via players page
    time.sleep(11)
    status, html, _ = http("/admin/game/players?kw=alice", cookie=cookie)
    ok(status == 200 and "1000" in html, "grant persisted to the database")
    # unban for a clean rerun
    http("/admin/game/players/save", cookie=cookie, data={
        "id": str(uid_alice), "nickname": "爱丽丝", "job": "0",
        "level": "8", "gold": "1000", "gems": "5",
        "mapId": "1", "status": "1", "banReason": ""})

    # offline settlement: backdate alice's logout by 2h, relogin, gold +1000 (cap 12h, 500/h)
    import sqlite3
    db = sqlite3.connect("data/app.db")
    db.execute("UPDATE game_player SET \"lastLogoutAt\"=?, gold=100, status=1, \"banReason\"='' WHERE id=?", (int(time.time()) - 7200, uid_alice))
    db.commit(); db.close()
    pay = Client()
    pay.recv()
    pay.send({"op": "login", "user": "alice", "pass": "secret1"})
    r = pay.recv()
    ok(r and r.get("ok") == 1 and r["self"]["gold"] == 1100 and r["offline"]["gold"] == 1000,
       "offline settlement grants capped gold on login")
    pay.sock.close()

    print(f"ALL PASS checks={checks}")

if __name__ == "__main__":
    main()

"""End-to-end self-test for the realm-based server-game template.

Covers the full player flow AND the combat loop: web register/forgot (3-step
with security question, wrong-answer lockout), TCP realms/register/login/
characters/create/enter, realm-scoped chat/walk/who, realm switch with
character state kept, GM realm CRUD with maintain gating, account ban +
kick, online grant pushes, announce push, pro-rata capped offline
settlement, then the full hunt loop -- mob list, manual hunt with
exp/levelup/gold/drops, shop buy/sell, potion use, weapon equip/takeoff,
per-tick auto-hunt events, death respawn in town, GM item gift (online
push + offline grant) and DB persistence of hp/exp/equipped weapon/bag --
106 assertions. Stdlib urllib/socket only.

Run from the SERVER directory against a FRESH data/app.db:
  1. stop server, delete data/app.db*, start server
  2. python tools/e2e.py
"""
import json
import socket
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8099"
GAME = ("127.0.0.1", 7100)
checks = 0

T0 = time.time()

def ok(cond, label):
    global checks
    checks += 1
    print(f"[{time.time()-T0:7.1f}s] [{'PASS' if cond else 'FAIL'}] {label}")
    if not cond:
        print("ALL FAIL at", checks)
        sys.exit(1)

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **kw):
        return None

opener = urllib.request.build_opener(NoRedirect)

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
        return resp.status, resp.read().decode("utf-8", "replace"), \
            resp.headers.get_all("Set-Cookie") or []
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), \
            e.headers.get_all("Set-Cookie") or []

def gm(path, data, cookie):
    status, text, _ = http(path, data=data, cookie=cookie)
    try:
        return status, json.loads(text), text
    except Exception:
        return status, {"raw": text}, text

class Client:
    def __init__(self):
        self.sock = socket.create_connection(GAME, timeout=10)
        self.buf = b""
        self.pending = []
        self.verbose = False

    def send(self, obj):
        self.sock.sendall((json.dumps(obj, ensure_ascii=False) + "\n").encode())

    def _fill(self, timeout):
        self.sock.settimeout(timeout)
        got = False
        try:
            while True:
                d = self.sock.recv(4096)
                if not d:
                    return False
                self.buf += d
                while b"\n" in self.buf:
                    line, self.buf = self.buf.split(b"\n", 1)
                    if line.strip():
                        m = json.loads(line)
                        self.pending.append(m)
                        got = True
                        if self.verbose:
                            print(f"[{time.time()-T0:7.1f}s] RX {json.dumps(m, ensure_ascii=False)[:220]}")
                if got:
                    return True
        except socket.timeout:
            pass
        except OSError:
            return False
        return True

    def recv(self, timeout=5):
        if self.pending:
            return self.pending.pop(0)
        self._fill(timeout)
        return self.pending.pop(0) if self.pending else None

    def reply_for(self, pred, timeout=5):
        """Next message matching pred; other lines stay queued."""
        for i, m in enumerate(self.pending):
            if pred(m):
                return self.pending.pop(i)
        deadline = time.time() + timeout
        while time.time() < deadline:
            if not self._fill(max(0.1, deadline - time.time())):
                break
            for i, m in enumerate(self.pending):
                if pred(m):
                    return self.pending.pop(i)
        return None

    def ok_for(self, op_extra=None, timeout=5):
        def pred(m):
            return m.get("ok") == 1 and (op_extra is None or op_extra(m))
        return self.reply_for(pred, timeout)

    def err_for(self, needle, timeout=5):
        def pred(m):
            return m.get("ok") == 0 and needle in (m.get("err") or "")
        return self.reply_for(pred, timeout)

    def ev(self, name, timeout=5):
        def pred(m):
            return m.get("ev") == name
        return self.reply_for(pred, timeout)

    def closed(self, timeout=3):
        return not self._fill(timeout) and not self.pending

    def drop(self):
        try:
            self.sock.close()
        except OSError:
            pass

def tcp():
    return Client()

# ---------- 1. 落地页与公共页面 ----------
st, html, _ = http("/")
ok(st == 200 and "一区·雷霆之怒" in html and "三区·战神殿" in html,
   "landing lists seeded realms")
ok("开放 2 / 共 3" in html and "维护" in html, "landing shows realm states")
ok("注册账号" in html and "找回密码" in html, "landing links register/forgot")
st, html, _ = http("/register")
ok(st == 200 and 'action="/register"' in html and "密保问题" in html,
   "register page renders")
st, html, _ = http("/forgot")
ok(st == 200 and 'action="/forgot"' in html, "forgot page renders")

# ---------- 2. 网页注册 ----------
st, html, _ = http("/register", data={
    "user": "al", "pass": "secret1", "pass2": "secret1",
    "question": "出生城市", "answer": "北京"})
ok("账号需 3-32 字" in html, "web register rejects short username")
st, html, _ = http("/register", data={
    "user": "alice", "pass": "secret1", "pass2": "different",
    "question": "出生城市", "answer": "北京"})
ok("两次输入的密码不一致" in html, "web register rejects mismatched pass")
st, html, _ = http("/register", data={
    "user": "alice", "pass": "secret1", "pass2": "secret1",
    "question": "出生城市", "answer": "北京"})
ok("注册成功" in html and "alice" in html, "web register creates alice")
st, html, _ = http("/register", data={
    "user": "alice", "pass": "secret1", "pass2": "secret1",
    "question": "出生城市", "answer": "北京"})
ok("账号已存在" in html, "web register rejects duplicate")

# ---------- 3. 网页找回密码 ----------
st, html, _ = http("/forgot", data={"user": "ghost"})
ok("账号不存在或未设置密保" in html, "forgot hides unknown accounts")
st, html, _ = http("/forgot", data={"user": "alice"})
ok("出生城市" in html and 'name="user"' in html, "forgot step2 shows question")
st, html, _ = http("/forgot/reset", data={
    "user": "alice", "answer": "上海", "newpass": "newpass99",
    "newpass2": "newpass99"})
ok("密保答案不正确" in html, "forgot rejects wrong answer")
st, html, _ = http("/forgot/reset", data={
    "user": "alice", "answer": "北京", "newpass": "newpass99",
    "newpass2": "newpass99"})
ok("密码已重置" in html, "forgot resets with correct answer")

# 密保答错限频：mallory 连错 5 次后锁定，正确答案也被拒
mallory = tcp()
mallory.send({"op": "register", "user": "mallory", "pass": "mallory1",
              "question": "小学校名", "answer": "实验小学"})
ok(mallory.ok_for() is not None, "TCP register mallory")
mallory.drop()
for i in range(5):
    st, html, _ = http("/forgot/reset", data={
        "user": "mallory", "answer": "错误答案", "newpass": "pass123",
        "newpass2": "pass123"})
    ok("密保答案不正确" in html, f"mallory wrong answer #{i+1}")
# 第 6 次（无论答案对错）都落在锁定窗口内
st, html, _ = http("/forgot/reset", data={
    "user": "mallory", "answer": "错误答案", "newpass": "pass123",
    "newpass2": "pass123"})
ok("错误次数过多" in html, "forgot locks after 5 wrong answers")
st, html, _ = http("/forgot/reset", data={
    "user": "mallory", "answer": "实验小学", "newpass": "pass123",
    "newpass2": "pass123"})
ok("错误次数过多" in html, "lockout applies even to correct answer")

# ---------- 4. TCP 账号/选区/建角 ----------
bob = tcp()
hello = bob.recv()
ok(hello and hello.get("ev") == "hello", "gateway greets on connect")
bob.send({"op": "realms"})
r = bob.ok_for(lambda m: len(m.get("realms", [])) == 3)
ok(r and r["realms"][2]["state"] == 1 and r["realms"][0]["name"] == "一区·雷霆之怒",
   "realms op lists 3 realms with states")
bob.send({"op": "register", "user": "bob", "pass": "short",
          "question": "旧手机号", "answer": "8888"})
ok(bob.err_for("密码需 6-64 字") is not None, "TCP register rejects short pass")
bob.send({"op": "register", "user": "bob", "pass": "secret1",
          "question": "宠物名字", "answer": "旺财"})
ok(bob.ok_for() is not None, "TCP register bob")
bob.send({"op": "register", "user": "bob", "pass": "secret1",
          "question": "宠物名字", "answer": "旺财"})
ok(bob.err_for("账号已存在") is not None, "TCP register rejects duplicate")
bob.send({"op": "login", "user": "bob", "pass": "wrong!!"})
ok(bob.err_for("账号或密码不正确") is not None, "login error is uniform")
bob.send({"op": "login", "user": "bob", "pass": "secret1"})
r = bob.ok_for(lambda m: "uid" in m and "realms" in m)
ok(r is not None, "login returns uid + realm list")
bob.send({"op": "say", "text": "hi"})
ok(bob.err_for("请先选择区服进入") is not None, "world ops gated before enter")
bob.send({"op": "enter", "realm": 999})
ok(bob.err_for("区服不存在或维护中") is not None, "unknown realm refused")
bob.send({"op": "enter", "realm": 3})
ok(bob.err_for("区服不存在或维护中") is not None, "maintained realm refused")
bob.send({"op": "enter", "realm": 1})
r = bob.reply_for(lambda m: m.get("ok") == 0 and m.get("needCreate") == 1)
ok(r is not None, "enter without character answers needCreate")
bob.send({"op": "characters", "realm": 1})
r = bob.ok_for(lambda m: m.get("rows") == [])
ok(r is not None, "characters empty before create")
bob.send({"op": "create", "realm": 1, "name": "刀", "job": 0})
ok(bob.err_for("角色名需 2-16 字") is not None, "create rejects 1-char name")
bob.send({"op": "create", "realm": 1, "name": "刀狂", "job": 9})
ok(bob.err_for("职业不合法") is not None, "create rejects bad job")
bob.send({"op": "create", "realm": 1, "name": "刀狂", "job": 0})
r = bob.ok_for(lambda m: m.get("self", {}).get("uid", 0) > 0
               and m["self"]["realm"] == 1 and "maps" in m)
ok(r is not None, "create enters world with self+maps")
bob_uid = r["self"]["uid"]
ok(bob.reply_for(lambda m: m.get("ev") == "move") is not None,
   "create broadcasts realm move event")

# alice 用网页重置后的新密码走 TCP，与 bob 同区
alice = tcp()
alice.recv()
alice.send({"op": "login", "user": "alice", "pass": "newpass99"})
ok(alice.ok_for() is not None, "alice logs in with web-reset password")
alice.send({"op": "create", "realm": 1, "name": "法萌", "job": 1})
r = alice.ok_for(lambda m: m.get("self", {}).get("job") == 1)
ok(r is not None, "alice creates mage in realm 1")
alice.send({"op": "create", "realm": 1, "name": "法萌二号", "job": 0})
ok(alice.err_for("该区已有角色") is not None, "one character per realm")
alice.send({"op": "create", "realm": 1, "name": "刀狂", "job": 0})
ok(alice.err_for("角色名已被占用") is not None, "character names unique per realm")
alice.drop()  # alice 下线，让后面 who/在线页的世界状态可预测

# 区服广播收窄：carl 在一区收到，dave 在二区收不到
carl = tcp()
carl.recv()
carl.send({"op": "register", "user": "carl", "pass": "secret1",
           "question": "旧手机号", "answer": "8888"})
carl.reply_for(lambda m: m.get("ok") == 1)
carl.send({"op": "login", "user": "carl", "pass": "secret1"})
carl.reply_for(lambda m: m.get("ok") == 1)
carl.send({"op": "create", "realm": 1, "name": "弓长", "job": 2})
ok(carl.ok_for(lambda m: m.get("self", {}).get("uid", 0) > 0) is not None,
   "carl creates archer in realm 1")

dave = tcp()
dave.recv()
dave.send({"op": "register", "user": "dave", "pass": "secret1",
           "question": "旧手机号", "answer": "8888"})
dave.reply_for(lambda m: m.get("ok") == 1)
dave.send({"op": "login", "user": "dave", "pass": "secret1"})
dave.reply_for(lambda m: m.get("ok") == 1)
dave.send({"op": "create", "realm": 2, "name": "二区土著", "job": 0})
ok(dave.ok_for() is not None, "dave creates character in realm 2")

bob.send({"op": "say", "text": "一区的兄弟们好"})
c = carl.ev("chat")
d = dave.ev("chat")
ok(c and c.get("text") == "一区的兄弟们好" and c.get("from") == "刀狂",
   "same-realm player receives chat")
ok(d is None, "other-realm player does not receive chat")

bob.pending.clear()  # 丢弃 bob 自己的 ev 回声与旧回复，保证下面的 ok 对上本条请求
bob.send({"op": "walk", "x": 999, "y": 3})
ok(bob.ev("walk") is not None, "walk accepts clamped coords")
w = carl.ev("walk")
ok(w and w.get("x") == 511 and w.get("y") == 3, "walk clamped to walkMax and broadcast")
ok(dave.ev("walk") is None, "walk not sent to other realm")
bob.pending.clear()
bob.send({"op": "who"})
r = bob.ok_for(lambda m: "rows" in m)
ok(r and sorted(x["name"] for x in r["rows"]) == ["刀狂", "弓长"],
   "who lists same-realm same-map players only")

bob.send({"op": "move", "map": 2})
ok(bob.err_for("需要 5 级") is not None, "move gated by map minLevel")

# 换区：bob 建二区角色再切回一区，金币保持
bob.send({"op": "create", "realm": 2, "name": "刀狂二区", "job": 0})
r = bob.ok_for(lambda m: m.get("self", {}).get("realm") == 2)
ok(r is not None, "bob creates second character in realm 2")
bob.send({"op": "enter", "realm": 1})
r = bob.ok_for(lambda m: m.get("self", {}).get("realm") == 1
               and m["self"]["name"] == "刀狂")
ok(r is not None, "bob re-enters realm 1, character state kept")

# ---------- 5. GM 后台 ----------
st, html, setc = http("/admin/login", data={
    "user": "admin", "pass": "admin1234"})
cookie = ""
for c in setc:
    if c.startswith("zsession="):
        cookie = c.split(";")[0]
ok(st in (200, 302) and cookie, "admin login sets session cookie")

st, html, _ = http("/admin/game/realms", cookie=cookie)
ok(st == 200 and "一区·雷霆之怒" in html and "维护" in html,
   "GM realms page lists realms")
st, j, _ = gm("/admin/game/realms/save", {
    "name": "四区·测试", "state": "0", "sort": "9"}, cookie)
ok(j.get("code") == "0000", "GM creates realm 4")
st, html, _ = http("/admin/game/realms", cookie=cookie)
ok("四区·测试" in html, "realms page shows new realm")
b = tcp()
b.recv()
b.send({"op": "realms"})
r = b.ok_for(lambda m: len(m.get("realms", [])) == 4)
ok(r and r["realms"][3]["name"] == "四区·测试", "TCP realms shows realm 4")
b.drop()

# 维护中的三区放开后可以 enter（needCreate）
st, j, _ = gm("/admin/game/realms/save", {
    "id": "3", "name": "三区·战神殿", "state": "0", "sort": "3"}, cookie)
ok(j.get("code") == "0000", "GM opens realm 3")
bob.send({"op": "enter", "realm": 3})
r = bob.reply_for(lambda m: m.get("ok") == 0 and m.get("needCreate") == 1)
ok(r is not None, "opened realm accepts enter (needCreate)")
bob.send({"op": "enter", "realm": 1})
bob.reply_for(lambda m: m.get("ok") == 1)

# 有角色的区服删除被拒
st, j, _ = gm("/admin/game/realms/delete", {"id": "1"}, cookie)
ok(st == 400 and j.get("code") == "0409" and "角色" in j.get("msg", ""),
   "GM cannot delete realm with characters")
st, j, _ = gm("/admin/game/realms/delete", {"id": "4"}, cookie)
ok(j.get("code") == "0000", "GM deletes empty realm 4")

st, html, _ = http("/admin/game/players?kw=alice", cookie=cookie)
ok(st == 200 and "法萌" in html and "一区·雷霆之怒" in html,
   "players page shows character + realm")
st, html, _ = http("/admin/game/players/form?id=" + str(bob_uid), cookie=cookie)
ok(st == 200 and 'name="realmId"' in html and 'name="accountStatus"' in html,
   "player form has realm select + account ban")

# 发奖（角色 id 路径，离线直写库）
st, j, _ = gm("/admin/game/players/save", {
    "id": str(bob_uid), "nickname": "刀狂", "realmId": "1", "job": "0",
    "level": "6", "gold": "500", "gems": "10", "mapId": "1",
    "accountStatus": "1", "banReason": ""}, cookie)
ok(j.get("code") == "0000", "GM save character")
bob.send({"op": "state"})
# GM 保存会连发多条 state（发奖一条、编辑一条、主动查询一条），取到含终值的那条
r = None
for _ in range(6):
    m = bob.reply_for(lambda m: m.get("ev") == "state", timeout=3)
    if m and m["self"]["gold"] == 500 and m["self"]["level"] == 6:
        r = m
        break
ok(r is not None, "online grant pushed to client")

# 封禁账号：在线的 carl 被踢
st, j, _ = gm("/admin/game/players/save", {
    "id": str(bob_uid), "nickname": "刀狂", "realmId": "1", "job": "0",
    "level": "6", "gold": "500", "gems": "10", "mapId": "1",
    "accountStatus": "0", "banReason": "作弊"}, cookie)
ok(j.get("code") == "0000" and "踢下线" in j.get("msg", ""),
   "GM bans account, kicks online session")
k = bob.ev("kick")
ok(k and "封禁" in k.get("text", ""), "banned client receives kick event")
bob.drop()  # 协议约定：客户端收到 kick 自行断开，服务端在 EOF 后清理会话
bob.drop()
bob2 = tcp()
bob2.recv()
bob2.send({"op": "login", "user": "bob", "pass": "secret1"})
ok(bob2.err_for("账号已被封禁：作弊") is not None, "banned login refused with reason")
st, j, _ = gm("/admin/game/players/save", {
    "id": str(bob_uid), "nickname": "刀狂", "realmId": "1", "job": "0",
    "level": "6", "gold": "500", "gems": "10", "mapId": "1",
    "accountStatus": "1", "banReason": ""}, cookie)
ok(j.get("code") == "0000", "GM unbans bob")

st, html, _ = http("/admin/game/online", cookie=cookie)
ok(st == 200 and 'tag off">未进区' not in html and "在世界中" in html
   and "carl" in html, "online page lists sessions with stage")
st, j, _ = gm("/admin/game/online/broadcast", {"text": "全体注意，今晚开BOSS"}, cookie)
ok(j.get("code") == "0000", "GM broadcast accepted")
c = carl.ev("chat")
d = dave.ev("chat")
ok(c and "开BOSS" in c.get("text", "") and d and "开BOSS" in d.get("text", ""),
   "GM broadcast reaches all realms")

st, j, _ = gm("/admin/game/announces/save", {
    "title": "维护通知", "body": "今晚 24:00 停机维护 30 分钟。",
    "enabled": "1"}, cookie)
ok(j.get("code") == "0000", "GM creates announce")
st, html, _ = http("/admin/game/announces", cookie=cookie)
ok("推送" in html, "announces page has push action")
import re
m = re.search(r'data-args="id=(\d+)" data-confirm="把这条公告', html)
push_id = m.group(1) if m else "1"
st, j, _ = gm("/admin/game/announces/push", {"id": push_id}, cookie)
ok(j.get("code") == "0000", "GM pushes announce")
c = carl.ev("announce")
ok(c and "维护通知" in c.get("title", ""), "announce push reaches client")

st, html, _ = http("/admin", cookie=cookie)
ok(st == 200 and "游戏账号" in html and "区服" in html,
   "dashboard shows account/realm KPIs")

# ---------- 6. 持久化与离线结算 ----------
import sqlite3
time.sleep(11)  # flush 周期 10s
db = sqlite3.connect("data/app.db")
row = db.execute(
    'SELECT nickname, realmId, gold, level FROM game_player WHERE id=?',
    (bob_uid,)).fetchone()
ok(row is not None and row[0] == "刀狂" and row[1] == 1 and row[3] == 6,
   "character row persisted with realmId")
acc = db.execute(
    'SELECT question, answerHash FROM game_account WHERE username=?',
    ("alice",)).fetchone()
ok(acc is not None and acc[0] == "出生城市" and acc[1] != "北京",
   "account stores question + hashed answer")
db.close()

# 离线结算：carl 登出，回拨 2 小时，重进一区结算 2 小时挂机（500/h）
carl.drop()
time.sleep(1)
db = sqlite3.connect("data/app.db")
db.execute('UPDATE game_player SET "lastLogoutAt"=? WHERE nickname="弓长"',
           (int(time.time()) - 7200,))
db.commit()
db.close()
carl2 = tcp()
carl2.recv()
carl2.send({"op": "login", "user": "carl", "pass": "secret1"})
carl2.reply_for(lambda m: m.get("ok") == 1)
carl2.send({"op": "enter", "realm": 1})
# 结算按秒折算（500/h 按比例），时长封顶；断言 ≥2h 且收益等于折算值
def settle_ok(m):
    o = m.get("offline") or {}
    return (o.get("seconds", 0) >= 7200
            and o.get("gold") == o["seconds"] * 500 // 3600)
r = carl2.ok_for(settle_ok)
ok(r is not None, "offline settlement grants 2h idle gold on enter")
carl2.drop()
dave.drop()
alice.drop()

# ---------- 7. 战斗闭环：打怪/升级/掉落/背包/商店/挂机/死亡 ----------
h = tcp()
h.verbose = True
h.recv()
h.send({"op": "register", "user": "hunter", "pass": "secret1",
        "question": "旧手机号", "answer": "8888"})
h.reply_for(lambda m: m.get("ok") == 1)
h.send({"op": "login", "user": "hunter", "pass": "secret1"})
h.reply_for(lambda m: m.get("ok") == 1)
h.send({"op": "create", "realm": 1, "name": "小猎手", "job": 0})
r = h.ok_for(lambda m: "self" in m)
ok(r is not None, "hunter creates fighter")
hunter_uid = r["self"]["uid"]
s0 = r["self"]
ok(s0["hp"] == s0["maxhp"] and s0["level"] == 1,
   "create starts with full hp at level 1")

h.send({"op": "mobs"})
r = h.ok_for(lambda m: "rows" in m)
scare = [x for x in r["rows"] if x["name"] == "稻草人"]
ok(len(r["rows"]) >= 3 and len(scare) == len(r["rows"])
   and all(x["alive"] == 1 for x in scare),
   "mobs lists alive scarecrows on newbie map")

# 打到升级：稻草人 exp 15 = ExpNext(1)，首杀必升级
for _ in range(4):
    h.send({"op": "hunt", "mob": scare[0]["tpl"]})
    r = h.ok_for(lambda m: "fight" in m)
    if r["self"]["level"] >= 2:
        break
ok(r is not None and r["self"]["level"] == 2 and r["self"]["maxhp"] == 100,
   "first kill levels up and raises max hp")
h.send({"op": "bag"})
r = h.ok_for(lambda m: "items" in m)
pelts = [i for i in r["items"] if i["name"] == "兽皮"]
ok(len(pelts) == 1 and pelts[0]["count"] >= 1,
   "scarecrow drop lands in bag")

# 商店：查目录拿物品 id，买药用金币，卖皮回收
h.send({"op": "shop"})
r = h.ok_for(lambda m: "shop" in m)
shop = {i["name"]: i["id"] for i in r["shop"]}
ok("金创药(小)" in shop and "铁剑" in shop and "兽皮" not in shop,
   "shop sells potions and gear, not materials")
st, j, _ = gm("/admin/game/players/save", {
    "id": str(hunter_uid), "nickname": "小猎手", "realmId": "1", "job": "0",
    "level": "5", "gold": "1000", "gems": "0", "mapId": "1",
    "accountStatus": "1", "banReason": ""}, cookie)
ok(j.get("code") == "0000", "GM tops up gold for shop test")
h.send({"op": "state"})
r = h.reply_for(lambda m: m.get("ev") == "state")
gold0 = r["self"]["gold"]
ok(gold0 == 1000, "GM gold lands in session state")
h.send({"op": "buy", "item": shop["金创药(小)"], "count": 2})
r = h.ok_for(lambda m: "self" in m)
ok(r is not None and r["self"]["gold"] == gold0 - 40, "buy charges gold")

# 换图打怪掉血，再用药回
h.send({"op": "move", "map": 2})
r = h.ok_for(lambda m: "self" in m and m["self"]["map"] == 2)
ok(r is not None, "move to wildcat map (level gate ok)")
cat = None
h.send({"op": "mobs"})
r = h.ok_for(lambda m: "rows" in m)
for x in r["rows"]:
    if x["name"] == "多钩猫" and x["alive"] == 1:
        cat = x["tpl"]
        break
ok(cat is not None, "wildcat mob lives on map 2")
hurt = 0
for _ in range(3):
    h.send({"op": "hunt", "mob": cat})
    r = h.ok_for(lambda m: "fight" in m)
    if r["fight"].get("mdmg", 0) > 0:
        hurt = r["self"]["hp"]
ok(hurt > 0 and hurt < r["self"]["maxhp"], "mob retaliates and hurts player")
h.send({"op": "use", "item": shop["金创药(小)"]})
r = h.ok_for(lambda m: "self" in m)
ok(r["self"]["hp"] > hurt, "potion heals player")

# GM 设 5 级 + 送铁剑 → ev drop 到达 → 穿上加攻
st, j, _ = gm("/admin/game/players/save", {
    "id": str(hunter_uid), "nickname": "小猎手", "realmId": "1", "job": "0",
    "level": "5", "gold": str(gold0), "gems": "0", "mapId": "2",
    "accountStatus": "1", "banReason": "",
    "giftItem": str(shop["铁剑"]), "giftCount": "1"}, cookie)
ok(j.get("code") == "0000", "GM gifts sword")
k = h.reply_for(lambda m: m.get("ev") == "drop"
                and "铁剑" in (m.get("item") or ""))
ok(k is not None, "gift drop event reaches client")
h.send({"op": "equip", "item": shop["铁剑"]})
r = h.ok_for(lambda m: "self" in m)
ok(r["self"]["weapon"] == shop["铁剑"]
   and r["self"]["atk"] >= 6 + 5 * 2 + 5 + 15,
   "equipping sword raises attack")
h.send({"op": "takeoff", "slot": "weapon"})
r = h.ok_for(lambda m: "self" in m)
ok(r["self"]["weapon"] == 0, "takeoff clears weapon slot")
h.send({"op": "equip", "item": shop["铁剑"]})
h.ok_for(lambda m: "self" in m)

# 卖兽皮换钱（材料不可买只能卖——打金闭环）
h.send({"op": "bag"})
r = h.ok_for(lambda m: "items" in m)
pelts = [i for i in r["items"] if i["name"] == "兽皮"]
pelt_n = pelts[0]["count"] if pelts else 0
pelt_id = pelts[0]["id"] if pelts else 0
gold1 = r["self"]["gold"] if pelts else 0
h.send({"op": "sell", "item": pelt_id, "count": pelt_n})
r = h.ok_for(lambda m: "self" in m)
ok(pelt_n > 0 and r["self"]["gold"] == gold1 + pelt_n * 15,
   "selling pelts pays half price")

# 自动挂机：开 → 每拍 ev fight → 关
h.send({"op": "auto", "mob": cat, "on": 1})
r = h.ok_for(lambda m: "auto" in m)
ok(r["auto"] == cat, "auto-hunt toggles on")
time.sleep(4)
h.send({"op": "auto", "mob": cat, "on": 0})
r = h.ok_for(lambda m: "auto" in m)
ok(r["auto"] == 0, "auto-hunt toggles off")
fights = 0
while True:
    m = h.reply_for(lambda m: m.get("ev") in ("fight", "levelup", "drop"),
                    timeout=3)
    if m is None:
        break
    if m.get("ev") == "fight":
        fights += 1
ok(fights >= 2, "auto-hunt pushes fight events each tick")

# 死亡：GM 送到 30 级赤月峡谷，auto 打 BOSS 三回合内倒下回城
st, j, _ = gm("/admin/game/players/save", {
    "id": str(hunter_uid), "nickname": "小猎手", "realmId": "1", "job": "0",
    "level": "30", "gold": str(gold0), "gems": "0", "mapId": "5",
    "accountStatus": "1", "banReason": ""}, cookie)
ok(j.get("code") == "0000", "GM moves hunter to boss map")
h.send({"op": "auto", "mob": 6, "on": 1})
r = h.ok_for(lambda m: "auto" in m)
ok(r["auto"] == 6, "auto-hunt targets boss")
died = False
for _ in range(10):
    m = h.reply_for(lambda m: m.get("ev") == "die", timeout=3)
    if m is not None:
        died = True
        break
h.pending.clear()
h.send({"op": "state"})
r = h.reply_for(lambda m: m.get("ev") == "state")
ok(died and r["self"]["map"] == 1 and r["self"]["auto"] == 0
   and r["self"]["hp"] == r["self"]["maxhp"] // 2,
   "death respawns player in town with half hp, auto off")

# 落库：背包/装备/血量随 flush 写入
time.sleep(11)
db = sqlite3.connect("data/app.db")
row = db.execute(
    'SELECT hp, weaponId FROM game_player WHERE id=?',
    (hunter_uid,)).fetchone()
ok(row is not None and row[1] == shop["铁剑"] and row[0] > 0,
   "combat state persisted with equipped weapon")
bags = db.execute(
    'SELECT itemId, count FROM game_bag WHERE playerId=?',
    (hunter_uid,)).fetchall()
ok(any(b[1] >= 1 for b in bags), "bag rows persisted")
db.close()
h.drop()

print(f"ALL PASS checks={checks}")

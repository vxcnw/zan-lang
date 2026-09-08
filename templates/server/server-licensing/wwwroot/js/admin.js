/* Admin 外壳行为：标签、弹窗、写操作与实时指标流。规则全部在标记中，屏幕即模板。 */
(function () {
  var panel, tabs, toasts;
  var state = { tabs: [], active: '' };
  var KEY = 'zanweb.admin.tabs.v2';
  var stream = null;
  var streamGen = 0;
  var loadSeq = 0;
  var loadController = null;
  var ctxMenu = null;
  var paneMemo = {};

  function el(id) { return document.getElementById(id); }

  function toast(msg, kind) {
    var t = document.createElement('div');
    t.className = 'toast ' + (kind || 'ok');
    t.textContent = msg;
    toasts.appendChild(t);
    setTimeout(function () { t.remove(); }, 3200);
  }

  // ---- tabs ---------------------------------------------------------------

  function save() {
    try {
      localStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) { /* private mode: tabs simply do not survive a reload */ }
  }

  function pathOf(path, keepHash) {
    var u = new URL(path || '/admin', location.origin);
    var q = Array.from(u.searchParams.entries()).sort(function (a, b) {
      return a[0] === b[0] ? a[1].localeCompare(b[1]) : a[0].localeCompare(b[0]);
    });
    u.search = '';
    q.forEach(function (p) { u.searchParams.append(p[0], p[1]); });
    return u.pathname + (u.search ? u.search : '') +
      (keepHash ? (u.hash || '') : '');
  }

  // A hash selects a pane inside the resource; it is not a second tab.
  function normalize(path) { return pathOf(path, false); }

  function rememberPane(path) {
    var u = new URL(path || '/admin', location.origin);
    if (u.hash && u.hash.length > 1) {
      paneMemo[normalize(path)] = decodeURIComponent(u.hash.slice(1));
    }
  }

  function restore() {
    try {
      var raw = localStorage.getItem(KEY);
      if (raw) { state = JSON.parse(raw); }
    } catch (e) { state = { tabs: [], active: '' }; }
    if (!state || !Array.isArray(state.tabs)) { state = { tabs: [], active: '' }; }
    state.tabs = state.tabs.map(function (t) {
      return { path: normalize(t.path), title: t.title || t.path };
    });
    state.active = state.active ? normalize(state.active) : '';
  }

  function find(path) {
    path = normalize(path);
    for (var i = 0; i < state.tabs.length; i++) {
      if (state.tabs[i].path === path) { return i; }
    }
    return -1;
  }

  function paint() {
    tabs.innerHTML = '';
    state.tabs.forEach(function (t) {
      var b = document.createElement('span');
      b.className = 'ad-tab' + (t.path === state.active ? ' active' : '');
      b.title = t.path;
      var label = document.createElement('span');
      label.textContent = t.title || t.path;
      b.appendChild(label);
      if (state.tabs.length > 1) {
        var x = document.createElement('span');
        x.className = 'x';
        x.textContent = '×';
        x.onclick = function (ev) { ev.stopPropagation(); close(t.path); };
        b.appendChild(x);
      }
      b.onclick = function () { open(t.path, t.title); };
      b.oncontextmenu = function (ev) { ev.preventDefault(); tabMenu(ev, t); };
      tabs.appendChild(b);
    });
    document.querySelectorAll('.ad-side a.mi').forEach(function (a) {
      a.classList.toggle('active', a.getAttribute('href') === base(state.active));
    });
    save();
    showActiveTab();
    paintTabNav();
  }

  // The strip scrolls under two arrows rather than a scrollbar, so a long
  // session does not squash the tabs or leave the active one off-screen.
  function paintTabNav() {
    var bar = tabs.parentNode;
    if (!bar) { return; }
    var arrows = bar.querySelectorAll('[data-tabnav]');
    var over = tabs.scrollWidth > tabs.clientWidth + 1;
    for (var i = 0; i < arrows.length; i++) { arrows[i].hidden = !over; }
  }

  function showActiveTab() {
    var a = tabs.querySelector('.ad-tab.active');
    if (!a) { return; }
    var left = a.offsetLeft;
    var right = left + a.offsetWidth;
    if (left < tabs.scrollLeft) { tabs.scrollLeft = left - 8; }
    else if (right > tabs.scrollLeft + tabs.clientWidth) {
      tabs.scrollLeft = right - tabs.clientWidth + 8;
    }
  }

  function base(path) {
    var u = new URL(path || '/admin', location.origin);
    return u.pathname;
  }

  // Right-click on a tab: the usual workspace menu. Closing is deliberate --
  // a left click never closes anything but the tab's own ×.
  function tabMenu(ev, t) {
    hideTabMenu();
    var i = find(t.path);
    var m = document.createElement('div');
    m.className = 'ad-ctx';
    var items = [
      ['刷新', function () { open(t.path, t.title); }, false],
      ['关闭', function () { close(t.path); }, state.tabs.length < 2],
      ['关闭其他', function () { closeOthers(t.path); }, state.tabs.length < 2],
      ['关闭右侧', function () { closeRight(t.path); }, i >= state.tabs.length - 1],
      ['全部关闭', function () { closeAllTabs(); }, state.tabs.length < 2]
    ];
    items.forEach(function (it) {
      var n = document.createElement('div');
      n.className = 'item' + (it[2] ? ' off' : '');
      n.textContent = it[0];
      if (!it[2]) {
        n.onclick = function () { hideTabMenu(); it[1](); };
      }
      m.appendChild(n);
    });
    document.body.appendChild(m);
    var x = Math.min(ev.clientX, window.innerWidth - m.offsetWidth - 6);
    var y = Math.min(ev.clientY, window.innerHeight - m.offsetHeight - 6);
    m.style.left = Math.max(4, x) + 'px';
    m.style.top = Math.max(4, y) + 'px';
    ctxMenu = m;
  }

  function hideTabMenu() {
    if (ctxMenu) { ctxMenu.remove(); ctxMenu = null; }
  }

  function closeOthers(path) {
    state.tabs = state.tabs.filter(function (o) { return o.path === path; });
    var keep = state.tabs[0];
    open(keep.path, keep.title);
  }

  function closeRight(path) {
    var i = find(path);
    if (i < 0) { return; }
    state.tabs = state.tabs.slice(0, i + 1);
    if (find(state.active) < 0) { open(path, state.tabs[i].title); return; }
    paint();
  }

  // The last tab stays: an empty workspace has nothing to show.
  function closeAllTabs() {
    var home = { path: '/admin', title: '仪表盘' };
    state.tabs = [home];
    open(home.path, home.title);
  }

  function close(path) {
    var i = find(path);
    if (i < 0) { return; }
    state.tabs.splice(i, 1);
    if (state.active === path) {
      var next = state.tabs[Math.min(i, state.tabs.length - 1)];
      if (next) { open(next.path, next.title); return; }
      state.active = '';
    }
    paint();
  }

  function open(path, title, replace) {
    rememberPane(path);
    path = normalize(path);
    var same = state.active === path;
    var i = find(path);
    if (i < 0) {
      /* Same screen, different query (pager / filter / detail link) reuses
         its tab in place: the tab strip stays one-per-screen and the URL
         still tracks what the panel shows. */
      var root = base(path);
      for (var j = 0; j < state.tabs.length; j++) {
        if (base(state.tabs[j].path) === root) {
          i = j;
          state.tabs[j].path = path;
          if (title) { state.tabs[j].title = title; }
          break;
        }
      }
    }
    if (i < 0) { state.tabs.push({ path: path, title: title || path }); }
    state.active = path;
    paint();
    if (replace || same) { history.replaceState({ path: path }, '', path); }
    else { history.pushState({ path: path }, '', path); }
    load(path);
  }

  function restoreHistory() {
    rememberPane(location.pathname + location.search + location.hash);
    var path = normalize(location.pathname + location.search + location.hash);
    var i = find(path);
    var title = i >= 0 ? state.tabs[i].title : path;
    open(path, title, true);
  }

  // ---- panel --------------------------------------------------------------

  function load(path, quiet) {
    path = normalize(path);
    var seq = ++loadSeq;
    if (loadController) { loadController.abort(); }
    loadController = window.AbortController ? new AbortController() : null;
    stopStream();
    panel.setAttribute('aria-busy', 'true');
    var opts = { headers: { 'X-Fragment': '1' }, credentials: 'same-origin' };
    if (loadController) { opts.signal = loadController.signal; }
    return fetch(path, opts)
      .then(function (r) {
        if (seq !== loadSeq) { return ''; }
        if (r.status === 401) { location.href = '/admin/login'; return ''; }
        if (!r.ok) { throw new Error('http ' + r.status); }
        var t = r.headers.get('X-Tab-Title');
        if (t) {
          var i = find(path);
          if (i >= 0) { state.tabs[i].title = decodeURIComponent(t); paint(); }
        }
        return r.text();
      })
      .then(function (html) {
        if (html === '' || seq !== loadSeq) { return; }
        panel.innerHTML = html;
        panel.removeAttribute('aria-busy');
        // A quiet refresh (after a dialog write) is in place: the list the
        // user is looking at updates where it stands -- no scroll jump.
        if (!quiet) { panel.scrollTop = 0; }
        startStream();
        runScripts(panel);
        restorePane(path);
        wireModelPick(panel);
      })
      .catch(function (err) {
        if (seq !== loadSeq || err.name === 'AbortError') { return; }
        panel.removeAttribute('aria-busy');
        toast('页面加载失败', 'bad');
      });
  }

  /* innerHTML does not execute <script>, and a screen may carry one. */
  function runScripts(root) {
    if (window.applyFragmentWidgets) { window.applyFragmentWidgets(root); }
    root.querySelectorAll('script').forEach(function (old) {
      var s = document.createElement('script');
      s.textContent = old.textContent;
      old.replaceWith(s);
    });
  }

  function reload(quiet) {
    if (state.active) { load(state.active, quiet); }
  }

  // Re-open the sub-pane this screen was on before its panel was rebuilt.
  function restorePane(path) {
    var name = paneMemo[base(path)];
    if (!name) { return; }
    var btn = panel.querySelector('[data-setting-tabs] [data-pane="' + name + '"]');
    if (btn) { btn.click(); }
  }

  // The AI model is fetched, not typed: given the base URL and key already on
  // the form, ask the provider what it offers and let the operator pick. The
  // key is only posted to our own endpoint, which uses it server-side and never
  // returns it. Providers with no /models endpoint keep the plain text field.
  function wireModelPick(root) {
    var input = root.querySelector('[name="ai.model"]');
    if (!input || input.getAttribute('data-model-wired')) { return; }
    input.setAttribute('data-model-wired', '1');
    var list = document.createElement('datalist');
    list.id = 'ai-model-options';
    input.setAttribute('list', list.id);
    input.parentNode.insertBefore(list, input.nextSibling);
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'btn sm';
    btn.textContent = '获取模型';
    btn.style.marginLeft = '8px';
    input.parentNode.insertBefore(btn, list.nextSibling);
    btn.addEventListener('click', function () {
      var url = root.querySelector('[name="ai.baseUrl"]');
      var key = root.querySelector('[name="ai.apiKey"]');
      if (!url || !url.value.trim()) { Layer.msg('请先填写接口地址'); return; }
      btn.disabled = true;
      btn.textContent = '获取中…';
      fetch('/admin/dev/ai/models', {
        method: 'POST', credentials: 'same-origin',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ baseUrl: url.value.trim(),
                                    apiKey: key ? key.value : '' }).toString()
      }).then(function (r) { return r.json(); }).then(function (j) {
        var models = (j && j.code === '0000' && j.data && j.data.models) || [];
        if (!models.length) { Layer.notify('没有获取到模型', '确认接口地址和 Key 是否正确，或该服务不支持模型列表', 'bad'); return; }
        list.innerHTML = '';
        for (var i = 0; i < models.length; i++) {
          var o = document.createElement('option');
          o.value = models[i];
          list.appendChild(o);
        }
        if (!input.value) { input.value = models[0]; }
        input.focus();
        Layer.msg('已获取 ' + models.length + ' 个模型，点输入框选择');
      }).catch(function () {
        Layer.notify('获取失败', '请求未完成', 'bad');
      }).then(function () {
        btn.disabled = false; btn.textContent = '获取模型';
      });
    });
  }

  // ---- layer: windows, drawers, prompts and notices ------------------------
  //
  // One primitive, five shapes. A layer is a positioned box over the shell:
  //   Layer.open({url|content})     a draggable, resizable-by-maximise window
  //   Layer.drawer({url|content})   the same panel, docked to the right edge
  //   Layer.confirm(text, onOk)     a question with two buttons
  //   Layer.msg(text, kind)         a short line in the middle of the screen
  //   Layer.notify(title, text)     a card in the corner that stacks
  //   Layer.tip(el, text)           a bubble anchored to an element
  // They stack: opening a form from a form is one more window, and Escape or
  // the close button always dismisses the topmost one.

  var Layer = (function () {
    var seq = 0;
    var zTop = 200;
    var stack = [];

    function node(tag, cls, text) {
      var n = document.createElement(tag);
      if (cls) { n.className = cls; }
      if (text !== undefined) { n.textContent = text; }
      return n;
    }

    function shell(opts) {
      var id = ++seq;
      var mask = node('div', 'lay-mask');
      var box = node('div', 'lay-box' + (opts.drawer ? ' drawer' : '')
        + (opts.kind ? ' ' + opts.kind : ''));
      box.style.zIndex = ++zTop;
      mask.style.zIndex = zTop;
      if (opts.width) { box.style.width = opts.width; }

      var head = node('header');
      head.appendChild(node('span', 'title', opts.title || ''));
      var ops = node('span', 'ops');
      if (!opts.drawer && !opts.bare) {
        var max = node('button', 'wbtn', '□');
        max.type = 'button';
        max.title = '最大化 / 还原';
        max.onclick = function () {
          box.classList.toggle('max');
          if (!box.classList.contains('max')) { place(box, opts); }
        };
        ops.appendChild(max);
      }
      var x = node('button', 'wbtn', '×');
      x.type = 'button';
      x.title = '关闭';
      x.onclick = function () { Layer.close(id); };
      ops.appendChild(x);
      head.appendChild(ops);

      var body = node('div', 'body');
      box.appendChild(head);
      box.appendChild(body);
      document.body.appendChild(mask);
      document.body.appendChild(box);
      place(box, opts);
      if (!opts.drawer) { drag(box, head); }
      box.addEventListener('mousedown', function () { box.style.zIndex = ++zTop; });
      if (opts.maskClose !== false) {
        mask.onclick = function () { Layer.close(id); };
      }
      stack.push({ id: id, box: box, mask: mask });
      return { id: id, box: box, body: body, head: head };
    }

    // Centred on first paint, then wherever the user drags it.
    function place(box, opts) {
      if (opts.drawer) { return; }
      var w = box.offsetWidth;
      var h = box.offsetHeight;
      var left = Math.max(8, (window.innerWidth - w) / 2);
      var top = Math.max(8, (window.innerHeight - h) / 3);
      box.style.left = Math.round(left) + 'px';
      box.style.top = Math.round(top) + 'px';
    }

    function drag(box, handle) {
      handle.addEventListener('mousedown', function (ev) {
        if (ev.target.closest('.wbtn')) { return; }
        if (box.classList.contains('max')) { return; }
        var sx = ev.clientX, sy = ev.clientY;
        var ox = box.offsetLeft, oy = box.offsetTop;
        document.body.classList.add('lay-dragging');
        function move(e) {
          var nx = Math.min(Math.max(0, ox + e.clientX - sx),
                            window.innerWidth - 60);
          var ny = Math.min(Math.max(0, oy + e.clientY - sy),
                            window.innerHeight - 30);
          box.style.left = nx + 'px';
          box.style.top = ny + 'px';
        }
        function up() {
          document.body.classList.remove('lay-dragging');
          document.removeEventListener('mousemove', move);
          document.removeEventListener('mouseup', up);
        }
        document.addEventListener('mousemove', move);
        document.addEventListener('mouseup', up);
        ev.preventDefault();
      });
    }

    function fill(w, opts) {
      if (opts.content !== undefined) {
        w.body.innerHTML = opts.content;
        ready(w, opts);
        return Promise.resolve(w.id);
      }
      w.body.innerHTML = '<div class="lay-loading">加载中…</div>';
      return fetch(opts.url, {
        headers: { 'X-Fragment': '1' }, credentials: 'same-origin'
      }).then(function (r) {
        if (r.ok) { return r.text(); }
        return r.json().then(function (j) { throw new Error(j.msg || '打开失败'); });
      }).then(function (html) {
        w.body.innerHTML = html;
        var t = w.body.querySelector('[data-title]');
        if (t) { w.head.querySelector('.title').textContent = t.getAttribute('data-title'); }
        ready(w, opts);
        return w.id;
      }).catch(function (e) {
        Layer.close(w.id);
        Layer.msg(e.message || '打开失败', 'bad');
      });
    }

    function ready(w, opts) {
      runScripts(w.body);
      if (!opts.drawer) { place(w.box, opts); }
      var first = w.body.querySelector('input:not([type=hidden]), textarea, select');
      if (first) { first.focus(); }
    }

    return {
      open: function (opts) {
        var w = shell(opts);
        return fill(w, opts);
      },
      drawer: function (opts) {
        opts.drawer = true;
        var w = shell(opts);
        return fill(w, opts);
      },
      confirm: function (text, onOk, title) {
        var w = shell({ title: title || '确认', width: '320px', bare: true,
                        maskClose: false });
        w.box.classList.add('ask');
        w.body.innerHTML = '';
        w.body.appendChild(node('p', 'ask-text', text));
        var foot = node('div', 'ask-ops');
        var no = node('button', 'btn sm', '取消');
        no.type = 'button';
        no.onclick = function () { Layer.close(w.id); };
        var yes = node('button', 'btn sm primary', '确定');
        yes.type = 'button';
        yes.onclick = function () { Layer.close(w.id); onOk(); };
        foot.appendChild(no);
        foot.appendChild(yes);
        w.body.appendChild(foot);
        yes.focus();
        return w.id;
      },
      msg: function (text, kind) {
        var m = node('div', 'lay-msg ' + (kind || 'ok'), text);
        m.style.zIndex = ++zTop;
        document.body.appendChild(m);
        setTimeout(function () { m.remove(); }, 2200);
      },
      notify: function (title, text, kind) {
        var host = document.getElementById('ad-notices');
        if (!host) { return; }
        var card = node('div', 'notice ' + (kind || 'ok'));
        card.appendChild(node('div', 'nt', title));
        if (text) { card.appendChild(node('div', 'nb', text)); }
        var x = node('span', 'x', '×');
        x.onclick = function () { card.remove(); };
        card.appendChild(x);
        host.appendChild(card);
        setTimeout(function () { card.remove(); }, 6000);
      },
      tip: function (anchor, text) {
        Layer.untip();
        var t = node('div', 'lay-tip', text);
        t.style.zIndex = ++zTop;
        document.body.appendChild(t);
        var r = anchor.getBoundingClientRect();
        var left = r.left + r.width / 2 - t.offsetWidth / 2;
        var top = r.top - t.offsetHeight - 6;
        if (top < 4) { top = r.bottom + 6; t.classList.add('below'); }
        t.style.left = Math.max(4, Math.round(left)) + 'px';
        t.style.top = Math.round(top) + 'px';
        Layer._tip = t;
      },
      untip: function () {
        if (Layer._tip) { Layer._tip.remove(); Layer._tip = null; }
      },
      close: function (id) {
        for (var i = stack.length - 1; i >= 0; i--) {
          if (stack[i].id !== id) { continue; }
          stack[i].box.remove();
          stack[i].mask.remove();
          stack.splice(i, 1);
          return;
        }
      },
      closeTop: function () {
        if (!stack.length) { return false; }
        var top = stack[stack.length - 1];
        Layer.close(top.id);
        return true;
      },
      any: function () { return stack.length > 0; }
    };
  })();

  window.Layer = Layer;

  // ---- dialogs ------------------------------------------------------------

  function dialog(url, wide, title) {
    return Layer.open({ url: url, title: title || '编辑',
                        width: wide ? '820px' : '560px' });
  }

  function closeDialog() { Layer.closeTop(); }

  // ---- writes -------------------------------------------------------------

  function post(url, body) {
    return fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Fragment': '1'
      },
      body: body || ''
    }).then(function (r) {
      if (r.status === 401) { location.href = '/admin/login'; return null; }
      return r.json();
    });
  }

  function submit(form) {
    var data = new FormData(form);
    var parts = [];
    // Checkbox groups arrive as one comma-joined field: the server reads a
    // single value and does not have to care about repeated names.
    var groups = {};
    data.forEach(function (v, k) {
      if (k.slice(-2) === '[]') {
        var name = k.slice(0, -2);
        (groups[name] = groups[name] || []).push(v);
        return;
      }
      parts.push(encodeURIComponent(k) + '=' + encodeURIComponent(v));
    });
    Object.keys(groups).forEach(function (name) {
      parts.push(encodeURIComponent(name) + '=' + encodeURIComponent(groups[name].join(',')));
    });
    var btn = form.querySelector('[type=submit]');
    if (btn) { btn.disabled = true; }
    post(form.getAttribute('action'), parts.join('&')).then(function (j) {
      if (btn) { btn.disabled = false; }
      if (!j) { return; }
      if (j.code === '0000') {
        toast(j.msg || '已保存', 'ok');
        closeDialog();
        // The dialog just closed over the list: refresh it quietly so the
        // rows update in place instead of jumping back to the top.
        reload(true);
        return;
      }
      toast(j.msg || '保存失败', 'bad');
    }).catch(function () {
      if (btn) { btn.disabled = false; }
      toast('请求失败', 'bad');
    });
  }

  // ---- live metrics -------------------------------------------------------

  function stopStream() {
    streamGen++;
    if (stream) { stream.close(); stream = null; }
    if (dayTimer) { clearInterval(dayTimer); dayTimer = null; }
    dayPts = {};
    dayDay = '';
    topDay = {};
    topLive = {};
    topTotal = 0;
  }

  function startStream() {
    var host = panel.querySelector('[data-stream]');
    if (!host) { return; }
    var gen = ++streamGen;
    var url = host.getAttribute('data-stream');
    stream = new EventSource(url);
    stream.addEventListener('metrics', function (ev) {
      if (gen !== streamGen) { return; }
      try { paintSnapshot(JSON.parse(ev.data)); } catch (e) { toast('实时数据格式错误', 'bad'); }
    });
    stream.addEventListener('series', function (ev) {
      if (gen !== streamGen) { return; }
      try { paintSeries(JSON.parse(ev.data)); } catch (e) { toast('实时序列格式错误', 'bad'); }
    });
    stream.onerror = function () { /* EventSource retries by itself */ };
    wireTopSort();
    startDay(host.getAttribute('data-day'), gen);
  }

  // ---- today, cumulative --------------------------------------------------

  // The day's figures come from the metrics database, not from the live
  // stream: a worker's counters restart with the worker, so anything drawn
  // from them walks backwards whenever the fleet changes. Polled slowly on
  // purpose -- it is a whole day of five-minute buckets, and it only grows.
  var dayTimer = null;
  var dayPts = {};      // bucket second -> point, so history is merged, not replaced
  var dayDay = '';

  function startDay(url, gen) {
    if (!url) { return; }
    var tick = function () {
      fetch(url, { credentials: 'same-origin' })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (j) { if (j && gen === streamGen) { paintDay(j); } })
        .catch(function () { /* the next tick tries again */ });
    };
    tick();
    dayTimer = setInterval(tick, 60000);
  }

  function paintDay(d) {
    // Midnight: the day being drawn has changed, so yesterday's buckets are
    // not the start of this one.
    if (d.day !== dayDay) { dayPts = {}; dayDay = d.day || ''; }
    put('day_calls', d.calls || 0);
    put('day_errors', d.errors || 0);
    put('day_avg_us', dur(d.avg_us));
    put('day_max_us', dur(d.max_us));
    put('day_total_us', dur(d.total_us));
    put('day_label', d.day || '');

    // Merged, not assigned: a bucket already on screen is updated by a later
    // answer and never removed by one, so a partial or failed read cannot
    // shorten the chart.
    (d.points || []).forEach(function (p) { dayPts[p.t] = p; });
    var pts = Object.keys(dayPts).map(function (k) { return dayPts[k]; })
      .sort(function (a, b) { return a.t - b.t; })
      .map(function (p) {
        return { t: p.t, label: clock(p.t), calls: p.calls || 0,
                 errors: p.errors || 0, avg_us: p.avg_us || 0,
                 max_us: p.max_us || 0 };
      });
    draw('chart-day-req', [
      { color: '#1f6feb', label: '请求', values: pts.map(function (p) { return p.calls; }) },
      { color: '#b42318', label: '错误', values: pts.map(function (p) { return p.errors; }) }
    ], pts, '');
    draw('chart-day-lat', [
      { color: '#7c3aed', label: '平均', values: pts.map(function (p) { return ms(p.avg_us); }) },
      { color: '#d97706', label: '最慢', values: pts.map(function (p) { return ms(p.max_us); }) }
    ], pts, ' ms');

    topTotal = d.calls || 0;
    topDay = {};
    (d.top || []).forEach(function (s) { topDay[s.req] = s; });
    paintTop();
  }

  // ---- one interface ranking ----------------------------------------------

  // One row per interface, sorted by whichever column was clicked. The three
  // tables this replaces were the same interfaces ordered three ways, which is
  // what sorting a table already does.
  //
  // Two sources, because neither answers the whole question: the day's counts
  // and durations come from the database (they survive a worker restart and
  // include the workers that are gone), while `failed` and `rejected` are only
  // counted live, in the processes that are up. An interface the live snapshot
  // has but the database has not yet (another worker's minute is not flushed)
  // is still listed, with its cumulative columns blank rather than as zeros.
  var topDay = {};       // req -> today's row, from the metrics database
  var topLive = {};      // req -> live row, from the snapshot stream
  var topTotal = 0;      // today's calls, for the share column
  var topSort = { key: 'calls', dir: -1 };

  function wireTopSort() {
    panel.querySelectorAll('[data-toptable] th[data-sort]').forEach(function (th) {
      if (!th.getAttribute('data-label')) {
        th.setAttribute('data-label', th.textContent);
      }
      th.style.cursor = 'pointer';
      th.addEventListener('click', function () {
        var key = th.getAttribute('data-sort');
        // Same column again reverses it; a new column starts descending,
        // except the name, which reads better A-Z.
        if (topSort.key === key) { topSort.dir = -topSort.dir; }
        else { topSort = { key: key, dir: key === 'req' ? 1 : -1 }; }
        paintTop();
      });
    });
    paintTopHead();
  }

  function paintTopHead() {
    panel.querySelectorAll('[data-toptable] th[data-sort]').forEach(function (th) {
      var label = th.getAttribute('data-label') || th.textContent;
      var on = th.getAttribute('data-sort') === topSort.key;
      th.textContent = label + (on ? (topSort.dir < 0 ? ' \u2193' : ' \u2191') : '');
    });
  }

  function paintTop() {
    var tb = panel.querySelector('[data-daytop]');
    if (!tb) { return; }
    var rows = [];
    var keys = {};
    Object.keys(topDay).forEach(function (k) { keys[k] = 1; });
    Object.keys(topLive).forEach(function (k) { keys[k] = 1; });
    Object.keys(keys).forEach(function (req) {
      var d = topDay[req], l = topLive[req] || {};
      rows.push({
        req: req,
        day: !!d,
        calls: d ? (d.calls || 0) : 0,
        errors: d ? (d.errors || 0) : 0,
        avg_us: d ? (d.avg_us || 0) : 0,
        max_us: d ? (d.max_us || 0) : 0,
        total_us: d ? (d.total_us || 0) : 0,
        failed: l.failed || 0,
        rejected: l.rejected || 0
      });
    });
    // The share column is the call count as a percentage, so it sorts by it.
    var k = topSort.key === 'share' ? 'calls' : topSort.key, dir = topSort.dir;
    rows.sort(function (a, b) {
      if (k === 'req') { return a.req < b.req ? -dir : (a.req > b.req ? dir : 0); }
      return (a[k] - b[k]) * dir;
    });
    paintTopHead();
    tb.innerHTML = rows.length
      ? rows.map(function (s) {
          var share = s.day && topTotal > 0
            ? (s.calls * 100 / topTotal).toFixed(1) + '%' : '—';
          var num = function (v) { return s.day ? String(v) : '—'; };
          var d2 = function (v) { return s.day ? dur(v) : '—'; };
          return '<tr><td class="ellip mono" title="' + esc(s.req) + '">' +
                 esc(s.req) + '</td><td class="num">' + num(s.calls) +
                 '</td><td class="num muted">' + share +
                 '</td><td class="num">' + num(s.errors) +
                 '</td><td class="num">' + d2(s.avg_us) +
                 '</td><td class="num">' + d2(s.max_us) +
                 '</td><td class="num">' + d2(s.total_us) +
                 '</td><td class="num">' + s.failed +
                 '</td><td class="num">' + s.rejected + '</td></tr>';
        }).join('')
      : '<tr><td colspan="9" class="muted">今天还没有请求</td></tr>';
  }

  // A bucket's wall clock as "hh:mm", for a chart whose x axis is one day.
  function clock(sec) {
    var d = new Date(sec * 1000);
    var p2 = function (n) { return (n < 10 ? '0' : '') + n; };
    return p2(d.getHours()) + ':' + p2(d.getMinutes());
  }

  function put(name, value) {
    panel.querySelectorAll('[data-metric="' + name + '"]').forEach(function (n) {
      n.textContent = value;
    });
  }

  function bytes(v) {
    if (v < 0) { return 'n/a'; }
    if (v < 1024) { return v + ' B'; }
    if (v < 1048576) { return (v / 1024).toFixed(0) + ' KB'; }
    return (v / 1048576).toFixed(1) + ' MB';
  }

  // Every duration the server publishes is MICROSECONDS (*_us). The unit is
  // picked per value because the range spans four orders of magnitude: a served
  // request is hundreds of microseconds, a stuck one is seconds -- and the
  // millisecond integers this replaces showed every fast endpoint as "0 ms".
  function dur(us) {
    us = us || 0;
    if (us < 0) { return 'n/a'; }
    if (us < 1000) { return us + ' \u00b5s'; }
    if (us < 1000000) { return (us / 1000).toFixed(2) + ' ms'; }
    return (us / 1000000).toFixed(2) + ' s';
  }

  // Microseconds as fractional milliseconds, for a chart whose axis is one
  // unit: 890us plots as 0.89, not as a flat 0.
  function ms(us) { return Math.round((us || 0) / 10) / 100; }

  // Uptime in the same shape the server-rendered fields use (Fmt.Uptime):
  // "d hh:mm:ss" once it has been up for a day.
  function upt(msv) {
    var t = Math.floor((msv || 0) / 1000);
    var p2 = function (n) { return (n < 10 ? '0' : '') + n; };
    var clock = p2(Math.floor((t % 86400) / 3600)) + ':' +
                p2(Math.floor((t % 3600) / 60)) + ':' + p2(t % 60);
    var d = Math.floor(t / 86400);
    return d > 0 ? d + 'd ' + clock : clock;
  }

  // One row per server process. Everything else on the page is the merge of
  // every worker, so this table is where an uneven or dead worker shows up:
  // `live` is 0 once a worker has stopped publishing, and its last totals stay
  // on screen (marked stale) instead of silently leaving the table.
  function paintProcs(rows) {
    var tb = panel.querySelector('[data-procs]');
    if (!tb) { return; }
    rows = rows || [];
    tb.innerHTML = rows.length
      ? rows.map(function (p) {
          var stale = !p.live;
          return '<tr' + (stale ? ' class="muted"' : '') + '><td class="mono">' +
                 (p.worker || 0) + '</td><td class="mono">' + (p.pid || 0) +
                 '</td><td class="mono">' + upt(p.uptime_ms) +
                 '</td><td class="num">' + (p.requests || 0) +
                 '</td><td class="num">' + (p.errors || 0) +
                 '</td><td class="num">' + dur(p.avg_us) +
                 '</td><td class="num">' + dur(p.max_us) +
                 '</td><td class="num">' + (p.concurrent || 0) +
                 '</td><td class="num">' + (p.streams || 0) +
                 '</td><td class="num">' + (p.queries || 0) +
                 '</td><td class="num">' + (p.cpu_percent < 0 ? 'n/a' : p.cpu_percent + '%') +
                 '</td><td class="num">' + bytes(p.mem_rss_bytes) +
                 '</td><td class="num">' + (stale ? (p.age || 0) + 's 未上报' : '正常') +
                 '</td></tr>';
        }).join('')
      : '<tr><td colspan="13" class="muted">等待数据…</td></tr>';
  }

  function paintSnapshot(m) {
    var r = m.requests || {}, q = m.queries || {};
    put('requests', r.count || 0);
    put('errors', r.errors || 0);
    put('failed', r.failed || 0);
    put('rejected', r.rejected || 0);
    put('avg_us', dur(r.avg_us));
    put('max_us', dur(r.max_us));
    put('queries', q.count || 0);
    put('query_avg_us', dur(q.avg_us));
    put('cpu', m.cpu_percent < 0 ? 'n/a' : m.cpu_percent + '%');
    put('mem', bytes(m.mem_rss_bytes));
    paintProcs(m.processes);
    topLive = {};
    (m.top_requests || []).forEach(function (s) { topLive[s.req] = s; });
    paintTop();
    var top = panel.querySelector('[data-topsql]');
    if (top) {
      var ts = m.top_sql || [];
      top.innerHTML = ts.length
        ? ts.map(function (s) {
            return '<tr><td class="ellip mono" title="' + esc(s.sql) + '">' +
                   esc(s.sql) + '</td><td class="num">' + (s.count || 0) +
                   '</td><td class="num">' + dur(s.avg_us) +
                   '</td><td class="num">' + dur(s.max_us) +
                   '</td><td class="num">' + dur(s.total_us) + '</td></tr>';
          }).join('')
        : '<tr><td colspan="5" class="muted">暂无 SQL 记录</td></tr>';
    }
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function paintSeries(s) {
    var pts = s.points || [];
    draw('chart-req', [
      { color: '#1f6feb', label: '请求', values: pts.map(function (p) { return p.req; }) },
      { color: '#b42318', label: '错误', values: pts.map(function (p) { return p.err; }) }
    ], pts, '');
    draw('chart-lat', [
      { color: '#7c3aed', label: '平均', values: pts.map(function (p) { return ms(p.avg_us); }) },
      { color: '#d97706', label: 'P95', values: pts.map(function (p) { return ms(p.p95_us); }) }
    ], pts, ' ms');
    draw('chart-db', [
      { color: '#0f766e', label: '查询数', values: pts.map(function (p) { return p.queries; }) },
      { color: '#0891b2', label: '平均 ms', values: pts.map(function (p) { return ms(p.query_avg_us); }) }
    ], pts, '');
    draw('chart-sys', [
      { color: '#15803d', label: 'CPU %', values: pts.map(function (p) { return Math.max(p.cpu_percent, 0); }) },
      { color: '#6b7280', label: '内存 MB', values: pts.map(function (p) {
          return Math.round(Math.max(p.mem_rss_bytes, 0) / 1048576); }) }
    ], pts, '');
  }

  // One shared floating tooltip for every chart; position:fixed so it is never
  // clipped by a card's overflow.
  function monTip() {
    var t = document.getElementById('mon-tip');
    if (!t) {
      t = document.createElement('div');
      t.id = 'mon-tip';
      t.style.cssText = 'position:fixed;z-index:9999;pointer-events:none;display:none;'
        + 'background:rgba(17,24,39,.92);color:#fff;font:12px/1.5 system-ui,sans-serif;'
        + 'padding:6px 8px;border-radius:6px;box-shadow:0 4px 12px rgba(0,0,0,.25);white-space:nowrap';
      document.body.appendChild(t);
    }
    return t;
  }

  /* A line chart is a polyline over a scaled array; a charting library would be
   * a lot of bytes for that. */
  function draw(id, series, pts, unit) {
    var c = panel.querySelector('#' + id);
    if (!c) { return; }
    var dpr = window.devicePixelRatio || 1;
    var w = c.clientWidth, h = c.clientHeight;
    c.width = w * dpr; c.height = h * dpr;
    var g = c.getContext('2d');

    var max = 1;
    series.forEach(function (s) {
      s.values.forEach(function (v) { if (v > max) { max = v; } });
    });

    // Redraws the whole chart; `hover` >= 0 overlays a guide line and a dot on
    // each series at that sample, so the tooltip has a visible anchor.
    function render(hover) {
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      g.clearRect(0, 0, w, h);
      g.strokeStyle = '#eef0f3';
      g.lineWidth = 1;
      for (var i = 1; i < 4; i++) {
        var gy = Math.round(h * i / 4) + .5;
        g.beginPath(); g.moveTo(0, gy); g.lineTo(w, gy); g.stroke();
      }
      series.forEach(function (s) {
        var n = s.values.length;
        if (n < 2) { return; }
        g.beginPath();
        for (var i = 0; i < n; i++) {
          var x = w * i / (n - 1);
          var y = h - (h - 4) * (s.values[i] / max);
          if (i === 0) { g.moveTo(x, y); } else { g.lineTo(x, y); }
        }
        g.strokeStyle = s.color;
        g.lineWidth = 1.5;
        g.stroke();
      });
      var nn = series[0] ? series[0].values.length : 0;
      if (hover >= 0 && nn >= 2) {
        var hx = w * hover / (nn - 1);
        g.strokeStyle = '#94a3b8';
        g.lineWidth = 1;
        g.beginPath(); g.moveTo(hx + .5, 0); g.lineTo(hx + .5, h); g.stroke();
        series.forEach(function (s) {
          var y = h - (h - 4) * (s.values[hover] / max);
          g.fillStyle = s.color;
          g.beginPath(); g.arc(hx, y, 3, 0, Math.PI * 2); g.fill();
        });
      }
    }
    render(-1);

    c._render = render;
    c._series = series;
    c._pts = pts;
    c._unit = unit || '';
    if (!c._tipBound) {
      c._tipBound = true;
      c.addEventListener('mousemove', function (ev) {
        var sv = c._series;
        if (!sv || !sv[0] || sv[0].values.length < 2) { return; }
        var rect = c.getBoundingClientRect();
        var n = sv[0].values.length;
        var idx = Math.round((ev.clientX - rect.left) / rect.width * (n - 1));
        if (idx < 0) { idx = 0; }
        if (idx > n - 1) { idx = n - 1; }
        c._render(idx);
        var sp = c._pts, un = c._unit;
        // A live sample counts seconds back from now; a day bucket carries the
        // clock time it stands for.
        var when = (sp && sp[idx] && sp[idx].label) ? sp[idx].label
          : ((sp && sp[idx] && typeof sp[idx].t === 'number')
              ? (sp[idx].t === 0 ? '现在' : (-sp[idx].t) + ' 秒前') : '');
        var html = when ? '<b>' + when + '</b>' : '';
        sv.forEach(function (s) {
          html += '<div><i style="display:inline-block;width:8px;height:8px;'
            + 'border-radius:2px;margin-right:6px;background:' + s.color + '"></i>'
            + esc(s.label || '') + ' ' + s.values[idx] + un + '</div>';
        });
        var tip = monTip();
        tip.innerHTML = html;
        tip.style.display = 'block';
        tip.style.left = (ev.clientX + 12) + 'px';
        tip.style.top = (ev.clientY + 12) + 'px';
      });
      c.addEventListener('mouseleave', function () {
        c._render(-1);
        var tip = document.getElementById('mon-tip');
        if (tip) { tip.style.display = 'none'; }
      });
    }

    var label = panel.querySelector('[data-max="' + id + '"]');
    if (label) { label.textContent = '峰值 ' + max; }
  }


  // A template cannot write `selected` on the right <option>, so a select that
  // carries its current value in data-value applies it after the fragment is
  // in the DOM. Same for the code preview's tabs, which are markup only.
  function applyFragmentWidgets(root) {
    var sels = root.querySelectorAll('select[data-value]');
    for (var i = 0; i < sels.length; i++) {
      var v = sels[i].getAttribute('data-value');
      if (v) { sels[i].value = v; }
    }
    var tabs = root.querySelectorAll('[data-code]');
    for (var t = 0; t < tabs.length; t++) {
      tabs[t].addEventListener('click', function () {
        var box = this.closest('.code-preview');
        var name = this.getAttribute('data-code');
        var all = box.querySelectorAll('[data-code]');
        for (var k = 0; k < all.length; k++) { all[k].classList.remove('on'); }
        this.classList.add('on');
        var bodies = box.querySelectorAll('[data-code-body]');
        for (var b = 0; b < bodies.length; b++) {
          bodies[b].classList.toggle('open',
            bodies[b].getAttribute('data-code-body') === name);
        }
      });
    }
    wireCodeGen(root);
  }
  window.applyFragmentWidgets = applyFragmentWidgets;

  // 激活码生成对话框：POST 生成端点，明文码在文本域里显示一次并提供
  // 复制按钮——服务器只存摘要，关掉对话框就再也拿不回明文。
  function wireCodeGen(root) {
    var form = root.querySelector('#codes-form');
    if (!form || form.getAttribute('data-wired')) { return; }
    form.setAttribute('data-wired', '1');
    var btn = form.querySelector('[data-generate]');
    if (btn) {
      btn.addEventListener('click', function () {
        var data = new FormData(form);
        var parts = [];
        data.forEach(function (v, k) {
          parts.push(encodeURIComponent(k) + '=' + encodeURIComponent(v));
        });
        btn.disabled = true;
        fetch(form.getAttribute('action'), {
          method: 'POST',
          credentials: 'same-origin',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Fragment': '1'
          },
          body: parts.join('&')
        }).then(function (r) {
          if (r.status === 401) { location.href = '/admin/login'; return null; }
          return r.json();
        }).then(function (j) {
          btn.disabled = false;
          if (!j) { return; }
          if (j.code !== '0000') { toast(j.msg || '生成失败', 'bad'); return; }
          var codes = (j.data && j.data.codes) || [];
          var box = root.querySelector('#codes-result');
          var area = root.querySelector('#codes-text');
          if (!box || !area) { return; }
          area.value = codes.join('\n');
          box.style.display = 'block';
          toast('已生成 ' + codes.length + ' 个激活码', 'ok');
        }).catch(function () {
          btn.disabled = false;
          toast('请求失败', 'bad');
        });
      });
    }
    var copy = root.querySelector('[data-copycodes]');
    if (copy) {
      copy.addEventListener('click', function () {
        var area = root.querySelector('#codes-text');
        if (!area) { return; }
        area.select();
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(area.value)
            .then(function () { toast('已复制', 'ok'); })
            .catch(function () { document.execCommand('copy'); });
        } else {
          document.execCommand('copy');
        }
      });
    }
  }

  // ---- wiring -------------------------------------------------------------

  document.addEventListener('click', function (ev) {
    hideTabMenu();
    var a = ev.target.closest('[data-tab]');
    if (a) {
      ev.preventDefault();
      open(a.getAttribute('href'), a.getAttribute('data-title') || a.textContent.trim());
      document.body.classList.remove('side-open');
      return;
    }
    var l = ev.target.closest('[data-load]');
    if (l) {
      ev.preventDefault();
      var href = l.getAttribute('href');
      var path = href.charAt(0) === '?' ? base(state.active) + href : href;
      open(path, l.getAttribute('data-title') || l.textContent.trim());
      return;
    }
    var d = ev.target.closest('[data-dialog]');
    if (d) {
      ev.preventDefault();
      dialog(d.getAttribute('href') || d.getAttribute('data-dialog'),
             d.hasAttribute('data-wide'),
             d.getAttribute('data-title') || d.textContent.trim());
      return;
    }
    var dr = ev.target.closest('[data-drawer]');
    if (dr) {
      ev.preventDefault();
      Layer.drawer({ url: dr.getAttribute('href') || dr.getAttribute('data-drawer'),
                     title: dr.getAttribute('data-title') || dr.textContent.trim(),
                     width: dr.getAttribute('data-width') || '420px' });
      return;
    }
    var p = ev.target.closest('[data-post]');
    if (p) {
      ev.preventDefault();
      var run = function () {
        post(p.getAttribute('data-post'), p.getAttribute('data-args') || '')
          .then(function (j) {
            if (!j) { return; }
            toast(j.msg || '完成', j.code === '0000' ? 'ok' : 'bad');
            if (j.code === '0000') { closeDialog(); reload(true); }
          })
          .catch(function () { toast('请求失败', 'bad'); });
      };
      var confirmText = p.getAttribute('data-confirm');
      if (confirmText) { Layer.confirm(confirmText, run); } else { run(); }
      return;
    }
    var nav = ev.target.closest('[data-tabnav]');
    if (nav) {
      ev.preventDefault();
      var dir = parseInt(nav.getAttribute('data-tabnav'), 10) || 1;
      tabs.scrollLeft = tabs.scrollLeft + dir * Math.max(120, tabs.clientWidth * 0.7);
      return;
    }
    if (ev.target.closest('[data-close]')) { ev.preventDefault(); closeDialog(); }
    if (ev.target.closest('[data-refresh]')) { ev.preventDefault(); reload(); }
    // On a phone the sidebar is a drawer; anywhere else this button is hidden.
    if (ev.target.closest('[data-side]')) {
      ev.preventDefault();
      document.body.classList.toggle('side-open');
      return;
    }
    if (document.body.classList.contains('side-open')
        && !ev.target.closest('.ad-side')) {
      document.body.classList.remove('side-open');
    }
  });

  document.addEventListener('submit', function (ev) {
    var search = ev.target.closest('[data-search]');
    if (search) {
      // A filter bar is a GET: it changes which rows the panel shows, so it
      // reloads the panel in place and leaves the tab where it is.
      ev.preventDefault();
      var parts = [];
      new FormData(search).forEach(function (v, k) {
        if (String(v).length) {
          parts.push(encodeURIComponent(k) + '=' + encodeURIComponent(v));
        }
      });
      var path = search.getAttribute('action') || base(state.active);
      if (parts.length) { path = path + '?' + parts.join('&'); }
      open(path, search.getAttribute('data-title') || path);
      return;
    }
    var form = ev.target.closest('[data-submit]');
    if (!form) { return; }
    ev.preventDefault();
    submit(form);
  });

  // A tip is markup, not a component: data-tip on anything shows a bubble.
  document.addEventListener('mouseover', function (ev) {
    var a = ev.target.closest('[data-tip]');
    if (a) { Layer.tip(a, a.getAttribute('data-tip')); }
  });
  document.addEventListener('mouseout', function (ev) {
    if (ev.target.closest('[data-tip]')) { Layer.untip(); }
  });

  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') { Layer.untip(); hideTabMenu(); Layer.closeTop(); }
  });

  document.addEventListener('DOMContentLoaded', function () {
    panel = el('ad-panel');
    tabs = el('ad-tabs');
    toasts = el('ad-toasts');
    restore();
    var here = normalize(location.pathname + location.search + location.hash);
    rememberPane(location.pathname + location.search + location.hash);
    var title = document.body.getAttribute('data-tab-title') || here;
    if (find(here) < 0) { state.tabs.push({ path: here, title: title }); }
    state.active = here;
    history.replaceState({ path: here }, '', here);
    paint();
    window.addEventListener('resize', paintTabNav);
    // A wheel over the strip pages it sideways, like a browser's tab bar.
    tabs.addEventListener('wheel', function (ev) {
      if (tabs.scrollWidth <= tabs.clientWidth) { return; }
      ev.preventDefault();
      tabs.scrollLeft = tabs.scrollLeft + (ev.deltaY || ev.deltaX);
    }, { passive: false });
    // The first screen is already in the panel, server-rendered.
    startStream();
    wireModelPick(panel);
    window.addEventListener('popstate', restoreHistory);
  });


  // Account menu in the top-right corner.
  (function account() {
    var box = document.querySelector('[data-account]');
    if (!box) { return; }
    var btn = box.querySelector('[data-account-btn]');
    btn.addEventListener('click', function (ev) {
      ev.stopPropagation();
      box.classList.toggle('open');
    });
    document.addEventListener('click', function () { box.classList.remove('open'); });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') { box.classList.remove('open'); }
    });
  })();

  // Ctrl+F filters the sidebar. Chinese entries also match their pinyin
  // initials ("wzgl" -> 文章管理): the first letter of a han character is
  // found by collating it against the 26 boundary characters of the zh-CN
  // order, which needs no lookup table.
  (function menuFilter() {
    var box = document.getElementById('ad-find');
    if (!box) { return; }
    var side = document.querySelector('.ad-side');
    var bounds = '阿八嚓咑妸发旮铪丌咔垃妈拏噢妑七呥仨他屲夕丫帀';
    var letters = 'abcdefghjklmnopqrstwxyz';
    var cache = {};

    function initial(ch) {
      if (cache[ch] !== undefined) { return cache[ch]; }
      var out = ch.toLowerCase();
      if (ch.charCodeAt(0) > 0x3fff) {
        out = '';
        for (var i = bounds.length - 1; i >= 0; i--) {
          if (ch.localeCompare(bounds.charAt(i), 'zh-CN') >= 0) { out = letters.charAt(i); break; }
        }
      }
      cache[ch] = out;
      return out;
    }

    function initials(text) {
      var s = '';
      for (var i = 0; i < text.length; i++) { s += initial(text.charAt(i)); }
      return s;
    }

    function apply() {
      var q = box.value.trim().toLowerCase();
      var items = side.querySelectorAll('a.mi');
      var first = null;
      for (var i = 0; i < items.length; i++) {
        var el = items[i];
        var text = el.textContent.trim();
        var hit = !q || text.toLowerCase().indexOf(q) >= 0 || initials(text).indexOf(q) >= 0;
        el.classList.toggle('filtered', !hit);
        if (hit && !first) { first = el; }
      }
      var groups = side.querySelectorAll('.ad-group');
      for (var g = 0; g < groups.length; g++) {
        var any = false;
        var n = groups[g].nextElementSibling;
        while (n && !n.classList.contains('ad-group')) {
          if (n.classList.contains('mi') && !n.classList.contains('filtered')) { any = true; }
          n = n.nextElementSibling;
        }
        groups[g].classList.toggle('filtered', !any);
      }
      return first;
    }

    box.addEventListener('input', apply);
    box.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') { box.value = ''; apply(); box.blur(); }
      if (ev.key === 'Enter') {
        var first = apply();
        if (first) { first.click(); }
      }
    });
    document.addEventListener('keydown', function (ev) {
      if ((ev.ctrlKey || ev.metaKey) && (ev.key === 'f' || ev.key === 'F')) {
        ev.preventDefault();
        document.body.classList.add('side-open');
        box.focus();
        box.select();
      }
    });
  })();



})();

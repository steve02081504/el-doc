/* Reading progress: a thin scroll bar plus the landing page's "continue" card.
 *
 * Two small promises to the reader: the page visibly advances while you read,
 * and the tutorial remembers where you stopped. Everything stays in
 * localStorage; nothing is sent anywhere.
 */
(function () {
  "use strict";

  var STORE_KEY = "el-doc-progress-v1";
  var MAX_ENTRIES = 80;
  var script = document.currentScript;
  var siteRoot = new URL("../", script ? script.src : window.location.href);

  function store() {
    try {
      var raw = window.localStorage.getItem(STORE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (error) {
      return {};
    }
  }

  function remember(data) {
    try {
      window.localStorage.setItem(STORE_KEY, JSON.stringify(data));
    } catch (error) {
      /* private mode: progress is a nice-to-have, not a requirement */
    }
  }

  function siteRelativePath(url) {
    var path = new URL(url, window.location.href).pathname;
    var root = siteRoot.pathname;
    if (path.indexOf(root) === 0) path = path.slice(root.length);
    return path.replace(/index\.html$/, "");
  }

  function visitCurrentPage() {
    var key = siteRelativePath(window.location.href);
    if (key === "404.html") return;
    var heading = document.querySelector(".md-content h1");
    var data = store();
    data[key] = {
      title: (heading ? heading.textContent : document.title)
        .replace(/[\u00b6#]/g, "")
        .trim(),
      at: Date.now(),
    };
    var keys = Object.keys(data);
    if (keys.length > MAX_ENTRIES) {
      keys
        .sort(function (a, b) {
          return data[a].at - data[b].at;
        })
        .slice(0, keys.length - MAX_ENTRIES)
        .forEach(function (old) {
          delete data[old];
        });
    }
    remember(data);
  }

  var pageList = null;
  function loadPages() {
    if (!pageList) {
      pageList = fetch(new URL("assets/random-pages.json", siteRoot), { cache: "no-cache" })
        .then(function (response) {
          if (!response.ok) throw new Error("page list unavailable");
          return response.json();
        })
        .then(function (urls) {
          return urls.map(function (url) {
            return siteRelativePath(new URL(url || ".", siteRoot).href);
          });
        })
        .catch(function () {
          return [];
        });
    }
    return pageList;
  }

  function renderProgress() {
    var box = document.querySelector("[data-el-progress]");
    if (!box) return;
    loadPages().then(function (pages) {
      if (!pages.length) {
        box.hidden = true;
        return;
      }
      var data = store();
      var visited = pages.filter(function (page) {
        return data[page];
      }).length;
      var count = box.querySelector("[data-el-progress-count]");
      var total = box.querySelector("[data-el-progress-total]");
      var fill = box.querySelector("[data-el-progress-fill]");
      var resume = box.querySelector("[data-el-progress-resume]");
      var reset = box.querySelector("[data-el-progress-reset]");
      if (count) count.textContent = String(visited);
      if (total) total.textContent = " / " + pages.length + " 页";
      if (fill) fill.style.width = Math.round((visited / pages.length) * 100) + "%";

      var here = siteRelativePath(window.location.href);
      var latest = Object.keys(data)
        .filter(function (page) {
          return page !== here && data[page] && pages.indexOf(page) !== -1;
        })
        .sort(function (a, b) {
          return data[b].at - data[a].at;
        })[0];
      if (resume && latest !== undefined) {
        var link = document.createElement("a");
        link.href = new URL(latest, siteRoot).href;
        link.textContent = "继续读：" + data[latest].title;
        resume.replaceChildren("上次读到 ", link);
        resume.hidden = false;
      }

      if (reset && !reset.dataset.bound) {
        reset.dataset.bound = "1";
        reset.addEventListener("click", function () {
          remember({});
          renderProgress();
        });
      }
      box.hidden = false;
    });
  }

  var bar = null;
  function ensureBar() {
    if (!bar || !bar.isConnected) {
      bar = document.getElementById("el-readbar");
      if (!bar) {
        bar = document.createElement("div");
        bar.id = "el-readbar";
        bar.className = "el-readbar";
        bar.setAttribute("aria-hidden", "true");
        document.body.appendChild(bar);
      }
    }
    return bar;
  }

  var pending = false;
  function updateBar() {
    pending = false;
    var element = ensureBar();
    var root = document.documentElement;
    var room = root.scrollHeight - window.innerHeight;
    var ratio = room > 0 ? Math.min(1, Math.max(0, window.scrollY / room)) : 0;
    element.style.transform = "scaleX(" + ratio.toFixed(4) + ")";
  }

  function onScroll() {
    if (pending) return;
    pending = true;
    window.requestAnimationFrame(updateBar);
  }

  function render() {
    visitCurrentPage();
    updateBar();
    renderProgress();
  }

  function start() {
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", updateBar);
    if (window.document$ && typeof window.document$.subscribe === "function") {
      window.document$.subscribe(render);
    } else {
      document.addEventListener("DOMContentLoaded", render);
    }
  }

  start();
})();
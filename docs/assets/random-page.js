/* Footer button that opens a random page of the tutorial. */
(function () {
  "use strict";

  var script = document.currentScript;
  var siteRoot = new URL("../", script ? script.src : window.location.href);
  var pages = [];

  function render() {
    var content = document.querySelector(".md-content__inner");
    if (!content) return;
    var old = content.querySelector(".el-random");
    if (old) old.remove();
    if (pages.length < 2) return;

    var box = document.createElement("div");
    box.className = "el-random";

    var label = document.createElement("span");
    label.className = "el-random__label";
    label.textContent = "不知道读什么？";

    var button = document.createElement("button");
    button.type = "button";
    button.className = "el-random__button";
    button.textContent = "随便翻一页";
    button.addEventListener("click", function () {
      var target = pick();
      if (target) window.location.href = target.href;
    });

    box.appendChild(label);
    box.appendChild(button);
    content.appendChild(box);
  }

  function pick() {
    var here = new URL(window.location.href).pathname;
    var all = pages.map(function (url) {
      return new URL(url || ".", siteRoot);
    });
    var candidates = all.filter(function (url) {
      return url.pathname !== here;
    });
    if (candidates.length === 0) candidates = all;
    return candidates[Math.floor(Math.random() * candidates.length)];
  }

  function load() {
    fetch(new URL("assets/random-pages.json", siteRoot), { cache: "no-cache" })
      .then(function (response) {
        if (!response.ok) throw new Error("random page list unavailable");
        return response.json();
      })
      .then(function (list) {
        pages = list;
        render();
      })
      .catch(function () {
        pages = [];
      });
  }

  function start() {
    if (window.document$ && typeof window.document$.subscribe === "function") {
      window.document$.subscribe(render);
    } else {
      document.addEventListener("DOMContentLoaded", render);
    }
    load();
  }

  start();
})();

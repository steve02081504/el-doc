/* Large references keep only nearby batches mounted. The build preserves every
 * fragment in lightweight placeholders and provides an unchanged full page. */
(function () {
	"use strict";
	var dispose = function () {};
	function start() {
		dispose();
		var root = document.querySelector("[data-virtual-content]");
		if (!root) return;
		var base = new URL(".", location.href);
		var chunks = Array.from(root.children).map(function (element) {
			return { element: element, placeholder: element.innerHTML, visible: false, loading: false, loaded: false };
		});
		var stopped = false;
		var active = 0;
		var observer;
		var navigation = 0;
		function load(chunk) {
			if (chunk.promise) return chunk.promise;
			chunk.loading = true;
			active++;
			chunk.promise = fetch(new URL(chunk.element.dataset.content, base))
				.then(function (response) {
					if (!response.ok) throw new Error("HTTP " + response.status);
					return response.json();
				})
				.then(function (sections) {
					if (stopped) return;
					chunk.element.innerHTML = sections.join("");
					chunk.element.style.minHeight = "0";
					chunk.element.querySelectorAll(".highlight pre").forEach(function (pre) {
						var copy = document.createElement("button");
						copy.className = "el-copy-button";
						copy.textContent = "复制";
						copy.setAttribute("aria-label", "复制代码");
						copy.onclick = function () {
							navigator.clipboard.writeText(pre.querySelector("code").textContent).then(function () {
								copy.textContent = "已复制";
							}, function () { copy.textContent = "复制失败，请手动选择"; });
						};
						pre.before(copy);
					});
					chunk.loaded = true;
					chunk.failed = false;
				})
				.catch(function () {
					if (stopped) return;
					var error = document.createElement("p");
					error.textContent = "内容加载失败。";
					var retry = document.createElement("button");
					retry.textContent = "重试";
					retry.onclick = function () { chunk.promise = null; load(chunk); };
					error.appendChild(retry);
					chunk.element.innerHTML = chunk.placeholder;
					chunk.element.appendChild(error);
					chunk.failed = true;
				})
				.finally(function () {
					chunk.loading = false;
					active--;
					if (!stopped) { trim(); pump(); }
				});
			return chunk.promise;
		}
		function trim() {
			chunks.forEach(function (chunk) {
				if (!chunk.loaded || chunk.visible || chunk.loading || chunk.pinned || chunk.element.contains(document.activeElement)) return;
				chunk.element.style.minHeight = chunk.element.getBoundingClientRect().height + "px";
				chunk.element.innerHTML = chunk.placeholder;
				chunk.loaded = false;
				chunk.promise = null;
			});
		}
		function pump() {
			chunks.forEach(function (chunk) {
				if (active < 2 && chunk.visible && !chunk.loaded && !chunk.loading && !chunk.failed) load(chunk);
			});
		}
		function followHash() {
			var ticket = ++navigation;
			var identity;
			try { identity = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
			var target = document.getElementById(identity);
			if (!target || !root.contains(target)) return;
			var chunk = chunks.find(function (item) { return item.element.contains(target); });
			// Mark the destination before loading, so eviction cannot remove it.
			chunk.visible = true;
			chunk.pinned = true;
			load(chunk).then(function () {
				if (stopped || ticket !== navigation) { chunk.pinned = false; return; }
				var destination = document.getElementById(identity);
				if (destination) destination.scrollIntoView();
				chunk.pinned = false;
			});
		}
		if (window.IntersectionObserver) {
			observer = new IntersectionObserver(function (entries) {
				entries.forEach(function (entry) {
					chunks.find(function (chunk) { return chunk.element === entry.target; }).visible = entry.isIntersecting;
				});
				trim();
				pump();
			}, { rootMargin: "1200px 0px" });
			chunks.forEach(function (chunk) { observer.observe(chunk.element); });
		} else {
			location.replace(new URL("full.html" + location.hash, base));
			return;
		}
		var input = document.querySelector("[data-type-search]");
		var results = document.querySelector("[data-type-results]");
		var indexPromise;
		var searchTicket = 0;
		input.oninput = function () {
			var ticket = ++searchTicket;
			var query = input.value.trim().toLocaleLowerCase();
			results.replaceChildren();
			if (!query) return;
			if (!indexPromise) indexPromise = fetch(new URL("content-index.json", base)).then(function (response) {
				if (!response.ok) throw new Error("index unavailable");
				return response.json();
			}).catch(function () { indexPromise = null; return null; });
			indexPromise.then(function (index) {
				if (stopped || ticket !== searchTicket) return;
				if (!index) { results.textContent = "索引加载失败，请重新输入或打开完整页面。"; return; }
				var matches = index.filter(function (item) { return item.title.toLocaleLowerCase().includes(query); });
				var count = document.createElement("p");
				count.textContent = matches.length + " 项匹配（最多显示 40 项，请输入更完整的名称缩小范围）";
				results.appendChild(count);
				matches.slice(0, 40).forEach(function (item) {
					var link = document.createElement("a");
					link.href = "#" + encodeURIComponent(item.id);
					link.textContent = item.title;
					var row = document.createElement("div");
					row.appendChild(link);
					results.appendChild(row);
				});
			});
		};
		function onClick(event) {
			var link = event.target.closest("a[href^='#']");
			if (link && link.hash === location.hash) followHash();
		}
		window.addEventListener("hashchange", followHash);
		document.addEventListener("click", onClick);
		dispose = function () {
			stopped = true;
			observer.disconnect();
			window.removeEventListener("hashchange", followHash);
			document.removeEventListener("click", onClick);
		};
		followHash();
	}
	if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(start);
	else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
	else start();
})();

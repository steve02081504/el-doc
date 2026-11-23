(function () {
  "use strict";

  const selector = ".el-code-link";
  const previews = new Map();
  const root = document.documentElement;
  const popup = document.createElement("div");
  popup.className = "el-code-preview";
  popup.id = "el-code-preview";
  popup.setAttribute("role", "tooltip");
  popup.hidden = true;
  document.body.append(popup);

  let active;
  let showTimer;
  let hideTimer;

  function excerpt(text, length) {
    return text.length > length ? text.slice(0, length).trimEnd() + "…" : text;
  }

  function extract(heading) {
    if (!heading) return null;
    const row = heading.closest("tr");
    if (row && row.cells.length >= 3) {
      return {
        title: row.cells[0].textContent.trim(),
        signature: excerpt(row.cells[1].querySelector("code:last-child")?.textContent.trim() || "", 240),
        summary: excerpt(row.cells[2].textContent.trim(), 240),
      };
    }
    const title = Array.from(heading.childNodes)
      .filter(node => !node.classList?.contains("headerlink"))
      .map(node => node.textContent).join("").trim();
    let summary = "";
    let signature = "";
    for (let section = heading.nextElementSibling; section; section = section.nextElementSibling) {
      if (/^H[1-6]$/.test(section.tagName)) break;
      if (!summary && section.matches("p")) {
        const text = section.textContent.trim();
        if (!text.startsWith("源码：")) summary = excerpt(text, 240);
      }
      if (!signature && section.matches(".language-el-signature")) signature = excerpt(section.textContent.trim(), 240);
      if (summary && signature) break;
    }
    return { title, summary, signature };
  }

  async function fetchContent(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(response.statusText);
    return response;
  }

  async function readPreview(url) {
    const target = url.hash ? "#" + CSS.escape(decodeURIComponent(url.hash.slice(1))) : "h1";
    url.hash = "";
    const current = new URL(location.href);
    current.hash = "";
    const page = url.href === current.href ? document :
      new DOMParser().parseFromString(await (await fetchContent(url)).text(), "text/html");
    const heading = page.querySelector(".md-content__inner")?.querySelector(target);
    const chunk = heading?.matches("span") && heading.parentElement.closest(".el-virtual-chunk[data-content]");
    if (!chunk || heading.parentElement !== chunk) return extract(heading);

    const response = await fetchContent(new URL(chunk.dataset.content, url));
    const template = document.createElement("template");
    template.innerHTML = (await response.json()).join("");
    return extract(template.content.querySelector(target));
  }

  function load(link) {
    const url = new URL(link.href);
    const key = url.href;
    if (!previews.has(key)) {
      previews.set(key, readPreview(url).catch(() => {
        previews.delete(key);
        return null;
      }));
    }
    return previews.get(key);
  }

  function close() {
    clearTimeout(showTimer);
    clearTimeout(hideTimer);
    active?.removeAttribute("aria-describedby");
    active = null;
    popup.hidden = true;
  }

  function place() {
    if (popup.hidden || !active) return;
    const bounds = active.getBoundingClientRect();
    if (!active.isConnected || bounds.bottom <= 0 || bounds.top >= innerHeight ||
        bounds.right <= 0 || bounds.left >= innerWidth) {
      close();
      return;
    }
    const gap = 6;
    const left = Math.max(gap, Math.min(bounds.left, innerWidth - popup.offsetWidth - gap));
    const bottom = bounds.bottom + gap;
    const top = bottom + popup.offsetHeight <= innerHeight ? bottom : bounds.top - popup.offsetHeight - gap;
    popup.style.left = left + "px";
    popup.style.top = Math.max(gap, top) + "px";
  }

  function open(link) {
    clearTimeout(hideTimer);
    if (active === link) return;
    close();
    active = link;
    showTimer = setTimeout(async () => {
      const preview = await load(link);
      if (active !== link || !link.isConnected || !preview?.title) return;
      const title = document.createElement("strong");
      title.textContent = preview.title;
      popup.replaceChildren(title);
      if (preview.signature) {
        const signature = document.createElement("code");
        signature.textContent = preview.signature;
        popup.append(signature);
      }
      if (preview.summary) {
        const summary = document.createElement("p");
        summary.textContent = preview.summary;
        popup.append(summary);
      }
      link.setAttribute("aria-describedby", popup.id);
      popup.hidden = false;
      place();
    }, 240);
  }

  document.addEventListener("pointerover", event => {
    if (event.pointerType === "touch") return;
    const link = event.target.closest(selector);
    if (link) open(link);
    if (popup.contains(event.target)) clearTimeout(hideTimer);
  });
  document.addEventListener("pointerout", event => {
    if (event.pointerType === "touch" || !active) return;
    if (!active.contains(event.target) && !popup.contains(event.target)) return;
    if (active.contains(event.relatedTarget) || popup.contains(event.relatedTarget)) return;
    if (document.activeElement !== active) hideTimer = setTimeout(close, 120);
  });
  document.addEventListener("focusin", event => {
    if (event.target.matches(selector)) open(event.target);
  });
  document.addEventListener("focusout", event => {
    if (event.target === active) close();
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Alt") root.classList.add("el-show-code-links");
    if (event.key === "Escape" && active) close();
  });
  document.addEventListener("keyup", event => {
    if (event.key === "Alt") root.classList.remove("el-show-code-links");
  });
  window.addEventListener("blur", () => {
    root.classList.remove("el-show-code-links");
    close();
  });
  window.addEventListener("resize", place);
  window.addEventListener("scroll", place, { capture: true, passive: true });
  window.document$?.subscribe(() => {
    root.classList.remove("el-show-code-links");
    if (active && !active.isConnected) close();
  });
})();

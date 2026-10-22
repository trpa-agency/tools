/* bmp.trpa.gov, shared behavior.
   - mobile nav toggle and aria-current on the active link
   - document lists rendered from data/documents.json into [data-doc-section="slug"]
   - handbook chapters and toolkit rendered from data/handbook.json
   - photo gallery rendered from data/gallery.json with a <dialog> lightbox
   - live counts from the BMP_Status map service into [data-stat]
   Every page loads this file; each block only runs when its container exists. */
(function () {
  "use strict";

  const BMP = (window.BMP = window.BMP || {});

  // Service endpoints live here so a URL change is one edit.
  BMP.config = {
    bmpStatusLayer: "https://maps.trpa.org/server/rest/services/BMP_Status/MapServer/5",
    parcelTracker: "https://parcels.laketahoeinfo.org/parcels/",
    mapTool: "map.html",
    hotline: "(775) 589-5202",
    email: "bmp@trpa.gov",
    // Survey123 links. Leave empty until the forms are published (docs/FORMS.md); pages fall
    // back to the email path while they are empty.
    maintenanceForm: "",
    evaluationForm: ""
  };

  // ── ArcGIS REST query with a JSONP fallback. On the TRPA office network
  // fetch() to maps.trpa.org fails on CORS; a script tag is not subject to
  // CORS and ArcGIS REST honors callback=. Same pattern as tools.trpa.gov.
  BMP.query = async function (url, params) {
    const qs = new URLSearchParams({ f: "json", ...params });
    try {
      const resp = await fetch(`${url}/query?${qs}`);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const json = await resp.json();
      if (json.error) throw new Error(json.error.message || "Service error");
      return json;
    } catch (err) {
      return new Promise((resolve, reject) => {
        const cb = "bmpcb_" + Math.random().toString(36).slice(2);
        const s = document.createElement("script");
        const timer = setTimeout(() => { cleanup(); reject(err); }, 20000);
        function cleanup() { clearTimeout(timer); delete window[cb]; s.remove(); }
        window[cb] = (json) => { cleanup(); json && json.error ? reject(new Error(json.error.message)) : resolve(json); };
        s.onerror = () => { cleanup(); reject(err); };
        s.src = `${url}/query?${new URLSearchParams({ ...params, f: "json", callback: cb })}`;
        document.head.appendChild(s);
      });
    }
  };

  BMP.escape = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  // Resolve a document href: absolute URLs pass through, everything else hangs off docBase.
  BMP.docUrl = function (href, docBase) {
    if (!href) return "#";
    if (/^(https?:)?\/\//i.test(href) || href.startsWith("#") || href.startsWith("mailto:")) return href;
    // Encode spaces and other unsafe characters once; leave existing %xx escapes alone.
    const safe = href.split("/").map((seg) => encodeURIComponent(decodeURIComponent(seg))).join("/");
    return docBase.replace(/\/?$/, "/") + safe;
  };

  BMP.loadJson = (() => {
    const cache = {};
    return (path) => (cache[path] ||= fetch(path).then((r) => { if (!r.ok) throw new Error(`${path}: HTTP ${r.status}`); return r.json(); }));
  })();

  // ── Online forms: <a data-form="maintenanceForm" hidden> shows once the Survey123 link is configured
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-form]").forEach((a) => {
      const url = BMP.config[a.dataset.form];
      if (url) { a.href = url; a.hidden = false; a.target = "_blank"; a.rel = "noopener"; }
    });
    document.querySelectorAll("[data-form-fallback]").forEach((el) => { if (BMP.config[el.dataset.formFallback]) el.hidden = true; });
  });

  // ── Header: mobile toggle, current page
  document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector(".nav-toggle");
    const nav = document.getElementById("site-nav");
    if (toggle && nav) {
      toggle.addEventListener("click", () => {
        const open = nav.classList.toggle("open");
        toggle.setAttribute("aria-expanded", String(open));
      });
    }
    const here = location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll(".site-nav a, .footer-col a").forEach((a) => {
      const target = (a.getAttribute("href") || "").split("#")[0];
      if (target && target === here) a.setAttribute("aria-current", "page");
    });
    document.querySelectorAll('a[href^="http"]').forEach((a) => {
      if (!a.hostname.endsWith("trpa.gov") && !a.hostname.endsWith(location.hostname)) a.rel = "noopener";
    });
  });

  // ── Inline document links: <a href="(legacy URL)" data-doc="relative/path.pdf">
  // The static href works without JavaScript; once documents.json loads, the href is
  // rebuilt from docBase so moving the files is a one-line change in that file.
  async function rewriteDocLinks() {
    const links = document.querySelectorAll("a[data-doc]");
    if (!links.length) return;
    const data = await BMP.loadJson("data/documents.json");
    links.forEach((a) => { a.href = BMP.docUrl(a.dataset.doc, data.docBase); });
  }

  // ── Document lists
  const TYPE_LABEL = { pdf: "PDF", xlsx: "Excel", doc: "Word", dwg: "DWG", video: "Video", link: "Link", page: "Page" };

  function docItemHTML(item, docBase) {
    const type = item.type || "link";
    const href = BMP.docUrl(item.href, docBase);
    const external = /^https?:/i.test(href) && !href.includes(location.hostname);
    const extra = item.es
      ? `<a class="doc-extra" href="${BMP.escape(BMP.docUrl(item.es, docBase))}" lang="es" title="Versión en español">Español</a>`
      : "";
    return `<li class="doc-item">
      <span class="doc-type ${type}">${TYPE_LABEL[type] || type}</span>
      <span class="doc-body">
        <a class="doc-title" href="${BMP.escape(href)}"${external || type === "pdf" ? ' target="_blank" rel="noopener"' : ""}${item.lang ? ` lang="${item.lang}"` : ""}>${BMP.escape(item.title)}</a>
        ${item.note ? `<span class="doc-note">${BMP.escape(item.note)}</span>` : ""}
      </span>
      ${extra}
    </li>`;
  }

  async function renderDocSections() {
    const holders = document.querySelectorAll("[data-doc-section]");
    if (!holders.length) return;
    const data = await BMP.loadJson("data/documents.json");
    const byslug = Object.fromEntries(data.sections.map((s) => [s.slug, s]));
    holders.forEach((el) => {
      const slugs = el.dataset.docSection.split(/\s+/);
      const showHeading = el.dataset.heading !== "no";
      el.innerHTML = slugs.map((slug) => {
        const sec = byslug[slug];
        if (!sec) return `<p class="empty-note">Section "${BMP.escape(slug)}" not found.</p>`;
        const items = sec.items.map((it) => docItemHTML(it, data.docBase)).join("");
        return `<section class="doc-section" id="${sec.slug}" data-search-group>
          ${showHeading ? `<h2>${BMP.escape(sec.name)}</h2><p class="section-desc">${BMP.escape(sec.description || "")}</p>` : ""}
          <ul class="doc-list ${sec.items.length > 6 ? "doc-grid" : ""}">${items}</ul>
        </section>`;
      }).join("");
    });
    wireFilter();
  }

  // One text filter per page: hides doc items (and whole sections) that do not match.
  function wireFilter() {
    const input = document.getElementById("doc-filter");
    if (!input) return;
    const count = document.getElementById("doc-filter-count");
    const apply = () => {
      const q = (input.value || "").trim().toLowerCase();
      let shown = 0;
      document.querySelectorAll(".doc-item, .toolkit-list li:not(.heading)").forEach((li) => {
        const hit = !q || li.textContent.toLowerCase().includes(q);
        li.hidden = !hit;
        if (hit) shown++;
      });
      document.querySelectorAll("[data-search-group]").forEach((sec) => {
        sec.hidden = q && !sec.querySelector(".doc-item:not([hidden]), .toolkit-list li:not([hidden]):not(.heading)");
      });
      if (count) count.textContent = q ? `${shown} match${shown === 1 ? "" : "es"}` : "";
    };
    input.addEventListener("calciteInputInput", apply);
    input.addEventListener("input", apply);
  }

  // ── Handbook
  async function renderHandbook() {
    const chapters = document.querySelector("[data-handbook-chapters]");
    const toolkit = document.querySelector("[data-handbook-toolkit]");
    if (!chapters && !toolkit) return;
    const [hb, docs] = await Promise.all([BMP.loadJson("data/handbook.json"), BMP.loadJson("data/documents.json")]);
    const base = docs.docBase;
    const link = (href, text, cls = "") => `<a class="${cls}" href="${BMP.escape(BMP.docUrl(href, base))}" target="_blank" rel="noopener">${BMP.escape(text)}</a>`;

    if (chapters) {
      chapters.innerHTML = `<ul class="doc-list">
        <li class="doc-item"><span class="doc-type pdf">PDF</span><span class="doc-body">${link(hb.complete.href, hb.complete.title, "doc-title")}<span class="doc-note">Single file, ${BMP.escape(hb.complete.note)}. The chapters below are smaller downloads.</span></span></li>
        ${hb.chapters.map((ch) => {
          const inPage = ch.href.startsWith("#");
          const title = inPage ? `<a class="doc-title" href="${ch.href}">${BMP.escape(ch.title)}</a>` : link(ch.href, ch.title, "doc-title");
          const supp = (ch.supplements || []).map((s) => `<li>${link(s.href, s.title)}</li>`).join("");
          return `<li class="doc-item"><span class="doc-type ${inPage ? "page" : "pdf"}">${inPage ? "Page" : "PDF"}</span><span class="doc-body">${title}${ch.note ? `<span class="doc-note">${BMP.escape(ch.note)}</span>` : ""}${supp ? `<ul class="small" style="margin:0.4rem 0 0.2rem">${supp}</ul>` : ""}</span></li>`;
        }).join("")}
      </ul>`;
    }

    if (toolkit) {
      toolkit.innerHTML = hb.toolkit.map((sec) => `<section class="toolkit-section" id="toolkit-${sec.number.replace(".", "-")}" data-search-group>
        <h3><span class="num">${sec.number}</span> ${BMP.escape(sec.name)} <span class="small" style="font-weight:400">${link(sec.intro, "Introduction (PDF)")}</span></h3>
        <div class="toolkit-cols">
          <div>
            <h4>Fact sheets</h4>
            <ul class="toolkit-list">${sec.factSheets.map((f) => f.heading
              ? `<li class="heading">${link(f.href, f.name)}</li>`
              : `<li>${link(f.href, f.name)}</li>`).join("")}</ul>
          </div>
          <div>
            <h4>Standard drawings</h4>
            <ul class="toolkit-list">${sec.drawings.map((d) => `<li><span class="dw-id">${d.id}</span><span>${BMP.escape(d.name)}</span><span class="dw-links">${link(d.pdf, "PDF")}${d.dwg ? link(d.dwg, "DWG") : '<span class="muted small">no DWG</span>'}</span></li>`).join("")}</ul>
          </div>
        </div>
      </section>`).join("");
    }
    wireFilter();
  }

  // ── Gallery
  async function renderGallery() {
    const holder = document.querySelector("[data-gallery]");
    if (!holder) return;
    const data = await BMP.loadJson("data/gallery.json");
    const only = holder.dataset.gallery ? holder.dataset.gallery.split(/\s+/) : null;
    const groups = data.groups.filter((g) => !only || only.includes(g.slug));
    const all = [];
    holder.innerHTML = groups.map((g) => {
      const imgs = data.images.filter((i) => i.group === g.slug);
      const html = imgs.map((img) => {
        const idx = all.push(img) - 1;
        return `<button class="gallery-item" type="button" data-index="${idx}" aria-label="${BMP.escape(img.caption)}, open larger">
          <img src="assets/gallery/thumbs/${img.file}" alt="${BMP.escape(img.caption)}" loading="lazy" width="560" height="420">
          <figcaption aria-hidden="true">${BMP.escape(img.caption)}</figcaption>
        </button>`;
      }).join("");
      return `<section class="gallery-group" id="${g.slug}">
        <h2>${BMP.escape(g.name)} <span class="muted small" style="font-weight:400">${imgs.length}</span></h2>
        <p class="muted">${BMP.escape(g.description)}</p>
        <div class="gallery-grid">${html}</div>
      </section>`;
    }).join("");

    // Lightbox
    let dlg = document.getElementById("lightbox");
    if (!dlg) {
      dlg = document.createElement("dialog");
      dlg.id = "lightbox";
      dlg.className = "lightbox";
      dlg.innerHTML = `<div class="lightbox-frame">
        <img id="lightbox-img" alt="">
        <div class="lightbox-caption" id="lightbox-caption"></div>
        <button class="lightbox-nav lightbox-prev" type="button" aria-label="Previous photo">&lsaquo;</button>
        <button class="lightbox-nav lightbox-next" type="button" aria-label="Next photo">&rsaquo;</button>
        <button class="lightbox-close" type="button" aria-label="Close">&times;</button>
      </div>`;
      document.body.appendChild(dlg);
    }
    let current = 0;
    const img = dlg.querySelector("#lightbox-img");
    const cap = dlg.querySelector("#lightbox-caption");
    const show = (i) => {
      current = (i + all.length) % all.length;
      const it = all[current];
      img.src = `assets/gallery/${it.file}`;
      img.alt = it.caption;
      cap.textContent = `${it.caption} (${current + 1} of ${all.length})`;
    };
    holder.addEventListener("click", (e) => {
      const btn = e.target.closest(".gallery-item");
      if (!btn) return;
      show(Number(btn.dataset.index));
      dlg.showModal();
    });
    dlg.querySelector(".lightbox-prev").addEventListener("click", () => show(current - 1));
    dlg.querySelector(".lightbox-next").addEventListener("click", () => show(current + 1));
    dlg.querySelector(".lightbox-close").addEventListener("click", () => dlg.close());
    dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") show(current - 1);
      if (e.key === "ArrowRight") show(current + 1);
    });
  }

  // ── Live counts: [data-stat="bmp|sco|parcels|evaluated"]
  async function renderStats() {
    const els = document.querySelectorAll("[data-stat]");
    if (!els.length) return;
    const where = {
      bmp: "BMPStatus='BMP'",
      sco: "BMPStatus='SCO'",
      parcels: "1=1",
      evaluated: "EvaluationComplete=1 AND BMPStatus='NOBMP'"
    };
    await Promise.all([...els].map(async (el) => {
      try {
        const json = await BMP.query(BMP.config.bmpStatusLayer, { where: where[el.dataset.stat] || "1=1", returnCountOnly: "true" });
        el.textContent = Number(json.count).toLocaleString();
      } catch (err) {
        // leave the static fallback number in the markup
        el.title = "Live count unavailable; showing the last published figure.";
      }
    }));
  }

  document.addEventListener("DOMContentLoaded", () => {
    rewriteDocLinks().catch(console.error);
    renderDocSections().catch(console.error);
    renderHandbook().catch(console.error);
    renderGallery().catch(console.error);
    renderStats().catch(console.error);
  });
})();

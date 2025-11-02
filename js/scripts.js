// js/scripts.js

async function loadIncludes() {
  try {
    // Header
    const headerRes = await fetch("header.html");
    if (headerRes.ok) {
      const headerHtml = await headerRes.text();
      document.getElementById("header-placeholder").innerHTML = headerHtml;
      initNavMenu();
      highlightActiveLink();

      // ✅ Scroll fix: ensure the page resets to top after header is injected
      if (window.location.pathname.endsWith("index.html") || window.location.pathname === "/") {
        requestAnimationFrame(() => window.scrollTo({ top: 0, behavior: "instant" }));
      }
    } else {
      console.error("Header fetch failed:", headerRes.status);
    }

    // Footer
    const footerRes = await fetch("footer.html");
    if (footerRes.ok) {
      const footerHtml = await footerRes.text();
      document.getElementById("footer-placeholder").innerHTML = footerHtml;
    } else {
      console.error("Footer fetch failed:", footerRes.status);
    }
  } catch (err) {
    console.error("Include error:", err);
  }
}

// ---- Mobile Nav Toggle ----
function initNavMenu() {
  const navToggle = document.getElementById("nav-toggle");
  const navMenu = document.getElementById("nav-menu");

  if (navToggle && navMenu) {
    navToggle.addEventListener("click", () => {
      navMenu.classList.toggle("show");
    });
  }
}

// ---- Highlight Active Nav Link ----
function highlightActiveLink() {
  const links = document.querySelectorAll(".nav-link");
  const currentPage = window.location.pathname.split("/").pop().toLowerCase();

  links.forEach(link => {
    const linkPage = link.getAttribute("href").split("/").pop().toLowerCase();
    if (linkPage === currentPage) link.classList.add("active");
    if ((currentPage === "" || currentPage === "index.html") && linkPage === "home.html")
      link.classList.add("active");
  });
}

// ---- Run when DOM is ready ----
document.addEventListener("DOMContentLoaded", () => {
  if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
  }
  loadIncludes();
});

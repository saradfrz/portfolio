/* Browser-only enhancements. All portfolio content is rendered by Python. */
(() => {
  "use strict";
  const data = document.getElementById("typing-data");
  const out = document.getElementById("typed");
  const lines = JSON.parse(data.textContent);
  const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let timer;
  function startTyping() {
    clearTimeout(timer);
    if (!lines.length) { out.textContent = ""; return; }
    if (motion.matches) { out.textContent = lines[0]; return; }
    let line = 0, pos = 0, deleting = false;
    out.textContent = "";
    function tick() {
      const text = lines[line];
      pos += deleting ? -1 : 1;
      out.textContent = text.slice(0, pos);
      let delay = deleting ? 22 : 55;
      if (!deleting && pos === text.length) { deleting = true; delay = 1700; }
      else if (deleting && pos === 0) { deleting = false; line = (line + 1) % lines.length; delay = 350; }
      timer = setTimeout(tick, delay);
    }
    tick();
  }
  startTyping();
  motion.addEventListener("change", startTyping);
  // External shields.io badges degrade to text chips when unavailable.
  for (const img of document.querySelectorAll("img.badge")) {
    const fallback = () => {
      const chip = document.createElement("span");
      chip.className = "chip";
      chip.textContent = img.alt;
      img.replaceWith(chip);
    };
    img.addEventListener("error", fallback, { once: true });
    if (img.complete && !img.naturalWidth) fallback();
  }
  document.getElementById("year").textContent = new Date().getFullYear();
})();

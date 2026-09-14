(() => {
  "use strict";
  const storageKey = "starhunt.language";
  const valid = value => value === "en" || value === "sv";
  const entry = document.documentElement.dataset.languageEntry;

  if (entry) {
    const url = new URL(window.location.href);
    let language = url.searchParams.get("lang");
    if (!valid(language)) language = { "#english": "en", "#svenska": "sv" }[url.hash];
    if (!valid(language)) {
      try { language = localStorage.getItem(storageKey); } catch { /* Storage is optional. */ }
    }
    if (!valid(language)) language = navigator.language.toLowerCase().startsWith("sv") ? "sv" : "en";
    const page = entry === "home" ? "" : entry + "/";
    window.location.replace("/" + language + "/" + page);
    return;
  }

  const select = document.querySelector("#language");
  if (!select) return;
  document.querySelector(".language-picker").hidden = false;
  select.addEventListener("change", () => {
    const destination = new URL(select.value, window.location.href);
    const language = destination.pathname.split("/")[1];
    if (destination.origin !== window.location.origin || !valid(language)) return;
    try { localStorage.setItem(storageKey, language); } catch { /* The URL keeps the choice. */ }
    window.location.assign(destination.href);
  });
  // Restore the dropdown to the URL's language when returning via browser Back.
  window.addEventListener("pageshow", () => {
    for (const option of select.options) option.selected = option.defaultSelected;
  });
})();

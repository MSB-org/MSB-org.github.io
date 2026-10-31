// Único script do site: abre e fecha o menu em telas pequenas. Todo o resto funciona sem JavaScript.
(function () {
  var btn = document.querySelector(".menu-btn");
  var nav = document.getElementById("nav");
  if (!btn || !nav) return;
  btn.addEventListener("click", function () {
    var aberto = nav.classList.toggle("aberto");
    btn.setAttribute("aria-expanded", String(aberto));
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && nav.classList.contains("aberto")) {
      nav.classList.remove("aberto");
      btn.setAttribute("aria-expanded", "false");
      btn.focus();
    }
  });
})();

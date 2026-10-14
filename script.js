// Marque la section courante dans la barre du haut, et neutralise les liens
// encore à remplir (inscription, courriel) pour qu'ils ne mènent nulle part.

(function () {
  "use strict";

  var liens = Array.prototype.slice.call(
    document.querySelectorAll('.topbar nav a[href^="#"]')
  );

  if (liens.length && "IntersectionObserver" in window) {
    var parSection = {};
    liens.forEach(function (lien) {
      var cible = document.querySelector(lien.getAttribute("href"));
      if (cible) parSection[cible.id] = lien;
    });

    var observateur = new IntersectionObserver(
      function (entrees) {
        entrees.forEach(function (entree) {
          var lien = parSection[entree.target.id];
          if (!lien) return;
          if (entree.isIntersecting) {
            liens.forEach(function (autre) { autre.removeAttribute("aria-current"); });
            lien.setAttribute("aria-current", "true");
          }
        });
      },
      { rootMargin: "-20% 0px -70% 0px" }
    );

    Object.keys(parSection).forEach(function (id) {
      var section = document.getElementById(id);
      if (section) observateur.observe(section);
    });
  }

  // Les ancres encore vides ne doivent pas renvoyer en haut de page.
  document.querySelectorAll('a[data-placeholder][href="#"]').forEach(function (a) {
    a.setAttribute("aria-disabled", "true");
    a.addEventListener("click", function (e) { e.preventDefault(); });
  });
})();

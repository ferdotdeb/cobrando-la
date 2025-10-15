// ACORDEÓN FAQ
(function () {
  const faqButtons = document.querySelectorAll(".faq-button");

  faqButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      const isExpanded = button.getAttribute("aria-expanded") === "true";
      const targetId = button.getAttribute("aria-controls");
      const targetContent = document.getElementById(targetId);
      const icon = button.querySelector(".faq-icon");

      // Toggle estado
      button.setAttribute("aria-expanded", !isExpanded);

      if (targetContent) {
        targetContent.classList.toggle("hidden");
      }

      // Rotar icono
      if (icon) {
        icon.style.transform = isExpanded ? "rotate(0deg)" : "rotate(180deg)";
      }
    });

    // Soporte teclado (Enter y Espacio)
    button.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        button.click();
      }
    });
  });
})();

document.addEventListener("DOMContentLoaded", () => {
  const menu = document.querySelector("#mainNavigation");
  if (!menu) return;

  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      if (window.innerWidth < 992 && menu.classList.contains("show")) {
        bootstrap.Collapse.getOrCreateInstance(menu).hide();
      }
    });
  });
});

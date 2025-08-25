const btn = document.getElementById("menu-toggle");
const sidebar = document.querySelector(".sidebar");
btn?.addEventListener("click", () => sidebar.classList.toggle("open"));
document.addEventListener("click", (e) => {
    if (!sidebar.classList.contains("open")) return;
    const inside = e.target.closest(".sidebar") || e.target.closest("#menu-toggle");
    if (!inside) sidebar.classList.remove("open");
});
/* custom.js */

document.addEventListener("DOMContentLoaded", function () {
    // Add a fade-in effect to elements with class "fade-in"
    const elements = document.querySelectorAll(".fade-in");
    elements.forEach(function (element) {
        element.classList.add("fade");
    });
});

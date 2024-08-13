document.addEventListener("DOMContentLoaded", function () {
    // Add a fade-in effect to elements with class "fade-in"
    const elements = document.querySelectorAll(".fade-in");
    elements.forEach(function (element) {
        element.classList.add("fade");
        element.style.opacity = 0;
        element.addEventListener("transitionend", function () {
            element.style.opacity = 1;
        });
    });

    // Handle form submission when the "Submit" button is clicked
    const submitButton = document.getElementById("submitButton");
    submitButton.addEventListener("click", function (event) {
        // Prevent the default form submission
        event.preventDefault();
        
        // Trigger the form submission
        const form = document.getElementById("dataForm");
        form.submit();
    });
});

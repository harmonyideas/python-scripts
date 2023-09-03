document.querySelector("#filejob").addEventListener('click', function(e) {
    if (e.target.classList.contains('collapsible')) {
        var coll = document.getElementsByClassName("collapsible");
        e.target.classList.toggle("active");
        var content = e.target.nextElementSibling;
        if (content.style.display === "block") {
            e.target.innerHTML = 'Show Results';
            content.style.display = "none";
        } else {
            e.target.innerHTML = 'Close Results';
            content.style.display = "block";
        }

    }
});
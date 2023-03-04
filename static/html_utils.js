function readWebpage() {
    // Get the rendered HTML content of the page
    var content = document.documentElement.outerHTML;
    
    var data = { webpage: content };
    fetch("/read-page", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
}

function accordian_trigger() {
    var acc = document.getElementsByClassName("accordion");
    var i;
    
    for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
        panel.style.display = "none";
        } else {
        panel.style.display = "block";
        }
    });
    }
}


function hideWhenScrolled(elementClass) {
    window.addEventListener("scroll", function() {
    var element = document.querySelector(elementClass);
    if (window.scrollY > 0) {
        element.classList.add("hidden");
    } else {
        element.classList.remove("hidden");
    }
    });
}

function goBack() {
    window.history.back();
}
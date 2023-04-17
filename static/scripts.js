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

//----------------- home page functions ------------------------------//
function logout() {
    fetch("/signout", {
        method:"POST"
    }).then((response) => {
        window.location.href = response.url;
    });
}

function getSelected(remove) {
    let ingredients = [];
    checkboxes = document.getElementsByName('ingredient');

    for (const ingredient of checkboxes) 
        if (ingredient.checked) 
            ingredients.push(ingredient.parentNode.id);

    if (remove)
        for (const ingredient of ingredients) 
            document.getElementById(ingredient).remove();
        
    return ingredients;
}

function remove() {
    fetch("/removeItems", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'ingredients': getSelected(true)
        })
    })
}

function search() {
    fetch("/searchItems", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'ingredients': getSelected()
        })
    }).then((response) => {
        window.location.href = response.url;
    });
}

function sendImageToBarcodeScanner() {
  var imageInput = document.getElementById("imageInput");
  var image = imageInput.files[0];

  var formData = new FormData();
  formData.append("image", image);

  fetch("/scan-barcode", {
    method: "POST",
    body: formData
  }).then((response) => {
    return response.json(); // Parse response as JSON data
  }).then((items) => {
    addIngredients(items)
  })
}

function sendToSpeech() {
  event.preventDefault();
  fetch("/speech", {
    method: "POST",
  }).then((response) => {
    return response.json(); // Parse response as JSON data
  }).then((items) => {
    addIngredients(items)
  })
}

function addIngredients(items) {
    for (const item of items) {
        const div = document.createElement('div');
        div.className = 'form-check';
        div.id = item;
        div.innerHTML = `
            <input class="form-check-input" name="ingredient" type="checkbox" value="" id="flexCheckDefault" checked="true">
            <label class="form-check-label" for="flexCheckDefault">
                ${item.charAt(0).toUpperCase() + item.slice(1)}
            </label>
        `
        document.getElementById('ingredients').appendChild(div)
    }
}

var checked = true;
function selectAll() {
    checkboxes = document.getElementsByName('ingredient');
    for(checkbox of checkboxes) checkbox.checked = !checked;
    checked = !checked;
}

function handleEnterKeyDown(event) {
  if (event.keyCode === 13) { // check if Enter key was pressed
    event.preventDefault();
    let data = { ingredients: document.getElementById("text-box").value};
    fetch("/text", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }).then((response) => {
      return response.json();
    }).then((items) => {
        addIngredients(items)
        document.getElementById("text-box").value = "";
    })
 }
}

function takePicture() {
  fetch("/savePicture", {
    method: "POST",
  })
}

function sendImageToAI() {
  var imageInput = document.getElementById("imageInputAI");
  var image = imageInput.files[0];

  var formData = new FormData();
  formData.append("image", image);

  fetch("/run-AI", {
    method: "POST",
    body: formData
  }).then((response) => {
    return response.json(); // Parse response as JSON data
  }).then((items) => {
    addIngredients(items)
  })
}

function startCarousel() {
        var images = document.querySelectorAll(".image-carousel img");
        var index = 0;
        setInterval(function() {
            images[index].classList.remove("active");
            index = (index + 1) % images.length;
            images[index].classList.add("active");
        }, 3000);
    }
    startCarousel();

function clearAllFields() {
  var inputFields = document.querySelectorAll('input, textarea');

  for (var i = 0; i < inputFields.length; i++) {
    if (inputFields[i].type === 'file') {
      inputFields[i].value = null;
    } else {
      inputFields[i].value = "";
    }
  }
}

//----------------- results page functions ------------------------------//
function toggleLikes(like) {
    let counter = document.getElementById('counter-' + like.id);
    let liked = true;
    
    if (like.name == 'False') {
        like.src = "static/images/True.png";
        like.name = "True";
        counter.innerHTML = Number(counter.innerHTML) + 1;
    } else {
        like.src = "static/images/False.png";
        like.name = "False";
        counter.innerHTML = Number(counter.innerHTML) - 1;
        liked = false;
    }

    fetch('/like', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'id': like.id,
            'count': counter.innerHTML,
            'liked': liked
        })
    })
}

//Dark mode
function toggleDarkMode() {
    var body = document.getElementById('body');
    body.classList.toggle('dark-mode');
    // Save the user's preference to local storage
    var isDarkModeEnabled = body.classList.contains('dark-mode');
    localStorage.setItem('dark-mode-enabled', isDarkModeEnabled);
}

// Load the user's preferred mode from local storage
var isDarkModeEnabled = localStorage.getItem('dark-mode-enabled');
if (isDarkModeEnabled === 'true') {
  document.getElementById('body').classList.add('dark-mode');
}

//----------------- feedback page functions ------------------------------//
function submitComment() {
    var comment = document.getElementById("comment").value;
    var commentSection = document.getElementById("comment-section");
    var newComment = document.createElement("div");
    newComment.classList.add("comment");
    newComment.innerHTML = `
      <span class="comment-text">${comment}</span>
      <div class="comment-actions">
        <button onclick="editComment(this)">Edit</button>
        <button onclick="deleteComment(this)">Delete</button>
      </div>
    `;
    commentSection.insertBefore(newComment, commentSection.firstChild);
    document.getElementById("comment").value = "";
    document.getElementById("comment").focus();
    saveComments(commentSection.innerHTML);
  }

  function editComment(button) {
    var commentText = button.parentNode.parentNode.querySelector(".comment-text");
    var newText = prompt("Enter new comment text", commentText.innerText);
    if (newText !== null) {
      commentText.innerText = newText;
      saveComments(document.getElementById("comment-section").innerHTML);
    }
  }

  function deleteComment(button) {
    var comment = button.parentNode.parentNode;
    comment.parentNode.removeChild(comment);
    saveComments(document.getElementById("comment-section").innerHTML);
  }

  function saveComments(comments) {
    localStorage.setItem("userComments", comments);
  }

  function loadComments() {
    var commentSection = document.getElementById("comment-section");
    var comments = localStorage.getItem("userComments");
    if (comments) {
      commentSection.innerHTML = comments;
    }
  }
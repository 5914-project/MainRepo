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

function displayItems() {
  fetch("/searchItems", {
    method: "POST",
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
    addListItems(items)
  })
}

function sendToSpeech() {
  event.preventDefault();
  fetch("/speech", {
    method: "POST",
  }).then((response) => {
    return response.json(); // Parse response as JSON data
  }).then((items) => {
    addListItems(items)
  })
}

function clearItems() {
  fetch("/removeItems", {
    method: "POST",
  }).then(response => {
    var itemsList = document.getElementById("items");
    itemsList.innerHTML = "";
  })
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
      addListItems(items)
    })
 }
}

function takePicture() {
  fetch("/savePicture", {
    method: "POST",
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

function addListItems(items) {
  var itemsList = document.getElementById("items");
  itemsList.innerHTML = "";
  for (let item of items) { 
    var li = document.createElement("li");
    var text = document.createTextNode(item);
    li.appendChild(text);
    // Create the remove button
    const removeButton = document.createElement("button");
    removeButton.innerText = "Remove";
    removeButton.classList.add("remove-button");
    removeButton.addEventListener("click", () => {
      const itemText = text.textContent;
      fetch("/removeSingleItem", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({itemText: itemText})
      }).then((response) => {
        return response.json();
      }).then((items) => {
        addListItems(items)
      })
    });
    li.appendChild(removeButton);
    itemsList.appendChild(li); 
  } 
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
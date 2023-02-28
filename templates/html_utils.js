export function readWebpage() {
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
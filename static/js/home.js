window.addEventListener("DOMContentLoaded", function() {
    // Stream from the camera to the video player
    var video = document.getElementById('video');

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const getImage = async () => {
            video.srcObject = await navigator.mediaDevices.getUserMedia({ video: true })
            video.play();
        }
        getImage()
    }

    var message = document.getElementById('message');
    var navtext = document.getElementById('navtext');
    var boi = document.getElementById('boi');

    const happyMsg = "What a nice smile 😍🥰🌈🔥"
    const unhappyMsg = "not happy 😢"

    const refresh = async () => {
        // Draw the image on a canvas so it can be captured as base64 encoded binary data
        var canvas = document.createElement('canvas');
        canvas.width = 640;
        canvas.height = 480;

        var context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        var data = {
            'image_base64': canvas.toDataURL("image/png")
        }

        // Make the POST request and get back the result
        const getResult = async () => {
            console.log("Getting image result..")
            var result = await fetch('process_image', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: { 'Content-Type': 'application/json' }
            })

            var jsonResult = await result.json(
            console.log(jsonResult);
            )
            if (jsonResult.happy == 1) {
              message.textContent = happyMsg
              navtext.textContent = happyMsg
            } else {
              message.textContent = unhappyMsg
              navtext.textContent = ""
            }
            boi.setAttribute("src", jsonResult.boi)
        }

        // this function can be a bit slow depending on upload speed.
        await getResult()

        refresh();
    }

    refresh();

    var scroller = document.querySelector("#scroller");
    var template = document.querySelector('#post_template');
    var sentinel = document.querySelector('#sentinel');

    // Set a counter to count the items loaded
    var counter = 0;

    // Function to request new items and render to the dom
    function loadItems() {

      // Use fetch to request data and pass the counter value in the QS
      fetch(`/load?c=${counter}`).then((response) => {

        // Convert the response data to JSON
        response.json().then((data) => {

          // If empty JSON, exit the function
          if (!data.length) {

            // Replace the spinner with "No more posts"
            sentinel.innerHTML = "No more posts";
            return;
          }

          // Iterate over the items in the response
          for (var i = 0; i < data.length; i++) {

            // Clone the HTML template
            let template_clone = template.content.cloneNode(true);

            // Query & update the template content
            // template_clone.querySelector("#title").innerHTML = `${data[i][0]}`;
            template_clone.querySelector("#content").setAttribute('src', data[i][1]);

            // Append template to dom
            scroller.appendChild(template_clone);

            // Increment the counter
            counter += 1;
          }
        })
      })
    }

    // Create a new IntersectionObserver instance
    var intersectionObserver = new IntersectionObserver(entries => {

      // Uncomment below to see the entry.intersectionRatio when
      // the sentinel comes into view

      // entries.forEach(entry => {
      //   console.log(entry.intersectionRatio);
      // })

      // If intersectionRatio is 0, the sentinel is out of view
      // and we don't need to do anything. Exit the function
      if (entries[0].intersectionRatio <= 0) {
        return;
      }

      // Call the loadItems function
      loadItems();

    });

    // Instruct the IntersectionObserver to watch the sentinel
    intersectionObserver.observe(sentinel);
})
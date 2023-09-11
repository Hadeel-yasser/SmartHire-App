   /* console.log("Before DOMContentLoaded event listener");
    document.addEventListener("DOMContentLoaded", () => {
    console.log("DOMContentLoaded event fired");
      
      const dropdown = document.getElementById("job-dropdown");
      
      
      if (dropdown) {
        console.log("Dropdown element found");
        
          dropdown.addEventListener("change", () => {
          const selectedValue = dropdown.value;
          console.log("Selected value: ", selectedValue);
          const xhr = new XMLHttpRequest();
          xhr.open("POST", "/api/create_core");   
          xhr.setRequestHeader("Content-Type", "application/json");
          xhr.send(JSON.stringify({ selectedValue }));
          
          //console.log(JSON.stringify({ selectedValue }))
        });
      } else {
        console.log("Dropdown element not found");
      }
      });*/
      //console.log("Before DOMContentLoaded event listener");
      document.addEventListener("DOMContentLoaded", () => {
       // const currentHostname = window.location.hostname;
      //  const currentProtocol = window.location.protocol; // 'http:' or 'https:'
      //  const currentPort = window.location.port || (currentProtocol === 'https:' ? '443' : '80');

      //  console.log(`Hostname: ${currentHostname}`);
       // console.log(`Port: ${currentPort}`);

        const dropdown = document.getElementById("job-dropdown");

        dropdown.addEventListener("change", () => {
        const selectedValue = dropdown.value;
        
        
            // Send the selectedValue to your Python backend using an HTTP request
            fetch('/return_core_name', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ selectedValue }),
            })
            .then(response => response.json())
            .then(data => {
                // Handle the response from the Python function if needed
                console.log("Response from server:", data);
            })
            .catch(error => {
                // Handle errors, if any
                console.error("Error:", error);
            });
        });
      });
document.getElementById("login-button").addEventListener("click", function(event) {
    event.preventDefault(); // Prevent form submission
    
    // Get the entered username and password
    var username = document.getElementById("inputemail").value;
    var password = document.getElementById("inputPassword").value;
    
    // Check if the credentials are valid
    if (username === "hadeel" && password === "123") {
      window.location.href = "index.html"; // Redirect to Home.html page
    } 
       else if (username === "" || password === "") {
        swal({
          title: "Please Enter Your Credentials",
          text: "Both email and password are required",
          icon: "error",
          button: {
            text: "OK",
            className: "btn-black",
          },
          closeOnClickOutside: false,
        });}
        else {
        swal({
          title: "Invalid Credentials",
          text: "Please try again",
          icon: "error",
          button: {
            text: "OK",
            className: "btn-black",
          },
          closeOnClickOutside: false,
        });
      }
    });
  
  
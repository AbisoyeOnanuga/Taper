   // Get the input box element
   const inputBox = document.getElementById("user_input");

   // Get the button elements
   const dogButton = document.getElementById("dog");
   const loveButton = document.getElementById("love");
   const mysteryButton = document.getElementById("mystery");
   const spaceButton = document.getElementById("space");
   const dreamButton = document.getElementById("dream");

   // Add a click event listener to each button
   dogButton.addEventListener("click", function () {
     // Change the value of the input box to "dog"
     inputBox.value = "dog";
     // Generate a prompt with the word "dog"
     generatePrompt("dog");
   });

   loveButton.addEventListener("click", function () {
     // Change the value of the input box to "love"
     inputBox.value = "love";
     // Generate a prompt with the word "love"
     generatePrompt("love");
   });

   mysteryButton.addEventListener("click", function () {
     // Change the value of the input box to "mystery"
     inputBox.value = "mystery";
     // Generate a prompt with the word "mystery"
     generatePrompt("mystery");
   });

   spaceButton.addEventListener("click", function () {
     // Change the value of the input box to "space"
     inputBox.value = "space";
     // Generate a prompt with the word "space"
     generatePrompt("space");
   });

   dreamButton.addEventListener("click", function () {
     // Change the value of the input box to "dream"
     inputBox.value = "dream";
     // Generate a prompt with the word "dream"
     generatePrompt("dream");
   });
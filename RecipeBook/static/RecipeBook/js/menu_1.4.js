$(document).ready(function () {
    window.onscroll = function() {myFunction()};

    let header = document.getElementById("nav_header");
    let sticky = header.offsetTop;

    function myFunction() {
      if (window.pageYOffset > sticky) {
        header.classList.add("sticky");
      } else {
        header.classList.remove("sticky");
      }
    }
});
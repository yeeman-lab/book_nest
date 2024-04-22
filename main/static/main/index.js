document.addEventListener("DOMContentLoaded", function () {
  // -------------------------------- Scroll to top functions ------------------------------------------------
  // Get the button:
  let mybutton = document.getElementById("myBtn");

  // When the user scrolls down 20px from the top of the document, show the button
  window.onscroll = function () {
    scrollFunction();
  };

  function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      mybutton.style.display = "block";
    } else {
      mybutton.style.display = "none";
    }
  }
  // When the user clicks on the button, scroll to the top of the document
  mybutton.addEventListener("click", topFunction);

  // When the user clicks on the button, scroll to the top of the document
  function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  }
  // -------------------------------- For Carousel's functions ------------------------------------------------

  // example carousel
  var multipleCardCarousel = document.querySelector(".carousel");
  if (multipleCardCarousel) {
    if (window.matchMedia("(min-width: 768px)").matches) {
      var carousel = new bootstrap.Carousel(multipleCardCarousel, {
        interval: false,
      });
      var carouselWidth = $(".carousel-inner")[0].scrollWidth;
      var cardWidth = $(".carousel-item").width();
      var scrollPosition = 0;
      $(".carousel .carousel-control-next").on("click", function () {
        if (scrollPosition < carouselWidth - cardWidth * 4) {
          scrollPosition += cardWidth;
          $(".carousel .carousel-inner").animate({ scrollLeft: scrollPosition }, 600);
        }
      });
      $(".carousel .carousel-control-prev").on("click", function () {
        if (scrollPosition > 0) {
          scrollPosition -= cardWidth;
          $(".carousel .carousel-inner").animate({ scrollLeft: scrollPosition }, 600);
        }
      });
    } else {
      $(multipleCardCarousel).addClass("slide");
    }
  }
});

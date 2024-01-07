"use strict";

$(document).ready(function () {
  $("#currentYear").text(new Date().getFullYear());
  var $toggleBtn = $("#toggle");
  var $collapseMenu = $("#collapseMenu");

  function handleClick() {
    if ($(window).innerWidth() <= 1024) {
      if ($collapseMenu.css("display") === "block") {
        $collapseMenu.hide();
        $collapseMenu.css({
          position: "",
          "z-index": "",
          top: "",
          left: "",
          width: "",
          "background-color": "",
        });
      } else {
        $collapseMenu.show().css({
          position: "absolute",
          "z-index": "999",
          top: "70px",
          left: "0",
          width: "100%",
          "background-color": "#fff",
        });
      }
    }
  }

  $(window).resize(function () {
    if ($(window).innerWidth() > 1024) {
      $collapseMenu.hide().css({
        position: "",
        "z-index": "",
        top: "",
        left: "",
        width: "",
        "background-color": "",
      });
    }
  });

  $toggleBtn.click(handleClick);
});

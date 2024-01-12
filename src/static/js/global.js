"use strict";

$(document).ready(function () {
  //navebar
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
  function formatRp(angka, prefix) {
    var number_string = angka.replace(/[^,\d]/g, "").toString(),
      split = number_string.split(","),
      sisa = split[0].length % 3,
      rupiah = split[0].substr(0, sisa),
      ribuan = split[0].substr(sisa).match(/\d{3}/g),
      separator = "";

    if (ribuan) {
      separator = sisa ? "." : "";
      rupiah += separator + ribuan.join(".");
    }

    rupiah = split[1] != undefined ? rupiah + "," + split[1] : rupiah;
    return prefix == undefined ? rupiah : rupiah ? "Rp. " + rupiah : "";
  }

  $("#dengan-rupiah").keyup(function () {
    $(this).val(formatRp($(this).val(), "Rp. "));
  });

  //Buat Navebar aktif
  var url = window.location.href;
  var page = url.substr(url.lastIndexOf("/") + 1);
  if (page === "") {
    page = "home";
  }

  $("li").each(function () {
    if ($(this).text().trim().toLowerCase() === page) {
      $(this).addClass("border-emerald-500 text-emerald-500");
    }
  });
});

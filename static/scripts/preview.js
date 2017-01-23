

var url = "http://localhost:3000";

//Filter laden
$.getJSON(url+"/filters",{},function(data){
  var counter = 0;

  $("#filters").append("<li> <div class = \"menu-space\" >");
  $.each(data, function(key, value) {
    if(counter%3 == 0 && counter != 0){
        $("#filters").append("</div></li>");
        $("#filters").append("<li> <div class = \"menu-space\" >");
    }

    $("#filters").append(""+
      "<div class = \"menu-item\" onclick=\"applyFilter(\'"+value[0]+":"+value[1]+"\')\">"+
      "        <div class = \"menu-image\">"+
              "<img src = \"img/preview/filters/"+value[3]+"\" class = \"preview-image\">"+
            "</div>"+
          "<div class = \"menu-description\">"+value[2]+"</div>"+
      "</div>");




   console.log(key+ counter + value[3]);
   counter = counter + 1;
  });
  for(var i = 0; i < 2-(counter-1)%3; i++){
    $("#filters").append("<div class = \"menu-item space\"></div>");

  }

  $("#filters").append(" </div></li> <li><a>Filter</a></li>");



});

//Masken Laden

$.getJSON(url+"/masks",{},function(data){
  var counter = 0;

  $("#masks").append("<li> <div class = \"menu-space\" >");
  $.each(data, function(key, value) {
    if(counter%3 == 0 && counter != 0){
        $("#masks").append("</div></li>");
        $("#masks").append("<li> <div class = \"menu-space\" >");
    }

    $("#masks").append(""+
      "<div class = \"menu-item\" onclick=\"applyMask(\'"+value[0]+":"+value[1]+"\')\">>"+
      "        <div class = \"menu-image\">"+
              "<img src = \"img/preview/masks/"+value[3]+"\" class = \"preview-image\">"+
            "</div>"+
          "<div class = \"menu-description\">"+value[2]+"</div>"+
      "</div>");




   console.log(key+ counter + value[3]);
   counter = counter + 1;
  });
  for(var i = 0; i < 2-(counter-1)%3; i++){
    $("#masks").append("<div class = \"menu-item space\"></div>");

  }

  $("#masks").append(" </div></li> <li><a>Masken</a></li>");



});

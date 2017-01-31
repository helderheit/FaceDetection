

function applyFilter(filterName){
    var id = "#"+filterName.replace(':','-');
    $.get(url+"/stream/12345/filteractive",function(data){
      var lastFilter = data;
      console.log(lastFilter);

      $.post(url +"/stream/12345/filter", { filter: filterName },function( data ) {

          $(id).addClass("menu-item-selected");
          $("#"+lastFilter).removeClass("menu-item-selected");
          console.log(data);
      });
    });

}



function applyMask(maskName){
  var id = "#"+maskName.replace(':','-');
  $.get(url+"/stream/12345/maskactive",function(data){
    var lastMask = data;
    console.log(lastMask);

    $.post(url +"/stream/12345/mask", { mask: maskName },function( data ) {
      $(id).addClass("menu-item-selected");
      $("#"+lastMask).removeClass("menu-item-selected");
      console.log(data);
    });
  });
}


function changeCam(camId){
  console.log("changecam");
  $.post(url +"/stream/12345/changecam", { id: camId },function( data ) {
  console.log(data);
  });

}

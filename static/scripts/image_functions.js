

var url = "http://localhost:3000";

function applyFilter(filterName){
  $.post(url +"/filter", { filter: filterName },function( data ) {
  console.log(data)
  });
}



function applyMask(maskName){
  $.post(url +"/mask", { mask: maskName },function( data ) {
  console.log(data)
  });
}

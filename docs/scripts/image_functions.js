


function applyFilter(filterName){
  $.post(url +"/12345/filter", { filter: filterName },function( data ) {
  console.log(data)
  });
}



function applyMask(maskName){
  $.post(url +"/12345/mask", { mask: maskName },function( data ) {
  console.log(data)
  });
}

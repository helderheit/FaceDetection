function downloadImage() {
  console.log('download')
  var link = document.createElement("a");
  link.download = 'download';
  link.href = url+"/stream/12345/download";
  link.target = "blank";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  delete link;
}

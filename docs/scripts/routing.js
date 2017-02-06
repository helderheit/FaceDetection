var url = "http://localhost:3000";
var streamer = false;

if(!window.location.href.includes('localhost')){
  console.log(window.location.href);
  streamer = true;
}

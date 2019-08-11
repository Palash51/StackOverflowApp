function clickHandler(e) {
    // console.log(window.location.href);
    localStorage.setItem('token', "4202a4700931c79a244ce4fc23c661798f22ba66");
    var current_url;
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        console.log(tabs[0].url);
        current_url = tabs[0].url

        check_current_url = validate_url(current_url);
        if (check_current_url)
          {
            postData(current_url)
          }
        else{
          alert("Please mark only stackoverflow")
        }
      });
    
    // alert(localStorage.getItem('current_url'));
    // window.close(); // Note: 
}
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('click-me').addEventListener('click', clickHandler);
});



function validate_url(current_url) {

  var matches = current_url.match(/(\d+)/); 
              
  if (matches) { 
      var intValue = parseInt(current_url.match(/[0-9]+/)[0], 10); 
      // alert(typeof(intValue))
      var question_id = intValue.toString().length
      if (question_id > 4) {
        return true
      }
  }
  return false 
}


function postData(current_url) {
  var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:8000/v1/marked");
    var token = localStorage.getItem('token');
    xhr.setRequestHeader('Authorization', 'Token '  + token);
    xhr.setRequestHeader('Content-Type', 'application/json');
    // var current_url = window.location.href;
    // console.log(current_url);
    body = {
        "url" : current_url,
        "marked" : true
    }
    // var token = "2edea0cda47b8fa115e6ca479a3cec1932c0175c"
    // xhr.setRequestHeader('Authorization', '2edea0cda47b8fa115e6ca479a3cec1932c0175c');
    
    xhr.send(JSON.stringify(body));
    alert("You have marked url!!")
    window.close();
}







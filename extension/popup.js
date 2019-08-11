function clickHandler(e) {
    // console.log(window.location.href);
    localStorage.setItem('token', "4202a4700931c79a244ce4fc23c661798f22ba66");
    var test;
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        console.log(tabs[0].url);
        test = tabs[0].url
        postData(test)
      });
    
    // alert(localStorage.getItem('test'));
    // window.close(); // Note: 
}
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('click-me').addEventListener('click', clickHandler);
});




function postData(test) {
  var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:8000/v1/marked");
    var token = localStorage.getItem('token');
    xhr.setRequestHeader('Authorization', 'Token '  + token);
    xhr.setRequestHeader('Content-Type', 'application/json');
    // var current_url = window.location.href;
    // console.log(test);
    body = {
        "url" : test,
        "marked" : true
    }
    // var token = "2edea0cda47b8fa115e6ca479a3cec1932c0175c"
    // xhr.setRequestHeader('Authorization', '2edea0cda47b8fa115e6ca479a3cec1932c0175c');
    xhr.send(JSON.stringify(body));
    alert(xhr)
    window.close();
}







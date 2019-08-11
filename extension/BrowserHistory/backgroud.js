

// chrome.extension.onConnect.addListener(function(port) {
//       console.log("Connected .....");

//       $.ajax({

//         url: "localhost:8000/v1/search?search_query=python&sort=votes",
//         type: 'GET',
//         // Fetch the stored token from localStorage and set in the header localStorage.getItem('token')
//         headers: {
//             "Authorization": 'Token ' + "4202a4700931c79a244ce4fc23c661798f22ba61"
//         },
//         contentType: 'application/json',

//       });




//       port.onMessage.addListener(function(msg) {
//            console.log("message recieved" + msg);
//            port.postMessage("Hi Popup.js");
//       });
//  })
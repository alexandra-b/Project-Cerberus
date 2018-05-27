function putEverythinginArrays(dbRefObject,callback){
    dbRefObject.on('value', snapshot =>{
    snapshot.forEach(childSnapshot => {
      arrayOfDates.push(childSnapshot.key); //********************
      console.log(childSnapshot.key); //prints date
      document.getElementById("events").innerHTML += childSnapshot.key;
      childSnapshot.forEach(anotherChildSnapShot =>{
        arrayOfHours.push(anotherChildSnapShot.key); //**********************
        document.getElementById("events").innerHTML += "<li>";
        document.getElementById("events").innerHTML += anotherChildSnapShot.key;
        document.getElementById("events").innerHTML += "</li>";
        console.log(anotherChildSnapShot.key); //this is the hour of the event
        var ok=0;
        anotherChildSnapShot.forEach(lastChildSnapshot =>{
          console.log(lastChildSnapshot.key); //motion
          console.log(lastChildSnapshot.val()); //string of where motion was detected
          document.getElementById("events").innerHTML += " ";
          document.getElementById("events").innerHTML += lastChildSnapshot.val();
          arrayOfMotionsDetected.push(lastChildSnapshot.val()); //**********************
      });
      });
    })
  });
  callback(arrayOfDates,arrayOfHours,arrayOfMotionsDetected);
}
function printFunctions(arrayDates,arrayHours,arrayMotions){
  console.log("DATES:");
  console.log(arrayDates.length);
  for(var i=0;i<arrayDates.length;i++){
    console.log(arrayOfDates[i]);
  }
  console.log("HOURS:");
  console.log(arrayHours.length);
  for(var i=0;i<arrayHours.length;i++){
    console.log(arrayOfHours[i]);
  }
  console.log("MOTIONS:");
  console.log(arrayMotions.length);
  for(var i=0;i<arrayMotions.length;i++){
    console.log(arrayMotions[i]);
  }
}
// Initialize Firebase
var config = {
  apiKey: "AIzaSyCoAPkN2TzXPzLAJf5ev7D1_50pJaKUqQA",
  authDomain: "guardian-dbd05.firebaseapp.com",
  databaseURL: "https://guardian-dbd05.firebaseio.com",
  projectId: "guardian-dbd05",
  storageBucket: "guardian-dbd05.appspot.com",
  messagingSenderId: "769331595214"
};
firebase.initializeApp(config);
//create references
const dbRefObject = firebase.database().ref().child('events');
var myevents = [];
var arrayOfDates = [];
var arrayOfHours = [];
var arrayOfMotionsDetected = [];
putEverythinginArrays(dbRefObject,printFunctions);
/*
for(var i=0;i<events.length;i++){
  document.getElementById("events").children[0].innerHTML += "<li>"+events[i]+"</li>";
}
*/
//sync object changes
//  dbRefObject.on('value',snap => console.log(snap.val()));
//firebase.database().ref("/armed").set("hellobitches");

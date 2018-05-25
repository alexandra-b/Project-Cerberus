const Alexa = require("alexa-sdk")
const firebase = require("https://www.gstatic.com/firebasejs/3.3.0/firebase.js")

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

const handlers = {
	"Unhandled": function() {
		//unhandled intent:
		this.emit(":ask", "Welcome. Start system by saying 'arm', or stop system by saying 'disarm'.")
	},
	"Arm": function() {
		/*firebase.put("/armed", true).then(() => {
			this.emit(":tell", "Guardian has been activated.")
		})*/
		this.emit(":tell", "Guardian has been activated.")
		//set armed to true
	  firebase.database().ref("/armed").set("true");
	},
	"Disarm": function() {
		//set armed to false
		/*firebase.put("/armed", false).then(() =>{
			this.emit(":tell", "Guardian has been deactivated.")
		})*/
		this.emit(":tell", "Guardian has been deactivated.")
		 firebase.database().ref("/armed").set("false");
	},
	"SessionEndedRequest": function() {
		// exit the function if the user tries at an unexpected time
		this.emit()
	}
}

//lambda config
exports.handler = function(event, context, callback) {
	const alexa = Alexa.handler(event, context)
	alexa.registerHandlers(handlers)	// connect handler functions
	alexa.execute()										// execute function
}

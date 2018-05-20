const Alexa = require("alexa-sdk")
const firebase = require("./firebase.js")

firebase.host = "guardian-dbd05.firebaseio.com "

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
		firebase.patch("/armed", true)
	},
	"Disarm": function() {
		//set armed to false
		/*firebase.put("/armed", false).then(() =>{
			this.emit(":tell", "Guardian has been deactivated.")
		})*/
		this.emit(":tell", "Guardian has been deactivated.")
		firebase.patch("/armed", false)
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

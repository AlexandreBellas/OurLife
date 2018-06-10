var db;
var ID_name = document.querySelector("#pid");

String.prototype.splice = function(idx, rem, str) {
    return this.slice(0, idx) + str + this.slice(idx + Math.abs(rem));
};

function getPacient(id){
	var first = true;
	db = firebase.database();

	var leadsRef = db.ref(id);
	id = id.splice(3, 0, '.');
	id = id.splice(7, 0, '.');
	id = id.splice(11, 0, '-');

	ID_name.textContent = id;

	leadsRef.on('value', function(snapshot) {
		snapshot.forEach(function(childSnapshot) {
		  if(!first) return;
		  var childData = childSnapshot.val();
		  childData = JSON.parse(childData);
		//console.log(childData);
		  first = false;
		});
	});
}

function setup() {
  	var config = {
	    apiKey: "AIzaSyC5qDlckVniuFbbmwgPRki-JJWJWifx9-I",
	    authDomain: "babysanca-4f129.firebaseapp.com",
	    databaseURL: "https://babysanca-4f129.firebaseio.com",
	    projectId: "babysanca-4f129",
	    storageBucket: "babysanca-4f129.appspot.com",
	    messagingSenderId: "8286925553"
	  };

	firebase.initializeApp(config);
	getPacient('45038205836');
	barGraphics();
	pieGraphics("#_pie");
	pieGraphics("#_pie2");

	document.querySelector('.progress').style.visibility = "hidden";
}

window.onload = setup;
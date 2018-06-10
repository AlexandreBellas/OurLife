var db;

var heartbeat = document.querySelector("#heartbeat");
var pas = document.querySelector("#pas");
var pad = document.querySelector("#pad");
var temperatura = document.querySelector("#temperatura");
var CPFinput = document.querySelector("#cpf");

var protocol = document.querySelector("#protocol");

String.prototype.splice = function(idx, rem, str) {
    return this.slice(0, idx) + str + this.slice(idx + Math.abs(rem));
};

function getPacient(id){
	var first = true;
	db = firebase.database();

	var leadsRef = db.ref(id);
	
	leadsRef.on('value', function(snapshot) {
		snapshot.forEach(function(childSnapshot) {
		  if(!first) return;
		  var childData = childSnapshot.val();
		  childData = JSON.parse(childData);
		  console.log(childData);

		  heartbeat.innerHTML = "<i class='material-icons'>favorite</i><span> " + childData.batimentos + "</span>";
		  heartbeat.innerHTML += "<span>" + " - Ok" + "</span>";
		  heartbeat.classList.remove("gray");
		  heartbeat.classList.add("green");

		  pas.innerHTML = "<i class='material-icons'>PAD ⚕️</i><span> " + childData.PAS + "</span>";
		  pas.innerHTML += "<span>" + " - Atento" + "</span>";
		  pas.classList.remove("gray");
		  pas.classList.add("orange");
		  
		  pad.innerHTML = "<i class='material-icons'>🌡️</i><span> " + childData.PAD + "</span>";
		  pad.innerHTML += "<span>" + " - Ok" + "</span>";
		  pad.classList.remove("gray");
		  pad.classList.add("green");

		  temperatura.innerHTML = "<i class='material-icons'>PAS ⚕️</i><span> " + childData.temperatura  + "</span>";
		  temperatura.innerHTML += "<span>" + " - Crítico" + "</span>";
		  temperatura.classList.remove("gray");
		  temperatura.classList.add("red");

		  var n;

		  // Simulação de um resultado
		  if(childData.temperatura > 37) {
			n = 12;
		  } else {
		  	n = 24;
		  }

		  protocol.innerHTML = `
		  	<span class="card-title">
	          	<i class="material-icons">check</i>
	          	Protocolo #` + n + `
	          </span>
	          <p>
	          	Lorem ipsum dolor sit amet, consectetur adipiscing elit. In elementum felis vel vehicula lobortis. Nam lacinia nisi quis orci blandit aliquet. Fusce feugiat nec turpis id placerat. Ut tristique tellus vitae nisi pellentesque, a aliquam metus bibendum. Donec luctus lectus lorem, quis tincidunt tortor lobortis eu. Curabitur porttitor diam vitae ullamcorper rutrum. Nullam sit amet nisi at odio suscipit laoreet ac ut urna. Curabitur lectus ex, aliquam non tristique eu, mollis sit amet diam. Duis id imperdiet lorem. Etiam vitae dui dapibus, pulvinar ligula vitae, fermentum leo. Vestibulum vel ipsum elementum, mollis purus et, molestie justo. Suspendisse tincidunt, erat eget tincidunt condimentum, nisi velit semper neque, a elementum orci eros quis dolor. Sed vehicula velit sit amet velit ultrices, vel ultrices nunc maximus. In leo nulla, sollicitudin at massa sed, volutpat commodo diam. Nulla facilisi. Duis sed tortor vel felis commodo molestie sed ac augue.
	          </p>
	        `;
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
	CPFinput.value = '45038205836';
	readInput();

	document.querySelector('.progress').style.visibility = "hidden";
}

function readInput(){
	getPacient(CPFinput.value);
};

$(document).ready(function(){$('.collapsible').collapsible();});

window.onload = setup;
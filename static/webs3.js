function SendForm(InputId, buttonName, divIdToUpdate){
  var formGroup = $('#'+InputId)
  console.log('Input Id to check for inputs is: '+ InputId)
  //var fData = new FormData(formGroup[0].id)
  var fData = new FormData(formGroup[0])
  var fInput = formGroup.find(':input')
  var action = formGroup[0].attributes.action.value
  var session;
  for (var i = 0; i < fInput.length; i++) {
    if (!(fInput[i].type === "submit")){
    fData.append(fInput[i].name, fInput[i].value);
    console.log('name: ' + fInput[i].value + ' val: '+ fInput[i].name);
    }
    if (fInput[i].name === ""+buttonName) {
      console.log("Button used: ")
      console.log(fInput[i])
      fData.append(fInput[i].value, fInput[i].name);
      }
  }
var request = new XMLHttpRequest();

request.open("POST", action);

request.onreadystatechange = function(){
   if (request.readyState === 4){
       if (request.state === 200){
           console.log("received the response - " + request);
       } else {
             if (divIdToUpdate === 'body'){
               $(divIdToUpdate)[0].innerHTML = request.response;
             }else{
               console.log("request resp: "+request);
               $('#' +divIdToUpdate)[0].outerHTML = request.response;
             }
       }
    } else {
        console.log("waiting for the response to come");
   }
}

for (var p of fData){
    console.log(p)
}

request.send(fData);
}


function removeElement(elementId) {
    // Removes an element from the document
    var element = document.getElementById(elementId);
    element.parentNode.removeChild(element);
}


function showHideCh(div) {
	var chObjs = $('#'+div)[0].children
	for (var i = 0; i < chObjs.length; i++) {
		if (!(chObjs[i].style.visibility === "collapse")) {
			chObjs[i].style.visibility="collapse"
		}else {
			chObjs[i].style.visibility=""
		}
	}
}



function SendFormAndDel(InputId, buttonName, divIdToUpdate){
  var formGroup = $('#'+InputId)
  console.log('Input Id to check for inputs is: '+ InputId)
  //var fData = new FormData(formGroup[0].id)
  var fData = new FormData(formGroup[0])
  var fInput = formGroup.find(':input')
  var session;
  for (var i = 0; i < fInput.length; i++) {
    if (!(fInput[i].type === "submit")){
    fData.append(fInput[i].name, fInput[i].value);
    console.log('name: ' + fInput[i].name + ' val: '+ fInput[i].value);
    }
    if (fInput[i].name === ""+buttonName) {
      console.log("Button used: ")
      console.log(fInput[i])
      fData.append(fInput[i].name, fInput[i].value);
      var session = fInput[i].attributes.target.value;
      }
  }
var request = new XMLHttpRequest();
console.log("Session Before Post to FormMgr: "+ session)
//var session = session.attributes.target.value;
var fgAction = formGroup[0].attributes.action.value;
console.log('FormGroup Action: ' + fgAction);
request.open("POST", '/FormMgr/'+session+' '+ fgAction +' '+divIdToUpdate);

request.onreadystatechange = function(){
   if (request.readyState === 4){
       if (request.state === 200){
           console.log("received the response - " + request);
       } else {
             if (divIdToUpdate === 'body'){
               $(divIdToUpdate)[0].innerHTML = request.response;
             }else{
               console.log("request resp: "+request);
               $('#' +divIdToUpdate)[0].innerHTML = request.response;
             }
       }
    } else {
        console.log("waiting for the response to come");
   }
}

for (var p of fData){
    console.log(p)
}


request.send(fData);

function removeElement(elementId) {
    // Removes an element from the document
    var element = document.getElementById(elementId);
    element.parentNode.removeChild(element);
}
removeElement(InputId);
}



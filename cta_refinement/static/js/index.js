//Functions to validate CTA form using regex prior to submission to server

function validateCta(cta){

   let ctaRefines = new RegExp('.* refines\\? .*;');
   let ctaPattern = new RegExp('Cta [A-Za-z]\\w+ = {[\\s\\S]{1,}?};',"g");
   let enteredCtas = editor.getValue();
   
   var matchingArray = [];
   let matched;
   var refinesMatch = ctaRefines.exec(cta);

   while(matched = ctaPattern.exec(cta)){
       matchingArray.push(matched);
   }

   if(checkTags(enteredCtas) != 0){
      document.getElementById("reqCloseTag").hidden = false;
   }
   else if (matchingArray.length < 2){
      document.getElementById("malFormed").hidden = false;
   }
   else if(refinesMatch === null){
      document.getElementById("reqRefine").hidden = false;
   }
   else if(matchingArray.length>1){
      return true;
   }
}

//Check opening and closing tags {()}

function checkTags(enteredCtas){
var tags = 0;
for(i=0; i < enteredCtas.length; i++){
   if (enteredCtas[i] == "{"|enteredCtas[i] == "("){
         tags++;
   }
   else if (enteredCtas[i] == "}"|enteredCtas[i] == ")"){
         tags--;
   }
}
return tags;
}

//Grab Ctas entered and check validity if valid submit to server

function enterText(){
   var text = editor.getValue();
   var script = document.getElementById("script");
   script.value = text;
   document.getElementById("reqCloseTag").hidden = true;
   document.getElementById("malFormed").hidden = true;
   document.getElementById("reqRefine").hidden = true;

   if(validateCta(script.value)){
      document.getElementById("scriptBtn").click();
   }
}

//Functions for uploading external file and placing in editor window for submission

var scriptFile = document.getElementById('scriptFile');
scriptFile.addEventListener('change', readSingleFile, false);

function readSingleFile(e) {
   var file = e.target.files[0];
   if (!file) {
      return;
   }
   var reader = new FileReader();
   reader.onload = function(e) {
      var contents = e.target.result;
   displayContents(contents);
   };
   reader.readAsText(file);
}

function displayContents(contents) {
   var element = document.getElementById('file-content');
   element.innerText = contents;
   initEditor(contents);
}

function initEditor(text) {
   var editor = ace.edit("editor");
   editor.setTheme("ace/theme/chrome");
   editor.set
   editor.session.setMode("ace/mode/cta");
   editor.setShowPrintMargin(true);
   editor.setValue(text);
   document.getElementById('editor').style.fontSize='20px';
   document.getElementById('editor').style.width='100%';
}

//Function to download CTA window output to text file

function download(filename, text) {
   var element = document.createElement('a');
   element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
   element.setAttribute('download', filename);

   element.style.display = 'none';
   document.body.appendChild(element);

   element.click();

   document.body.removeChild(element);
}

//Function to share script - gets editor places in secret form and submits to server

function share(){
   document.getElementById("script2").value = editor.getValue();
   document.getElementById("hiddenForm2").submit();
 }
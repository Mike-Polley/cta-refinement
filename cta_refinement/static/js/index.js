//Functions to validate CTA form using regex prior to submission to server

function validateCta(cta){

   let ctaRefines = new RegExp('.* refines\\? .*;');
   let ctaPattern = new RegExp('Cta [A-Za-z]\\w+ = {[\\s\\S]*};');
   var refinesMatch = ctaRefines.exec(cta);
   var patternMatch = ctaPattern.exec(cta);

   if (patternMatch === null){
      document.getElementById("malFormed").hidden = false;
   }
   else if(refinesMatch === null){
      document.getElementById("reqRefine").hidden = false;
   }
   else if(patternMatch.length>=1){
   return true;
   }
}


function enterText(){
   var text = editor.getValue();
   var script = document.getElementById("script");
   script.value = text;
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


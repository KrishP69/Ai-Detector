let fileInput = document.getElementById("imageUpload");
let preview = document.getElementById("preview");
let dropArea = document.getElementById("dropArea");

fileInput.addEventListener("change", showImage);

dropArea.addEventListener("dragover", function(e){
e.preventDefault();
});

dropArea.addEventListener("drop", function(e){
e.preventDefault();

let file = e.dataTransfer.files[0];
fileInput.files = e.dataTransfer.files;

showImage();
});

function showImage(){

let file = fileInput.files[0];

if(!file) return;

preview.src = URL.createObjectURL(file);
preview.style.display = "block";

}

function removeImage(){

fileInput.value = "";
preview.src = "";
preview.style.display = "none";

document.getElementById("result").innerText = "";

}

async function detectAI(){

if(fileInput.files.length === 0){
alert("Upload an image first");
return;
}

let result = document.getElementById("result");

result.innerText = "Analyzing image...";

try{

let formData = new FormData();
formData.append("image", fileInput.files[0]);

let response = await fetch("https://ai-detector-api-q80d.onrender.com/detect",{
method:"POST",
body:formData
});

let data = await response.json();

result.innerText =
data.result + " (" + data.confidence + "% confidence)";

}catch(error){

result.innerText = "Backend server not running";

}

}
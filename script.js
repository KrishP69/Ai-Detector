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
document.getElementById("confidenceBar").style.display = "none";

}

async function detectAI(){

if(fileInput.files.length === 0){
alert("Upload an image first");
return;
}

let result = document.getElementById("result");
let loading = document.getElementById("loading");
let bar = document.getElementById("confidenceBar");
let fill = document.getElementById("confidenceFill");

result.innerText = "";
loading.style.display = "block";

try{

let formData = new FormData();
formData.append("image", fileInput.files[0]);

let response = await fetch(
"https://ai-detector-api-q80d.onrender.com/detect",
{
method:"POST",
body:formData
});

let data = await response.json();

loading.style.display = "none";

result.innerText =
data.result + " (" + data.confidence + "% confidence)";

bar.style.display = "block";
fill.style.width = data.confidence + "%";

}catch(error){

loading.style.display = "none";
result.innerText = "Error connecting to server";

}

}
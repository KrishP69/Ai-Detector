let fileInput = document.getElementById("imageUpload");
let preview = document.getElementById("preview");
let dropArea = document.getElementById("dropArea");
let result = document.getElementById("result");

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

    result.innerText = "";

    document.getElementById("patternBar").style.width = "0%";
    document.getElementById("lightingBar").style.width = "0%";
    document.getElementById("textureBar").style.width = "0%";

    document.getElementById("finalProbability").innerText = "";
}


async function detectAI(){

    if(fileInput.files.length === 0){
        alert("Upload an image first");
        return;
    }

    result.innerText = "Analyzing image...";

    try{

        let formData = new FormData();
        formData.append("image", fileInput.files[0]);

        let response = await fetch("https://ai-detector-api-q80d.onrender.com/detect",{
            method:"POST",
            body:formData
        });

        let data = await response.json();

        // main result
        result.innerText =
        data.result + " (" + data.confidence + "% confidence)";


        // progress bars
        document.getElementById("patternBar").style.width =
        data.pattern + "%";

        document.getElementById("lightingBar").style.width =
        data.lighting + "%";

        document.getElementById("textureBar").style.width =
        data.texture + "%";


        // final probability (from backend only)
        document.getElementById("finalProbability").innerText =
        "Final AI Probability: " + data.confidence + "%";


        // scan history
        addToHistory(data.result, data.confidence);


    }catch(error){

        result.innerText = "Backend server not running";

    }

}


function addToHistory(label, confidence){

    let history = document.getElementById("history");

    let item = document.createElement("div");
    item.className = "historyItem";

    let img = document.createElement("img");
    img.src = preview.src;

    let text = document.createElement("div");
    text.innerText = label + " (" + confidence + "%)";

    let time = document.createElement("div");
    time.className = "time";
    time.innerText = new Date().toLocaleTimeString();

    item.appendChild(img);

    let container = document.createElement("div");
    container.appendChild(text);
    container.appendChild(time);

    item.appendChild(container);

    history.prepend(item);
}
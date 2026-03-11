let fileInput = document.getElementById("imageUpload")
let preview = document.getElementById("preview")
let forensic = document.getElementById("forensicImage")
let dropArea = document.getElementById("dropArea")

fileInput.addEventListener("change", showImage)

dropArea.addEventListener("dragover", e=>{
e.preventDefault()
})

dropArea.addEventListener("drop", e=>{
e.preventDefault()
fileInput.files = e.dataTransfer.files
showImage()
})

function showImage(){

let file = fileInput.files[0]

if(!file) return

preview.src = URL.createObjectURL(file)
preview.style.display = "block"

forensic.style.display = "none"

}

function removeImage(){

fileInput.value=""
preview.src=""
preview.style.display="none"

forensic.src=""
forensic.style.display="none"

document.getElementById("result").innerText=""
document.getElementById("confidenceBar").style.display="none"
document.getElementById("analysisSection").style.display="none"

}

async function detectAI(){

if(fileInput.files.length===0){
alert("Upload image first")
return
}

let result=document.getElementById("result")
let loading=document.getElementById("loading")
let bar=document.getElementById("confidenceBar")
let fill=document.getElementById("confidenceFill")

loading.style.display="block"
result.innerText=""

try{

let formData=new FormData()
formData.append("image",fileInput.files[0])

let response=await fetch(
"https://ai-detector-api-q80d.onrender.com/detect",
{
method:"POST",
body:formData
})

let data=await response.json()

loading.style.display="none"

result.innerText=data.result+" ("+data.confidence+"% confidence)"

bar.style.display="block"
fill.style.width=data.confidence+"%"

forensic.src =
"https://ai-detector-api-q80d.onrender.com/forensic?"+Date.now()

forensic.style.display = "block"

let aiScore=data.confidence

let pattern=Math.min(100, aiScore+10)
let lighting=Math.max(5, aiScore*0.6)
let texture=Math.max(3, aiScore*0.4)

document.getElementById("analysisSection").style.display="block"

document.getElementById("patternBar").style.width = pattern + "%"
document.getElementById("lightingBar").style.width = lighting + "%"
document.getElementById("textureBar").style.width = texture + "%"

document.getElementById("finalScore").innerText =
"Final AI Probability: " + aiScore + "%"

saveHistory(data.result,data.confidence)

}catch(error){

loading.style.display="none"
result.innerText="Server error"

}

}

function saveHistory(result,confidence){

let historyList=document.getElementById("historyList")

let imageURL=preview.src

let time=new Date().toLocaleTimeString()

let item=document.createElement("div")

item.className="history-item"

item.innerHTML=`
<img src="${imageURL}">
<div class="history-info">
<div>${result} (${confidence}%)</div>
<small>${time}</small>
</div>
`

historyList.prepend(item)

}

/* Theme toggle */

let toggle=document.getElementById("themeToggle")

toggle.onclick=function(){

document.body.classList.toggle("light")

if(document.body.classList.contains("light")){
toggle.innerText="☀️"
}else{
toggle.innerText="🌙"
}

}


/* Zoom viewer */

let zoomModal=document.getElementById("zoomModal")
let zoomImage=document.getElementById("zoomImage")
let closeZoom=document.getElementById("closeZoom")

let scale=1
let posX=0
let posY=0
let dragging=false
let startX,startY

forensic.onclick=function(){

zoomModal.style.display="flex"
zoomImage.src=forensic.src

scale=1
posX=0
posY=0

zoomImage.style.transform=`scale(${scale}) translate(${posX}px,${posY}px)`

}

closeZoom.onclick=function(){
zoomModal.style.display="none"
}

zoomImage.addEventListener("wheel",function(e){

e.preventDefault()

scale+=e.deltaY*-0.001

scale=Math.min(Math.max(.5,scale),5)

zoomImage.style.transform=`scale(${scale}) translate(${posX}px,${posY}px)`

})

zoomImage.addEventListener("mousedown",function(e){

dragging=true

startX=e.clientX-posX
startY=e.clientY-posY

zoomImage.style.cursor="grabbing"

})

window.addEventListener("mouseup",()=>{

dragging=false
zoomImage.style.cursor="grab"

})

window.addEventListener("mousemove",function(e){

if(!dragging) return

posX=e.clientX-startX
posY=e.clientY-startY

zoomImage.style.transform=`scale(${scale}) translate(${posX}px,${posY}px)`

})
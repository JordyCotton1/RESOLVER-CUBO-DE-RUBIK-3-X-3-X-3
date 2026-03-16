const video=document.getElementById("video")
const canvas=document.getElementById("overlay")
const ctx=canvas.getContext("2d")

navigator.mediaDevices.getUserMedia({video:true})

.then(stream=>{

video.srcObject=stream

video.onloadedmetadata=()=>{

video.play()

requestAnimationFrame(detectar)

}

})

.catch(err=>{

alert("No se pudo abrir la cámara")

console.log(err)

})

function detectar(){

ctx.drawImage(video,0,0,640,480)

let size=80
let startX=200
let startY=120

for(let y=0;y<3;y++){

for(let x=0;x<3;x++){

let px=startX+x*size
let py=startY+y*size

ctx.strokeStyle="white"
ctx.lineWidth=3
ctx.strokeRect(px,py,size,size)

}

}

requestAnimationFrame(detectar)

}

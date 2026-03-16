const instrucciones=[
"Escanear cara BLANCA",
"Girar DERECHA → cara NARANJA",
"Girar ABAJO → cara VERDE",
"Girar DERECHA → cara AMARILLA",
"Girar DERECHA → cara AZUL",
"Girar ABAJO → cara ROJA"
]

let caraActual=0

const video=document.getElementById("video")
const canvas=document.getElementById("overlay")
const ctx=canvas.getContext("2d")

document.getElementById("instruccion").innerText=instrucciones[caraActual]

navigator.mediaDevices.getUserMedia({video:true})
.then(stream=>{
video.srcObject=stream
requestAnimationFrame(detectar)
})

function detectar(){

ctx.drawImage(video,0,0,640,480)

let size=60
let startX=260
let startY=150

for(let y=0;y<3;y++){
for(let x=0;x<3;x++){

let px=startX+x*size
let py=startY+y*size

ctx.strokeStyle="white"
ctx.strokeRect(px,py,size,size)

let data=ctx.getImageData(px+20,py+20,20,20).data

let r=0,g=0,b=0

for(let i=0;i<data.length;i+=4){

r+=data[i]
g+=data[i+1]
b+=data[i+2]

}

r/=data.length/4
g/=data.length/4
b/=data.length/4

let color=detectarColor(r,g,b)

ctx.fillStyle=color
ctx.fillRect(px+20,py+20,20,20)

}

}

requestAnimationFrame(detectar)

}

function detectarColor(r,g,b){

if(r>200 && g>200 && b>200) return "white"

if(r>200 && g<80 && b<80) return "red"

if(r>200 && g>120 && b<80) return "orange"

if(r>200 && g>200 && b<80) return "yellow"

if(g>150 && r<100) return "green"

if(b>150 && r<100) return "blue"

return "gray"

}

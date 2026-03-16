const video=document.getElementById("video")
const canvas=document.getElementById("overlay")
const ctx=canvas.getContext("2d")

const caraDiv=document.getElementById("cara")

const colores=["white","red","orange","yellow","green","blue"]

let caraDetectada=[
"gray","gray","gray",
"gray","gray","gray",
"gray","gray","gray"
]

crearCara()

navigator.mediaDevices.getUserMedia({video:true})
.then(stream=>{

video.srcObject=stream

video.onloadedmetadata=()=>{
video.play()
requestAnimationFrame(detectar)
}

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

caraDetectada[y*3+x]=color

}

}

actualizarCara()

requestAnimationFrame(detectar)

}

function detectarColor(r,g,b){

if(r>200 && g>200 && b>200) return "white"

if(r>200 && g<80 && b<80) return "red"

if(r>200 && g>120 && b<80) return "orange"

if(r>200 && g>200 && b<80) return "yellow"

if(g>150 && r<120) return "green"

if(b>150 && r<120) return "blue"

return "gray"

}

function crearCara(){

caraDiv.innerHTML=""

for(let i=0;i<9;i++){

let c=document.createElement("div")
c.className="cuadro"
c.dataset.i=i

c.onclick=()=>cambiarColor(i)

caraDiv.appendChild(c)

}

}

function actualizarCara(){

let cuadros=document.querySelectorAll(".cuadro")

for(let i=0;i<9;i++){

cuadros[i].style.background=caraDetectada[i]

}

}

function cambiarColor(i){

let actual=caraDetectada[i]

let idx=colores.indexOf(actual)

idx=(idx+1)%colores.length

caraDetectada[i]=colores[idx]

actualizarCara()

}

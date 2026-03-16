const instrucciones=[
"Escanear cara BLANCA",
"Girar DERECHA → cara NARANJA",
"Girar ABAJO → cara VERDE",
"Girar DERECHA → cara AMARILLA",
"Girar DERECHA → cara AZUL",
"Girar ABAJO → cara ROJA"
]

let caraActual=0
let cubo=[]

const video=document.getElementById("video")

navigator.mediaDevices.getUserMedia({video:true})
.then(stream=>{
video.srcObject=stream
})

document.getElementById("instruccion").innerText=instrucciones[caraActual]

function crearCara(){

let cont=document.getElementById("cara")
cont.innerHTML=""

for(let i=0;i<9;i++){

let c=document.createElement("div")
c.className="cuadro"
c.style.background="gray"

c.onclick=()=>cambiarColor(c)

cont.appendChild(c)

}

}

const colores=[
"white",
"red",
"orange",
"yellow",
"green",
"blue"
]

function cambiarColor(c){

let actual=colores.indexOf(c.style.background)

actual=(actual+1)%6

c.style.background=colores[actual]

}

crearCara()

function guardarCara(){

let cuadros=document.querySelectorAll(".cuadro")

cuadros.forEach(c=>{

switch(c.style.background){

case "white":cubo.push("U");break
case "red":cubo.push("R");break
case "green":cubo.push("F");break
case "yellow":cubo.push("D");break
case "orange":cubo.push("L");break
case "blue":cubo.push("B");break

}

})

caraActual++

if(caraActual<6){

document.getElementById("instruccion").innerText=instrucciones[caraActual]
crearCara()

}
else{

resolver()

}

}

async function resolver(){

let res=await fetch("/solve",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({cube:cubo.join("")})
})

let data=await res.json()

let scramble=data.solution.split(" ").reverse().join(" ")

let url=
"https://alpha.twizzle.net/edit/?puzzle=3x3x3&alg="+
encodeURIComponent(scramble)

window.location=url

}
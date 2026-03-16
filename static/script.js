const video = document.getElementById("video");

navigator.mediaDevices.getUserMedia({video:true})
.then(stream=>{
video.srcObject = stream;
});

async function solve(){

let cube = prompt("Pega el string del cubo (54 letras)");

let res = await fetch("/solve",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({cube:cube})
});

let data = await res.json();

if(data.solution){

document.getElementById("result").innerText =
"Solucion: "+data.solution;

let scramble = data.solution.split(" ").reverse().join(" ");

let url =
"https://alpha.twizzle.net/edit/?puzzle=3x3x3&alg="+
encodeURIComponent(scramble);

window.open(url);

}
}
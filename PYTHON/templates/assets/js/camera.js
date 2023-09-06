const socket = io("http://172.20.10.3:5001/")

const camera = document.querySelector(".photo")
const names = document.querySelector(".names")

socket.on("camera", function(data){
console.log("dwd")
    camera.src = data.img;
    names.textContent = data.names.length ? data.names: "Людей не обнаружено" ;
})

setInterval(()=>{
    socket.emit("push_camera")
}, 2000)
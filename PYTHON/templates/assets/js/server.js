const bthLock = document.querySelector(".lock")
const bthLight = document.querySelector(".light")
const bthLight1 = document.querySelector(".light1")
const bthLight2 = document.querySelector(".light2")
const bthLight3 = document.querySelector(".light3")
const cardTemperature = document.querySelector(".temperature")
const cardHumidity = document.querySelector(".humidity")
const bthCoffee= document.querySelector(".coffee")
const names = document.querySelector(".names")
const socket = io("http://172.20.10.3:5001/")

let light
let light1
let light2
let light3
let lock
let coffee

socket.on("getData", function(data){
    console.log(data)
    lock = data.lock
    light1 = data.light1
    light = data.light
    light2 = data.light2
    light3 = data.light3
    coffee = data.coffee
    if(data.coffee){
        bthCoffee.textContent = "Заварить"
    }
    else{
        bthCoffee.textContent = "Остановить"
    }
    if(data.lock){
        bthLock.textContent = "Дверь открыта"
    }
    else{
        bthLock.textContent = "Дверь закрыта"
    }
    if(data.light){
        bthLight.textContent = "Выключить"
    }
    else{
        bthLight.textContent = "Включить"
    }
    if(data.light1){
        bthLight1.textContent = "Выключить"
    }
    else{
        bthLight1.textContent = "Включить"
    }
    if(data.light2){
        bthLight2.textContent = "Выключить"
    }
    else{
        bthLight2.textContent = "Включить"
    }
    if(data.light3){
        bthLight3.textContent = "Выключить"
    }
    else{
        bthLight3.textContent = "Включить"
    }
    cardTemperature.textContent = data.air_temp
    cardHumidity.textContent = data.humidity
})

socket.on("lock_names", function(data){
    names.textContent = data.length ? data: "В доме сейчас нет людей" ;
    console.log(data)
})

bthLock.addEventListener("click", function(){
    console.log("sqq")
    lock = !lock
    socket.emit("lock", {status: lock})
    if(lock){
        bthLock.textContent = "Дверь открыта"
    }
    else{
        bthLock.textContent = "Дверь закрыта"
    }
})

bthLight.addEventListener("click", function(){
    light = !light
    socket.emit("light", {status: light})
    if(light){
        bthLight.textContent = "Выключить"
    }
    else{
        bthLight.textContent = "Включить"
    }
})

bthLight1.addEventListener("click", function(){
    light1 = !light1
    socket.emit("light1", {status: light1})
    if(light1){
        bthLight1.textContent = "Выключить"
    }
    else{
        bthLight1.textContent = "Включить"
    }
})

bthLight2.addEventListener("click", function(){
    light2 = !light2
    socket.emit("light2", {status: light2})
    if(light2){
        bthLight2.textContent = "Выключить"
    }
    else{
        bthLight2.textContent = "Включить"
    }
})

bthLight3.addEventListener("click", function(){
    light3 = !light3
    socket.emit("light3", {status: light3})
    if(light3){
        bthLight3.textContent = "Выключить"
    }
    else{
        bthLight3.textContent = "Включить"
    }
})

bthCoffee.addEventListener("click", function(){
    coffee = !coffee
    socket.emit("coffee", {status: coffee})
    if(coffee){
        bthCoffee.textContent = "Заварить"
    }
    else{
        bthCoffee.textContent = "Остановить"
    }
})

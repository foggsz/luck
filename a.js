// new Promise((resolve)=>{
//     resolve(1)
// }).then(data=>console.log(data))

// setTimeout(function(){
//     process.nextTick(()=>{
//         console.log(777)
//     })
//     new Promise((resolve)=>{
//         console.log(1111)
//         resolve(888)
//     }).then((data)=>console.log(data))
//     console.log(2)
// },0)

// setTimeout(function(){
//     console.log(7777777777771)
// },0)


// process.nextTick(function(){
//     console.log(111)
//     process.nextTick(function(){
//         console.log(222)
//         setTimeout(function(){
//             console.log(2222)
//         },0)
//         process.nextTick(function(){
//             console.log(3333)
//         })
//     })
// })

// var a=9 ,b=10 

Function.prototype.myBind = function(thisArg){
    let context = thisArg
    let toBind = this
    let args = Array.prototype.slice.call(arguments, 1)
    console.log(context)
    var x = function(){
        let arguments_arr = args.concat(Array.prototype.slice.call(arguments))
        console.log(this)
        return toBind.apply( this instanceof x? this: context, arguments_arr)
    }

    if(this.prototype){
        x.prototype = Object.create(this.prototype)
    }
    return x
}

function sum(a,c){
    this.x = a
}

let x = {
    b:'11'
}

class Events {
    constructor(){
        this.events = {}
    }

    on(eventName, func){
        if(this.events[eventName]){
            this.events[eventName].push(func)
        }else {
            this.events[eventName] = [func]
        }
    }

    emit(eventName, ...args){
        this.events[eventName] && this.events[eventName].map((item)=>{
            item(...args)
        })
    }

    off(eventName){
        delete this.events[eventName]
    }

    once(eventName,func){
        this.on(eventName, (...args)=>{
            func(...args)
            this.off(eventName)
            console.log(this.events)
        })
    }
}
let  onceE = new Events()
onceE.once('abc', function(a,b){
    console.log(a)
})
onceE.emit('abc', 1,2)
onceE.on('hello', function(a,b){
    console.log(a)
})
onceE.emit('hello', 'hello', 'nhao')
onceE.emit('hello', 'hellotwo', 'nhao')
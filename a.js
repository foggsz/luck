new Promise((resolve)=>{
    console.log(0)
    resolve(1)
}).then(data=>console.log(data))

setTimeout(function(){
    console.log(2)
},0)
process.nextTick(function(){
    console.log(111)
    process.nextTick(function(){
        console.log(222)
        setTimeout(function(){
            console.log(2222)
        },0)
        process.nextTick(function(){
            console.log(3333)
        })
    })
})
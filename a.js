new Promise((resolve)=>{
    console.log(0)
    resolve(1)
}).then(data=>console.log(data))

setTimeout(function(){
    process.nextTick(()=>{
        console.log(777)
    })
    new Promise((resolve)=>{
        console.log(1111)
        resolve(888)
    }).then((data)=>console.log(data))
    console.log(2)
},0)

setTimeout(function(){
    console.log(7777777777771)
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


6501,6828,6963,7036,7422,7674,8146,8468,8704,8717,9170,9359,9719,9895,9896,9913,9962,154,293,334,492,1323,1479,1539,1727,1870,1943,2383,2392,2996,3282,3812,3903,4465,4605,4665,4772,4828,5142,5437,5448,5668,5706,5725,6300,6335
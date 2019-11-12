function debounce(func, delay){
    var t = null
    return  function(){
        clearTimeout(t)
        t = setTimeout(() => {
            console.log(11111)
            func.apply(this, arguments)
        }, 3000)
    }
}


function jy(func, delay){
    var can = true
    return function(){
        if(can){
            setTimeout(function(){
                func.apply(this,arguments)
                can = true
            })
        }
        can = false
    }
}

function say(){
    console.log('say')
}
jy(say, 1000)



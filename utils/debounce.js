function debounce(func, delay){
    let t = null
    return  function(){
        clearTimeout(t)
        setTimeout(() => {
            func.apply(this, arguments)
        })
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



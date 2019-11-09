function compose(middlewares){
    return function(context, next){
        let len = middlewares.length
        let dispitch = function(i){
            let fn = middlewares[i]
            if(i>len){
                throw  new Promise(111)
            }
            if(!fn){
                return Promise.resolve()
            }
            return Promise.resolve(fn(context, dispitch.bind(null, i+1)) )
        }
        return dispitch(0)
    
    }
}
let a =  async function(ctx,next){
    console.log(1)
    await next()
}

let b =  function(ctx, next){
    console.log(2)
    next()
}

let c =  function(ctx, next){
    console.log(3)
}
compose([a,b,c])()
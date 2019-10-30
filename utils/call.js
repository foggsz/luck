Function.prototype.myCall = function(thisArg){
    let context  =  thisArg || {}
    context.fn = this
    let result = context.fn( ...[].slice.call(arguments, 1))
    delete context.fn
    return result
}


function a(x,y,z){
    console.log('x,y,z', x,y,z)
    this.x = x
}

b = {}
let x = Function.prototype.myCall.myCall(a,b,1,2,3,45)
Reflect.apply(a,b,[1,2,3]) == Function.prototype.apply.call(a,b,[999])


function Sum_Solution(n)
{
    if(n<=1){
        return 1
    }      
    return Sum_Solution(n-1)+n    
}

let res  =Sum_Solution(6)
1,2,3,4,5
console.log(res)

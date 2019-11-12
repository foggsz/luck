var obj = {
    name:10,age:11
}

var handler = {
    get: function (target, key,receiver){
        console.log('get', receiver)
       return Reflect.get(target, key, receiver) 
    },
    set: (target, key, val, receiver) =>{
        console.log('receiver')
        return  target[key] = val
    }
}
var proxy = new Proxy(obj, handler)
proxy.name = 111
function abc(){
    this.a  = 10
}

var c = {}

let x = Function.prototype.apply

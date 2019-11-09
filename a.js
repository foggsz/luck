function nn(){
    this.name = 10
}
nn.prototype.say = function(){
    console.log('say')
}
function abc(){
    // nn.call( this)
}
// console.log(abc.prototype.constructor)
// abc.prototype = Object.create(nn)
// abc.prototype.constructor = abc
// let x = new abc()


function xz(arr){
    for(let i=0; i<arr.length; i++){
        let min = i, temp = arr[i]
        for(let j= i+1;j<arr.length;j++ ){
            if(arr[j]<temp){
                min = j
            }
        }
        arr[i] = arr[min]
        arr[min] = temp
    }
    return arr
}

// 数组
// 返回第一个函数
// 通过next 递归调用


function compose(middlewares){
    return function(context, next){
        let index = -1
        function dispath(i){
            if(i<=index){
                throw new Error("调用顺序不对")
            }
            index =i
            let fn = middlewares[i]
            if(!fn){
                return Promise.resolve()
            }
            if(i === middlewares.length){
                fn = next
            }

            return Promise.resolve(fn(context, dispath(i+1)))
        }
    }
}


var x = function(){
    return function(){
        setTimeout(function(){
            arguments[0] = arguments[0]+1
        })
    }
}



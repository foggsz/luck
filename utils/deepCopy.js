function deepCopy(obj){
    if(!(typeof obj == 'object')){
        return obj
    }

    if(Object.prototype.toString.call(obj) == "[object RegExp]"){
        return new RegExp(obj)

    }
    let newObj =  Array.isArray(obj)?[]:{ }
    for(let key in obj){
        newObj[key] = deepCopy(obj[key])
    }
    return newObj
}

function gd_deepCopy(obj){  //广度深拷贝
    let newObj = {}
    let queue = []
    for(let key in obj){
        queue.push({
            key:key,
            value: obj[key],
            parent: newObj
        })
    }

    while(queue.length){
        let currentNode = queue.shift()
        let parent = currentNode.parent
        let currentKey = currentNode.key
        let currentValue = currentNode.value
        if(typeof currentValue == 'object' || typeof currentValue == 'Array' ){

            parent[currentKey] = Object.prototype.toString.call(currentValue) === '[object Array]'?[]:{}
            for(let key in currentValue){
                queue.push({
                    key: key,
                    value: currentValue[key],
                    parent: parent[currentKey]
                })             
            }
        }else{
            parent[currentKey] = currentValue;
        }
    }
    return newObj
}

function sd_deepCopy(obj){  //深度深拷贝
    let newObj = {}
    let stack = []
    for(let key in obj){
        stack.push({
            key:key,
            value: obj[key],
            parent: newObj
        })
    }

    while(stack.length){
        let currentNode = stack.pop()
        let parent = currentNode.parent
        let currentKey = currentNode.key
        let currentValue = currentNode.value
        if(typeof currentValue == 'object' || typeof currentValue == 'Array' ){

            parent[currentKey] = Object.prototype.toString.call(currentValue) === '[object Array]'?[]:{}
            for(let key in currentValue){
                stack.push({
                    key: key,
                    value: currentValue[key],
                    parent: parent[currentKey]
                })             
            }
        }else{
            parent[currentKey] = currentValue;
        }
    }
    return newObj
}

let origin = {
    name:{
        age:[1,2,3]
    },
    sex:{
        male:{
            j:{
                j:1
            },
            c:[222]
        }
    },
    a: new RegExp('ssss')
}
let newObj = {}

let newObj_two = {}

newObj = deepCopy(origin)
console.log(newObj)
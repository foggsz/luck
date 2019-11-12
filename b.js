function Node(val){
    this.val = val
    this.left = null
    this.right = null
}

function Mirror(root)
{
    let left = root.left
    root.left =  root.right
    root.right = left
    if(root.left){
        Mirror(root.left)
    }
    if(root.right){
        Mirror(root.right)
    }
    return root
}

let n = new Node(1)
let b = new Node(2)
// let c = new Node(3)
n.left = b
// n.right = 


function isInstance(instance, obj){
    let prototype = instance.__proto__
    if(!prototype){
        return false
    }
    return prototype === obj.prototype ? true:isInstance(prototype.__proto__, obj)
}
let x = []
let res = isInstance(x, Array)


setImmediate(()=>{
    console.log(1)

    setTimeout(function(){
        console.log(2)
    },100)

    setImmediate(()=>{
        console.log(3)
    })

  
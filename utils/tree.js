let arr = [
    {id:1, context:'1'},
    {id:2, context:'2'},
    {id:3, context:'3', pid:1},
    {id:4, context:'4', pid:2},
    {id:5, context:'4', pid:4}
]
function tree(arr){
    let hashMap = {}
    let res = []
    for(let i in arr){
        let item = arr[i]
        hashMap[item.id] = item
    }
    for(let i  in arr ){
        let item  = arr[i]
        if(item.pid){
            hashMap[item.pid].child  = hashMap[item.pid].child || []
            hashMap[item.pid].child.push(item)
        }else {
            res.push(item)
        }
    }
    console.log(hashMap)
    console.log(res)
    return res
}
console.dir(tree(arr))
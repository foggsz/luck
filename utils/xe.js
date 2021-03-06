let arr = [2323,11,22,477,55,77]

function xz(arr){
    for(let i =0; i<arr.length-1; i++){
        let min = i
        for(let j= i+1; j<arr.length; j++){
            if(arr[j]<=arr[min]){
                min = j
            }
        }
        let temp = arr[i]
        arr[i] = arr[min]
        arr[min] = temp
    }
    return arr
}

function mp(arr){
    for(let i=0; i<arr.length-1; i++){
        for(let j=0; j<arr.length-i; j++){
            if(arr[j]<arr[j-1]){
                let temp = arr[j]
                arr[j] = arr[j-1]
                arr[j-1] = temp
            }
        }
    }
    return arr
}

function cr(arr){  //与假定排序好的数依次比较
    var j
    for(i=1; i<arr.length; i++){
        let temp = arr[i]
        for(j=i; j>0&&arr[j-1]>temp; j--){
            arr[j] = arr[j-1]
        }
        arr[j] = temp
    }
    return arr
}


function xr(arr){

    let mid= Math.floor(arr.length/2)
    let len = arr.length
    for(let gap=mid; gap>0; gap=Math.floor(gap/2)){ 
        for(let i=gap; i<len; i++){  // 对分组进行插入排序
            let temp = arr[i]
            let j
            for(j=i; j>=gap && arr[j-gap]<temp; j= j-gap){
                arr[j] =arr[j-gap]
            }
            arr[j] = temp
        }
    }
    return arr
}


function partition(arr, low, high){  // 快速排序 首先选定中轴，在第一次排序的时候 将小于中轴元素放在左边，大于放在右边，
    //最后中轴位于中央。轮番如此知道剩下一个元素数组为止
    let pivot = arr[high]
    let i = (low-1)
    for(let j=low; j<high; j++){
        if(arr[j]<pivot){
            i++
            let temp = arr[j]
            arr[j] = arr[i]
            arr[i] = temp
        }
    }
    arr[high] = arr[i+1]
    arr[i+1] = pivot
    return i+1

}

function ks(arr){
    high = arr.length-1
    low = 0
    if(low<high){
        let middle = partition(arr, low, high)
        partition(arr,low, middle-1)
        partition(arr,middle+1, high)
    }
    return arr
}
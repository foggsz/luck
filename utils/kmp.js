function kmp(str, query_str){
    let len = str.length, query_len = query_str.length;
    let next = getNext(query_str), result = -1;
    for(let i=0, j=0; i<len && j <query_len; ){
        if(j ==-1 || str[i] === query_str[j]){
            i++
            j++
            if(j===query_len){
                result = i-j
            }
        }else {
            j = next[j]
        }

    }

    return result
}


function getNext(query_str){
    let next = [], i=0, len = query_str.length;
    let prefix = '', suffix = '';
    while(i<len){
        if(i>=2){
           prefix = query_str.slice(0, i)
           suffix = query_str.slice(1,i+1) 
           next[i] =  prefix == suffix ? prefix.length:0 
        } else{
            next[i]  = 0
        }
        i++

    }
    next.unshift(-1)
    next.pop()
    return next
}

let  str = 'abababcassssss'
let  query_str = 'bababca'
let res = kmp(str, query_str)
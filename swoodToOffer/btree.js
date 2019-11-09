function abc(){
    setTimeout(()=>{
        console.log(1)
        Promise.resolve().then((data)=>{
            console.log(111)
        })
    })
    setTimeout(()=>{
        console.log(2)
        Promise.resolve().then((data)=>{
            console.log(131)
        })
    })
}

abc()
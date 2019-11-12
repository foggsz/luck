

function isFunction(fn){
    if(!(fn instanceof Function)){
        throw new Error("请传入一个函数")
    }
}

const REJECTED = 'rejected'
const RESOLVED = 'resolved'
const PENDING = 'pending'


function PromiseMy(fn){
    this.state = PENDING
    this.value = null
    this.handlers = []
    fn(this.resolve.bind(this), this.reject.bind(this))
}   

PromiseMy.prototype.onfilled = function(val){
    this.state = RESOLVED
    this.value = val
    this.handlers.forEach(this.handle)
}

PromiseMy.prototype.reject = function(val){
    this.state = REJECTED
    this.value = val
    console.log(this.handlers)
    this.handlers.forEach(this.handle)
}

PromiseMy.prototype.done = function (onfilled, onRejected) {
    // ensure we are always asynchronous
    setTimeout( ()=> {
      this.handle({
        onfilled: onfilled,
        onRejected: onRejected
      });
    }, 0);
  }

  PromiseMy.prototype.handle = function(handler) {
    let state = this.state, value = this.value
    if (state === PENDING) {
        this.handlers.push(handler);
    } else {
      if (state === RESOLVED &&
        typeof handler.onfilled === 'function') {
        handler.onfilled(value);
      }
      if (state === REJECTED &&
        typeof handler.onRejected === 'function') {
        handler.onRejected(value);
      }
    }
  }

PromiseMy.prototype.resolve = function(val){
    let then = getThen(val)
    if (then) {
        this.doResolve(then.bind(val), this.resolve, this.reject)
        return
    }
    this.onfilled(val)
}

PromiseMy.prototype.then = function(onfilled, rejected){
    onfilled = typeof onfilled!='function'? ()=>{}:onfilled
    reject = typeof reject!='function'? ()=>{}:rejected
    let self = this
    return new PromiseMy( (resolve,reject)=>{
        self.done(function(result){
            resolve(onfilled(result))
        }, function(error){
            reject(rejected(error))
        })
    })

}

PromiseMy.prototype.doResolve = function(fn, resolve, reject){
    var done = false;
    try {
      fn(function (value) {
        if (done) return
        done = true
        resolve(value)
      }, function (reason) {
        if (done) return
        done = true
        reject(reason)
      })
    } catch (ex) {
      if (done) return
      done = true
      reject(ex)
    }

}

function getThen(value){
    if(typeof value === 'object' || typeof value =='function'){
        let then = value.then
        if(typeof then =='function'){
            return then
        }
    }
    return null
}

let x = new PromiseMy((resolve,reject)=>{
    resolve(1)
}).then((data)=>{
   return new PromiseMy((resolve, reject)=>{
       reject(111)
   })
}, (err)=>{
    console.log(err,222)
}).then(()=>{}, (err)=>console.log(111,err))
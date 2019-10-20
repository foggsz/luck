

class Compile{
    constructor(el, vm){
        this.el = this.isElementNode(el)?el: document.querySelector(el)
        this.vm = vm
        if(this.el){
            let fragment = this.nodeFragment(this.el)
            // 编译文档节点
            this.compile(fragment)
            this.el.appendChild(fragment)
        }


    }

    isElementNode(node){
        return node.nodeType === 1
    }

    nodeFragment(el){
        let fragment = document.createDocumentFragment()
        let firstChild
        while(firstChild = el.firstChild){
            fragment.appendChild(firstChild)
        }
        return fragment
    }

    isDirective(name){
        return name.includes('v-')
    }

    //解析文档节点
    compile(fragment){
        let childNodes = fragment.childNodes
        Array.from(childNodes).forEach(node=>{
            if(this.isElementNode(node)){
                this.compile(node)
                this.compileElemnt(node)
            }else{
                this.compileText(node)
            }
        })
    }

    compileElemnt(node){
        let attrs = node.attributes
        Array.from(attrs).forEach(attr=>{
            let attrName = attr.name
            if(this.isDirective(attrName)){
                let exp = attr.value
                let [, type] = attrName.split('-')

                CompileUtil[type](node, this.vm, exp)
            }
        })
    }
    compileText(node){
        let exp = node.textContent
        let reg = /\{\{([^}]+)\}\}/g

        if(reg.test(exp)){
            CompileUtil["text"](node, this.vm, exp)
        }
    }
}
var CompileUtil = {}


CompileUtil.getVal= function(vm, exp){
    exp = exp.split('.')
    return exp.reduce((prev,next)=>{
        return prev[next]
    }, vm.$data)
}

CompileUtil.getTextVal = function(vm, exp){
        return exp.replace(/\{\{([^}]+)\}\}/g, (...args) => {
            return CompileUtil.getVal(vm, args[1]);
        });
    }

CompileUtil.setVal = function(vm, exp, newVal){
        exp = exp.split('.')
        return exp.reduce( (prev, next, index)=>{
            if(index === exp.length-1){
                // console.log(prev, newVal)
                return prev[next] = newVal
            }
            return prev[next]
        }, vm.$data)
    }


CompileUtil.updater = {
    textUpdater(node, value){
        node.textContent = value
    },

    modelUpdater(node, value){
        node.value = value
    }
}

CompileUtil.model = function(node, vm, exp){
    let updateFn = CompileUtil.updater['modelUpdater']

    let value = CompileUtil.getVal(vm, exp)
    new Watcher(vm, exp, newValue=>{
        updateFn && updateFn(node, newValue)
    })


    node.addEventListener('input', e => {
        // 获取输入的新值
        let newValue = e.target.value;

        // 更新到节点
        CompileUtil.setVal(vm, exp, newValue);
    });
    updateFn && updateFn(node, value)

}


CompileUtil.text = function(node, vm, exp){
    let updateFn = CompileUtil.updater['textUpdater']
    let value = CompileUtil.getTextVal(vm, exp)
    exp.replace(/\{\{([^}]+)\}\}/g, (...args) => {
        new Watcher(vm, args[1], newValue => {
            updateFn && updateFn(node, newValue);
        });
    });

    // 第一次设置值
    updateFn && updateFn(node, value);

}

class Dep{
    constructor(){
        this.subs = []
    }

    addSub(watcher){
        this.subs.push(watcher)
    }

    notify(){
        this.subs.forEach((watcher)=>{
            watcher.update()
        })
    }
}

class Watcher{
    constructor(vm, exp, callback){
        this.vm = vm
        this.exp = exp
        this.callback = callback
        this.value = this.get()
    }

    get(){
        Dep.target =  this
        let value = CompileUtil.getVal(this.vm, this.exp)
        Dep.target = null
        return value
    }
    update(){
        let newVal = CompileUtil.getVal(this.vm, this.exp)
        let oldVal = this.value
        if(newVal!== oldVal){
            this.callback(newVal)
        }
        
    }
}

class Observer{
    constructor(data){
        this.observer(data)
    }

    observer(data){
        if(!data||typeof data!='object'){
            return   
        }

        Object.keys(data).forEach(key=>{
            this.defineReactive(data, key, data[key])
            this.observer(data[key])

        })
    }

    defineReactive(object, key, value){
        let dep = new Dep()
        let _this = this
        Object.defineProperty(object, key, {
            enumerable: true,
            configurable: true,
            get () { // 当取值时调用的方法
                Dep.target && dep.addSub(Dep.target);
                return value;
            },
            set (newValue) { // 当给 data 属性中设置的值适合，更改获取的属性的值
                if(newValue !== value) {
                    _this.observer(newValue); // 重新赋值如果是对象进行深度劫持
                    value = newValue;
                    dep.notify(); // 通知所有人数据更新了
                }
            }
        })

    }
}
class MVVM {
    constructor(options){
        this.$el = options.el
        this.$data = options.data

        if(this.$el){
            new Observer(this.$data)
            this.proxyData(this.$data)
            new Compile(this.$el, this)
            
        }
    }

    proxyData(data){
        Object.keys(data).forEach(key=>{
            Object.defineProperty(this, key, {
                get(){
                    return data[key]
                },
                set(newVal){
                    data[key] = newVal
                }
            })
        })

    }
}
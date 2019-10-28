import React, {useEffect, useState, Suspense} from 'react';
import ReactDOM from 'react-dom';
import './index.css';
// import {x} from './App';
// console.log(x)

import App, {x} from './App'
import * as serviceWorker from './serviceWorker';
x.name = 999
setTimeout(()=>{ console.log(x.name); x.name=900;  }, 200)
function Form() {
    // 1. Use the name state variable
    const [name, setName] = useState('Mary');
  
    // 2. Use an effect for persisting the form
    // 3. Use the surname state variable
    const [surname, setSurname] = useState('Poppins');
    
    
    // 4. Use an effect for updating the title
    
    useEffect(function persistForm() {
        console.log('name11111', name)
        // localStorage.setItem('name', name)
      });
    useEffect(function updateTitle() {
      console.log('update title')
       document.title = name + ' ' + surname;
    })

    return (
        <div>
          <Suspense fallback={<div>Loading...</div>}>
            <section>
                <div onClick={()=>{ return setName('haha')} }>name: {name}</div>
                <div onClick={()=>{ return setSurname('heihei')} }>surname: {surname}</div>
            </section>
          </Suspense>
        </div>
      );
    // ...
  }
function Welcome(props){
    return (
        <div>hello {props.name}</div>
    )
}

// react 组件props参数  和纯函数一样， 不要对参数做修改，保持不可变性
function World(){
    return (
        <div>
            <Welcome name="god"/>
            <Welcome name='world'/>

        </div>
    )
}

class Clock extends React.Component{
    constructor(props){
        super(props)
        this.state ={
            date: new Date()
        }
    }

    componentDidMount(){  // 第一次渲染
        this.timer = setInterval(
            ()=>this.tick(),
            4000
        )

    }

    componentWillUnmount(){ //  会在组件卸载及销毁之前直接调用。在此方法中执行必要的清理操作，例如，清除 timer，取消网络请求或清除在 componentDidMount() 中创建的订阅等。
        clearInterval(this.timer)
    }

    componentWillUpdate(){
        console.log('update')
    }
    tick(){
        this.setState({
            date:new Date()
        })
    }
    render(){
        return (
            <div>{this.state.date.toLocaleTimeString()}</div>
        )
    }
}


ReactDOM.render( <World/>, document.getElementById('root'))
ReactDOM.render(<App />, document.getElementById('root'));
ReactDOM.render(<Form />, document.getElementById('root'));
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

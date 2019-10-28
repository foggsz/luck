import React, {  Component  }from 'react';
import './App.css';

class Square extends Component{
  render(){
    return (
      <button className='square' 
        onClick={
          () => this.props.onClick()
        }
      >
        {this.props.value}
      </button>
    )
  }

}
class Borard extends Component{

  renderSquare(i){
    return <Square value={this.props.squares[i]} 
        onClick={
            this.handleClick.bind(this, i)
          }
    />
  }

  handleClick(i){
    this.props.onClick(i)
  }

  render(){

    return (
      <div>
        <div className="board-row">
          {this.renderSquare(0)}
          {this.renderSquare(1)}
          {this.renderSquare(2)}
        </div>
        <div className="board-row">
          {this.renderSquare(3)}
          {this.renderSquare(4)}
          {this.renderSquare(5)}
        </div>
        <div className="board-row">
          {this.renderSquare(6)}
          {this.renderSquare(7)}
          {this.renderSquare(8)}
        </div>
      </div>
    )
  }
}

class Game extends Component{
  constructor(props){
    super(props)
    this.state = {
      history: [
        {
          squares:Array(9).fill(null)
        }
      ],
      xIsNext:true,
      stepNumber:0,
    }
  }

  render(){
      const history = this.state.history
      let stepNumber = this.state.stepNumber
      const current = history[stepNumber]
      const winer = calculateWinner(current.squares)

      const moves = history.map((step, move)=>{
        const desc = move?'Go to move '+move: 'Go to game start'
          return (
            <li key={move}>
              <button onClick = { ()=>  this.jumpTo(move) }>{desc}</button>
            </li>
            )
      })

      var status
      if(winer){
        status = 'winer: '+winer
      }else{
        let value = this.state.xIsNext?'X':'O'
        status = 'Next: '+value
      }


      return (
        <div className='game'>
          <div className='game-board'>
            <Borard  squares={current.squares}
              onClick={ (i)=>this.handleClick(i)}
            />
          </div>
          <div className='game=info'>
            <div>{status}</div>
            <div>{moves}</div> 
          </div>
        </div>
      )
  }

  jumpTo(step){
    this.setState({
      stepNumber:step,
      xIsNext: step%2===0
    })
  }

  handleClick(i){
    let stepNumber = this.state.stepNumber
    let history = this.state.history.slice(0,stepNumber+1)

    let current = history[history.length -1]
    let squares = current.squares.slice() // 不可变性，新数组

    let winer = calculateWinner(squares)
    if(winer || squares[i]){
      return
    }

    squares[i] = this.state.xIsNext?'X':'O'
    history.push({squares: squares})
    this.setState({
      history:history,
      xIsNext:!this.state.xIsNext,
      stepNumber: history.length-1
    })
  }
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

export var x = { name:10}
export default Game;
x.name = 10000
setTimeout(()=>console.log(x.name), 500)
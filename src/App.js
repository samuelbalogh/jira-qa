import React, {Component} from 'react';
import issues from './components/issues';
import './App.css';


class App extends Component {
  state = {
    issues: []
  }

  render () {
    return (
      <issues issues={this.state.issues} />
    )
  }

  componentDidMount() {
    fetch('http://127.0.0.1:5000/qa-time/76')
    .then(res => res.json())
    .then((data) => {
      console.log(data)
      this.setState({ issues: data })
    })
    .catch(console.log)
  }
}

export default App;

import React from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap';
import './style/index.css';
import './style/MassageList.css';
import './style/Header.css';
import './style/Userinput.css'

import ChatWindow from './components/chatwindow';

//class Application 

class App extends React.Component {
  constructor(props){
    super();
    const text = 'Hello world!'
    this.state = {
      messageList:[{
        author: 'them',
        type: 'text',
        data: {text}
      }]
    }
  }
  // Message functions
  //

  // state setting
  _onMessageWasSent(message) {
    this._sendMessage(message)
    console.log(message)
    this.setState({
      messageList: [...this.state.messageList, message]
    })
  }

  // sending messages and receiving messages
  // POST method
  // route path : 'http://localhost:7001/test/'
  // after receiving messages, update state of messagelist.

  async _sendMessage(message){
    var data = JSON.stringify(message.data.text);
    
    var url = 'http://localhost:7001/test/';
    let initHeaders = new Headers()
    initHeaders.append('Accept', 'application/json, text/plain, */*')
    initHeaders.append('Content-Type', 'application/x-www-form-urlencoded');

    const init = {
      method: 'POST',
      
      headers: initHeaders,
      body: `data=${data}`
    }

    const res = await fetch(url,init)
    var s = await res.json()
    console.log(s)
      message = 
      {
        author: 'them',
        type: 'text',
        data: {text:s}
      }
      console.log(message)
      this.setState({messageList: [...this.state.messageList,message]
    });
  }


  // render
  render() {
    return (
      <div className="App">
          <ChatWindow
            messageList = {this.state.messageList}
            onMessageWasSent={this._onMessageWasSent.bind(this)}
          ></ChatWindow>
      </div>
      
    );
  }
}
App.propTypes = {
  messageList: PropTypes.arrayOf(PropTypes.object),
};


ReactDOM.render(<App />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.

import React, { Component } from 'react';
import Message from './Messages'


// class MessageList
class MessageList extends Component {

  // render
  render () {
    return (
      <div className="sc-message-list">
        {this.props.messages.map((message, i) => {
          return <Message message={message} key={i} />
        })}
      </div>)
  }
}

export default MessageList
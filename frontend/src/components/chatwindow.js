import React, { Component } from 'react';
import Header from './Header'
import Userinput from './Userinput'
import MassageList from './MassageList'


// class ChatWindow 
class ChatWindow extends Component {
    constructor(props){
        super(props);
    }
    
    handleUserInput(message){
        this.props.onMessageWasSent(message);
    }

    render(){
        let messageList = this.props.messageList || []

        return (
            <div className='sc-chat-window'>
                <Header/>
                <MassageList
                messages = {messageList}
                
                />
                <Userinput
                    onSubmit={this.handleUserInput.bind(this)}
                />

            </div>
        );

    }

}
export default ChatWindow;
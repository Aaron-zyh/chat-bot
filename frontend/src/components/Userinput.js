import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';
import {InputGroup,Button,FormControl} from 'react-bootstrap';
import './Header';


// class Userinput
class Userinput extends Component {
  
  // functions for handling actions from users

  handleClick(event) {
    event.preventDefault();
    const text =  this.userInput.value;
    if (text && text.length > 0) {
      this.props.onSubmit({
        author: 'me',
        type: 'text',
        data: { text }
      });
    }
  }
  handleKeypress(event) {
    if (event.key === 'Enter'){
      event.preventDefault();
      const text =  this.userInput.value;
      if (text && text.length > 0) {
        this.props.onSubmit({
          author: 'me',
          type: 'text',
          data: { text }
        });
      }
    }
  }


  // render
    render() {
      return (
        
          <InputGroup className ="sc-user-input" >
            <FormControl
              placeholder="talk to me..."
              aria-label="talk to me..."
              aria-describedby="basic-addon2"
              ref={(e) => {this.userInput = (e)} }
              onkeypress = {this.handleKeypress.bind(this)}
            />
            <InputGroup.Append>
              <Button variant="link" block 
              onClick = {this.handleClick.bind(this)} 
              
              >
              Send the message
              </Button>
            </InputGroup.Append>
            
          </InputGroup>
          

      );
    }
  }
  Userinput.propTypes = {
    onSubmit: PropTypes.func.isRequired
};


export default Userinput;
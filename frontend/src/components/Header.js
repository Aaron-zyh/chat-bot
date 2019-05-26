import React, { Component } from 'react';
import icon from '../assets/usr_icon.jpg'
import {Figure} from 'react-bootstrap';


// class Header
class Header extends Component {
  
    // render
    render() {
      return (
        <div className="Header">
            <div>
                <Figure>
                     <Figure.Image className ='Header--img'
                     width={80}
                     height={80}
                     alt="171x180"
                     src={icon}
                     roundedCircle
                     />
                </Figure>
            </div>
            <div className = 'Header--team-name'>
                <text className="hellow world@all!!">Mr.Banana</text>
            </div>
            <div className = 'Header--close-button'>
                
            </div>

        </div>
      );
    }
  }
  
  export default Header;
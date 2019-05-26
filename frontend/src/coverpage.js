import React, {Component} from 'react'
import { Segment } from 'semantic-ui-react';
import { Link } from 'react-router-dom';



export default class Coverpage extends Component{
  render() {
    return (
      <div className="background">
        <div className = "title">
                  <Segment
                      style={{
                          textAlign:'center',width:'60%',margin:'10px auto'
                      }}>
                      X-o-Bot: A Generic Dialog Framework for Conversational Agents
                  </Segment>
                  <Segment
                      style={{
                          textAlign:'center',width:'60%',margin:'10px auto'
                      }}>
                      A student-tutor support system<br/>
                  </Segment>
        </div>
        <div className="signemmm" >
            <img src={require('./sign.png')} alt="emmm" width="100px" height="100px"/>
        </div>
        <div className="member">
                  <Segment
                      style={{
                          textAlign:'center',margin:'10px auto',
                      }}>
                      <br/>
                      developer: <br/>
                      <br/>
                      Hao Lan (z5102853)<br/>
                      Yuanhai Zhang (z5172174)<br/>
                      Runnan Wang (z5128137)<br/>
                      Zengwei Wang (z5153232)<br/>
                  </Segment>
        </div>
        <div>
          <Link to="/Messenger/" style={{color:'black'}}>
            <div className="buttonjump">
              <button className="button">Click to chat</button>
            </div>
          </Link>
        </div>
      </div>
    )
  }
}

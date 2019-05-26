import React, {Component} from 'react';
import { BrowserRouter as Router,Route} from 'react-router-dom';
import Messenger from './userinput';
import Coverpage from './coverpage';

export default class App extends Component{

    render(){
      return (
        <Router>
          <div className="app-wrapper">
            <Route exact path="/" component={Coverpage} />
            <Route path="/" component={Messenger} />
          </div>
        </Router>
    )
    }
}

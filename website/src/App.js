import React, { Component } from 'react';
import { Column, Row } from 'simple-flexbox';
//import logo from './logo.svg';
import './App.css';



class App extends Component {

  test = [
    {tweet:0},
    {tweet:1}
  ];

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Data Science Fall 2018</h1>
          <p>Anthony DiFalco, Louis Theiry</p>
          <p>Will Fritz, Tommy Lynch</p>
        </header>
        <p className="App-intro">
          Im thinking we have a listview here, and then when the user clicks we have some data&charts render
        </p>
          <Row vertical='center'>
            <Column flexGrow={1} horizontal='center'>
              <h3>Model Graph {this.test[0].tweet}</h3>
              <img src={'./images/test_2.png'}/>
              <p>description</p>
            </Column>
            <Column flexGrow={1} horizontal='center'>
              <h3>Model Graph {this.test[1].tweet}</h3>
              <img src={'./images/test_2.png'}/>
              <p>description</p>
            </Column>
          </Row>
      </div>
    );
  }
}

export default App;

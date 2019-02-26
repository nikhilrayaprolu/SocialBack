import React from 'react';
import ReactDOM from 'react-dom';
import App from './containers/App';
import '../scss/index.scss';
import {BrowserRouter} from "react-router-dom/";
ReactDOM.render(<BrowserRouter>
    <App />
  </BrowserRouter>, document.getElementById('react-app'));

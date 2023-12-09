import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Background from './components/background';
import LoginPage from './components/login';
import Request from './components/request';
import Reset from './components/reset';
import Success from './components/success';
import Dashboard from './components/dashboard';
import BackgroundPage from './pages/backgroundpage';
import TheLogin from './pages/loginpage';
import TheRequest from './pages/requestpage';
import TheReset from './pages/resetpage';
import TheSuccess from './pages/successpage';
import Modal1 from './components/modal1';
import Modal2 from './components/modal2';
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <Router>
    <Routes>
      <Route exact path="/" element={<Background />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/request" element={<Request />} />
      <Route path="/reset" element={<Reset />} />
      <Route path="/success" element={<Success />} /> 
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/backgroundpage" element={<BackgroundPage />} />
      <Route path="/loginpage" element={<TheLogin />} />
      <Route path="/requestpage" element={<TheRequest />} />
      <Route path="/resetpage" element={<TheReset />} />
      <Route path="/successpage" element={<TheSuccess />} />
      <Route path="/modal1" element={<Modal1 />} />
      <Route path="/modal2" element={<Modal2 />} />
      {/* Add more routes for other components/pages */}
    </Routes>
  </Router>,
  document.getElementById('root')
);

reportWebVitals();



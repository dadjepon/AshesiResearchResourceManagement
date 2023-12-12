import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Background from './components/background';
// import LoginPage from './components/login';
// import Request from './components/request';
// import Reset from './components/reset';
// import Success from './components/success';
// import Dashboard from './components/dashboard';
// import BackgroundPage from './pages/backgroundpage';
import TheLogin from './pages/loginpage';
import TheRequest from './pages/requestpage';
import TheReset from './pages/resetpage';
import TheSuccess from './pages/successpage';
import AdminPremake from './components/admin_premake';
import AdminAcad from './components/admin_acad';
import AdminSem from './components/admin_sem';
import AdminSemRA from './components/admin_sem_RA';
import RaDelete from './components/ra_delete';
import reportWebVitals from './reportWebVitals';
import InvitedProjectsPage from './pages/InvitedProjectsPage';
import RequestedProjectsPage from './pages/RequestedProjectsPage';
import ViewProjectPage from './pages/ViewProjectPage';
import UserProfilePage from './pages/UserProfilePage';

import HomePage from './pages/HomePage';
import './App.css';

ReactDOM.render(
  <Router>
    <Routes>
      <Route exact path="/" element={<Background />} />
      {/* <Route path="/login" element={<LoginPage />} />
      <Route path="/request" element={<Request />} />
      <Route path="/reset" element={<Reset />} />
      <Route path="/success" element={<Success />} /> 
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/backgroundpage" element={<BackgroundPage />} /> */}
      <Route path="/loginpage" element={<TheLogin />} />
      <Route path="/requestpage" element={<TheRequest />} />
      <Route path="/resetpage" element={<TheReset />} />
      <Route path="/successpage" element={<TheSuccess />} />
      <Route path="/admin_premake" element={<AdminPremake />} />
      <Route path="/admin_acad" element={<AdminAcad />} />
      <Route path="/admin_sem" element={<AdminSem />} />
      <Route path="/admin_sem_RA" element={<AdminSemRA />} />
      <Route path="/ra_delete" element={<RaDelete />} />
      {/* Add more routes for other components/pages */}
      <Route exact path="/home" element={<HomePage />} />
      <Route path="/inv_projects" element={<InvitedProjectsPage />} />
      <Route path="/req_projects" element={<RequestedProjectsPage />} />
      <Route path="/view_project" element={<ViewProjectPage />} />
      <Route path="/profile" element={<UserProfilePage/>} />

    </Routes>
  </Router>,
  document.getElementById('root')
);

reportWebVitals();



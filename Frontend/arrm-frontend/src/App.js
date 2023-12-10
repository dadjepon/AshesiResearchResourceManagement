import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; 
import HomePage from './pages/HomePage';
import InvitedProjectsPage from './pages/InvitedProjectsPage';
import RequestedProjectsPage from './pages/RequestedProjectsPage';
import ViewProjectPage from './pages/ViewProjectPage';


function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/inv_projects" element={<InvitedProjectsPage/>}/>
          <Route path="/req_projects" element={<RequestedProjectsPage/>} />
          <Route path="/view_project" element={<ViewProjectPage/>} />
 
        </Routes>
      </div>
    </Router>
  );
}

export default App;



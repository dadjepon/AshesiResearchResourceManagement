import React, { useState, useEffect } from "react";
import SideBar from '../components/Sidebar';
import ViewProject from '../components/ViewProject/ViewProject.js';
import Header from '../components/Header/Header.js'


function ViewProjectPage( {projectId}) {
const projectName = "Learning Skills";
const [isSideNavOpen, setSideNavOpen] = useState(false);

  return (
    
    <div className={`home-wrapper ${isSideNavOpen ? 'side-nav-open' : ''}`}>
<Header title={"Project " + projectName}/>
    <SideBar />
    <ViewProject/>
  </div>
   
  );
}

export default ViewProjectPage;

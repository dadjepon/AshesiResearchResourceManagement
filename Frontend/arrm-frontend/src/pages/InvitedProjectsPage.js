import React, { useState, useEffect } from "react";
import SideBar from '../components/Sidebar';
import InvitedProjects from '../components/InvitedProjects.js';
import Header from '../components/Header/Header.js'


function InvitedProjectsPage() {

  return (
    //include header
    <div className={`home-wrapper side-nav-open`}>
<Header title={"Invited Projects"}/>
    <SideBar />
    <InvitedProjects />
  </div>
   
  );
}

export default InvitedProjectsPage;

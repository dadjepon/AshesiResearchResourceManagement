import React, { useState, useEffect } from "react";
import SideBar from '../components/Sidebar';
import UserProfile from '../components/UserProfile/UserProfile.js';
import Header from '../components/Header/Header.js'


function UserProfilePage( {}) {
const userName = "Bright Sithole";
const [isSideNavOpen, setSideNavOpen] = useState(false);

  return (
    
    <div className={`home-wrapper ${isSideNavOpen ? 'side-nav-open' : ''}`}>
<Header title={"Profile " + userName}/>
    <SideBar />
    <UserProfile/>
  </div>
   
  );
}

export default UserProfilePage;

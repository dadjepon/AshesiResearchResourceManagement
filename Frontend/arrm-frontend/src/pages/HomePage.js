import React, { useState, useEffect } from "react";
import Sidebar from '../components/Sidebar';
import MainContent from '../components/MainContent.js';
import "../styles/HomePage.css";
import Header from '../components/Header/Header.js'


function HomePage() {
  const [isSideNavOpen, setSideNavOpen] = useState(false);

  return (
    
    <div className={`home-wrapper ${isSideNavOpen ? 'side-nav-open' : ''}`}>
     <Header title={"Welcome"}/>
    <Sidebar/>
    <MainContent/>
  </div>
   
  );
}

export default HomePage;

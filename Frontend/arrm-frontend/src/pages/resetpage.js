import React from 'react';
import Reset from '../components/reset.js';
import '../styles/reset.css'; // Import your dashboard.css file
import '../styles/backgroundpage.css';


function TheReset() {
  const logo = '/images/AshesiLogo-removebg-preview.png';  
  const logo_2 = '/images/background_image.png';

  return (
    
       <div className="bg-container">
      <div className="left-half bg-gradient-to-r from-red-500 to-white h-screen flex">
      </div>
      <div className="right-half bg-white">
        <img src={logo} alt="Ashesi Logo" className="top-right-image" />
      </div>
      <div className="image-background">
        <img src={logo_2} alt="Big design" className="center-image bigger-image" />
      </div>
        <Reset/>
    </div>

   
  );
  
}

export default TheReset;

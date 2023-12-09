import React from 'react';
import Success from '../components/success.js';
import '../styles/success.css'; // Import your dashboard.css file
import '../styles/backgroundpage.css';


function TheSuccess() {
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
        <Success/>
    </div>

   
  );
  
}

export default TheSuccess;

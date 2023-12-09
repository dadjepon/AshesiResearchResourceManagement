import React from 'react';
import '../styles/backgroundpage.css'; // Import your dashboard.css file

function BackgroundPage() {
  // const logo = '/images/ARRM_logo.png';
  const logo_2 = '/images/background_image.png';

  return (
    <div className="bg-container">
      <div className="left-half bg-gradient-to-r from-red-500 to-white h-screen flex">
        {/* ... (content for left half) ... */}
      </div>
      <div className="right-half bg-white">
        {/* <img src={logo} alt="ARRM Logo" className="top-right-image" /> */}
      </div>
      <div className="image-background">
        <img src={logo_2} alt="Big design" className="center-image bigger-image" />
      </div>
    </div>
  );
}
export default BackgroundPage;


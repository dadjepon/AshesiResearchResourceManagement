import React from 'react';
import '../styles/dashboard.css'; // Import your background.css file

const logo = '/images/ARRM_logo.png';
const logo_2 = '/images/background_image.png';

function Dashboard() {
  return (
    <div className="html-body-root">
      <div className="bg-container">
        <div className="left-half">
          <div className="left-content">
            <h1 className="welcome-text">
              Welcome to <br /><span className="arrm-line-break">ARRM</span>
            </h1>
            <p className="subtitle">
              The perfect toolkit for managing your <br /><span className="research-line-break">research projects.</span>
            </p>
            <div style={{ marginTop: '8px' }}>
              <button className="custom-button">EXPLORE</button>
            </div>
          </div>
        </div>
        <div className="right-half">
          <img src={logo} alt="ARRM Logo" className="top-right-image" />
        </div>
        <div className="image-background">
          <img src={logo_2} alt="Big design" className="center-image" />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;



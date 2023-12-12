import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/background.css'; // Import your background.css file

function Background() {
  const logo = '/images/ARRM_logo.png';
  const logo_2 = '/images/background_image.png';

  return (
    <>
      <div className="bg-container">
        <div className="left-half bg-gradient-to-r from-red-500 to-white h-screen flex">
          <div className="w-full flex flex-col justify-center items-start text-white">
            <h1 className="welcome-text">
              Welcome to <span className="arrm-line-break">ARRM</span>
            </h1>
            <p className="subtitle">
              The perfect toolkit for managing your <span className="research-line-break">research projects.</span>
            </p>
            <div className="mt-8">
              <Link to={"/loginpage"}>
                <button className="custom-button">EXPLORE</button>
              </Link>
            </div>
          </div>
        </div>
        {/* <div className="right-half bg-white">
          <img src={logo} alt="ARRM Logo" className="top-right-image" />
        </div>
        <div className="image-background">
          <img src={logo_2} alt="Big design" className="center-image" />
        </div> */}
      </div>
    </>
  );
}

export default Background;

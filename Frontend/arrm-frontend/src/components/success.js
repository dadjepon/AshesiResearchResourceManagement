import React from "react";
import '../styles/success.css';  // Import your login.css file

function Success() {
  const logo = '/images/ARRM_logo.png'
  const logo2 = '/images/ok.png'
  const userEmail = "richard.quayson@ashesi.edu.gh"; // Replace with the user's email address

  return (
    <div className="container">
      <div className="flex items-center justify-center h-screen">
        <div className="bg-white p-8 rounded-lg shadow-md">
          <div className="flex flex-col items-center relative">
          <p className="success-text">
                Password reset link has been sent to <span className="success-break"> <strong>{userEmail}</strong> Follow the link sent </span>
                to reset your password.
            </p>
            <div className="image-container">
              <img src={logo} alt="ARRM Logo" className="centered-image" />
            </div>
            <div className="image2-container">
              <img src={logo2} alt="Ok Logo" className="centered2-image" />
          </div>
        </div>
      </div>
    </div>
    </div>
  );
}
export default Success;


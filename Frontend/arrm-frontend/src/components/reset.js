import React, { useState } from "react";
import '../styles/reset.css';  // Import your reset.css file

function Reset() {
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const logo = '/images/ARRM_logo.png'
  const userEmail = "richard.quayson@ashesi.edu.gh";

  const handlePasswordChange1 = (e) => {
    setPassword1(e.target.value);
  };

  const handlePasswordChange2 = (e) => {
    setPassword2(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // perform your authentication logic here
    console.log(password1, password2);
  };

  return (
    <div className="container">
      <div className="flex items-center justify-center h-screen">
        <div className="bg-white p-8 rounded-lg shadow-md">
          <div className="flex flex-col items-center relative">
          <p className="reset-text">
                Hi <strong>{userEmail}</strong>, reset your password <span className="reset-break">to gain access to your account.</span>
            </p>
            <div className="image-container">
              <img src={logo} alt="ARRM Logo" className="centered-image" />
            </div>
          </div>
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label htmlFor="password1" className="block text-sm font-medium text-gray-700">
                  New Password
                </label>
                <input
                  id="password1"
                  name="password1"
                  type="password"
                  value={password1}
                  onChange={handlePasswordChange1}
                  autoComplete="current-password"
                  required
                  className="input-field" // Add a class for styling purposes if needed
                  placeholder="Password"
                />
              </div>
              <div>
                <label htmlFor="password2" className="block text-sm font-medium text-gray-700">
                  Confirm Password
                </label>
                <input
                  id="password2"
                  name="password2"
                  type="password"
                  value={password2}
                  onChange={handlePasswordChange2}
                  autoComplete="current-password"
                  required
                  className="input-field" // Add a class for styling purposes if needed
                  placeholder="Confirm Password"
                />
              </div>
            </div>
            <div>
              <button
                type="submit"
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Reset Password
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Reset;

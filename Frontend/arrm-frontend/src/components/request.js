import React, { useState } from "react";
import '../styles/request.css';  // Import your login.css file

function Request() {
  const [email, setEmail] = useState("");
  const logo = '/images/ARRM_logo.png'

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // perform your authentication logic here
    console.log(email);
  };

  return (
    <div className="container">
      <div className="flex items-center justify-center h-screen">
        <div className="bg-white p-8 rounded-lg shadow-md">
          <div className="flex flex-col items-center relative">
          <p className="request-text">
              Please enter the email registered to your account and <span className="request-break">request a password reset.</span>
            </p>
            <div className="image-container">
              <img src={logo} alt="ARRM Logo" className="centered-image" />
            </div>
          </div>
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                  Email
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  value={email}
                  onChange={handleEmailChange}
                  autoComplete="email"
                  required
                  className="input-field" // Add a class for styling purposes if needed
                  placeholder="Email"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Request Reset
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
export default Request;

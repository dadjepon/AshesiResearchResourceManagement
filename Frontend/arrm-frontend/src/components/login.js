import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css"; // Import your login.css file

function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const logo = "/images/ARRM_logo.png";

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    // perform your authentication logic here
    const formData = new FormData(event.target);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/account/login/", {
        method: "POST",
        body: formData,
      }); 

      if (response.ok) {
        const responseData = await response.json();

        // store the tokens as cookies
        document.cookie = `access_token=${responseData.access}`;
        document.cookie = `refresh_token=${responseData.refresh}`;

        navigate("/home", { replace: true });
      } else {
        if (response.status === 401) {
          // handle unauthorized error
          console.log("UNAUTHORIZED");
        }
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="container smaller-container">
      <div className="flex items-center justify-center h-screen">
        <div className="bg-white p-8 rounded-lg shadow-md">
          <div className="flex flex-col items-center relative">
            <div className="image-container">
              <img src={logo} alt="ARRM Logo" className="centered-image" />
            </div>
          </div>
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-gray-700"
                >
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
                  className="w-40 h-10 border border-gray-300 rounded-md pl-2" // Tailwind classes for width, height, borders, etc.
                  placeholder="Email"
                />
              </div>
              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-gray-700"
                >
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  value={password}
                  onChange={handlePasswordChange}
                  autoComplete="current-password"
                  required
                  className="input-field" // Add a class for styling purposes if needed
                  placeholder="Password"
                />
              </div>
            </div>

            <div className="forgot-password">
              {/* eslint-disable-next-line jsx-a11y/anchor-is-valid */}
              <a
                href="#"
                className="font-medium text-indigo-600 hover:text-indigo-500"
              >
                Forgot password?
              </a>
            </div>

            <div>
              <button
                type="submit"
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Sign in
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;

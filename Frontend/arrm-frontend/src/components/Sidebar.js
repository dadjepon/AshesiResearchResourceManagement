import React, { useState, useEffect } from "react";
import "../styles/SideNavBar.css";
import { SidebarData } from "./SidebarData";
import { Link } from "react-router-dom";

function Sidebar() {
  const [isExpanded, setExpandedState] = useState(false);
  const forward = "/icons/forward_arrow.png";
  const back = "/icons/back_arrow.png";
  const userName = "Bright Sithole";
  const logo = "/icons/arrm_logoo.png";
  const [userData, setUserData] = useState({
    userProfilePicture: "",
    userName: "",
  });

  useEffect(() => {
    // Replace this with actual fetch or API call
    setTimeout(() => {
      setUserData({
        userProfilePicture: "icons/user_profile_pic.jpg",
        userName: "Bright Sithole",
      });
    }, 1000); 
  }, []); 

  return (
    <div className={isExpanded ? "sliding-div" : "sliding-div-NX"}>
      
      <div
        className={
          isExpanded
            ? "side-nav-container"
            : "side-nav-container side-nav-container-NX"
        }
      >
        <div className="nav-upper">
          <div className="nav-heading ">
            {isExpanded && (
              <>
                <div className="user-profile">
                  <img
                    src={userData.userProfilePicture}
                    alt="user-profile"
                    className="user-profile-picture"
                  />
                  <p className="user-name">{userData.userName}</p>
                  <hr />
                </div>
              </>
            )}
          </div>
        </div>
        <div>
          {isExpanded && (
            <ul className="SidebarList">
              {SidebarData.map((val, key) => {
                return (
                  <li
                    key={key}
                    className="row"
                    id={window.location.pathname == val.link ? "active" : " "}
                    onClick={() => {
                      window.location.pathname = val.link;
                    }}
                  >
                    <Link to={val.link} id="icon" className="icon-container">
                      <img src={val.icon} alt="icon" />
                    </Link>

                    <div id="title">{val.title}</div>
                  </li>
                );
              })}
            </ul>
          )}

          {!isExpanded && (
            <ul className="SidebarList-compressed">
              {SidebarData.map((val, key) => {
                return (
                  <li
                    key={key}
                    className="row"
                    id={window.location.pathname == val.link ? "active" : " "}
                    onClick={() => {
                      window.location.pathname = val.link;
                    }}
                  >
                    <div id="icon" className="icon-container">
                      <img src={val.icon} alt="icon"></img>
                    </div>
                  </li>
                );
              })}
            </ul>
          )}
        </div>
        <div>
          {isExpanded && (
            <button
              className="arrow back-arrow"
              onClick={() => setExpandedState(!isExpanded)}
            >
              <img src={back} alt="icon" />
            </button>
          )}
        </div>
        <div>
          {!isExpanded && (
            <button
              className="arrow forward-arrow"
              onClick={() => {
                setExpandedState(!isExpanded);
              }}
            >
              <img src={forward} alt="icon" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default Sidebar;

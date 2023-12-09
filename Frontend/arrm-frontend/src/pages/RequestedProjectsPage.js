import React, { useState, useEffect } from "react";
import SideBar from "../components/Sidebar";
import RequestedProjects from "../components/RequestedProjects.js";
import Header from "../components/Header/Header.js";

function RequestedProjectsPage() {
  const [isSideNavOpen, setSideNavOpen] = useState(false);

  return (
    <div className={`home-wrapper side-nav-open`}>
      <Header title={"Requested Projects"} />
      <SideBar
        isOpen={isSideNavOpen}
        toggleSideNav={() => setSideNavOpen(!isSideNavOpen)}
      />
      <RequestedProjects />
    </div>
  );
}

export default RequestedProjectsPage;

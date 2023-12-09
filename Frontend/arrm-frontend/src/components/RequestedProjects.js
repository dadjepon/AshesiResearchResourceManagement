// RequestedProjects.js
import React, { useState } from "react";
import "../styles/RequestedProjects.css";
import Projects from "./Projects";

function RequestedProjects() {
  const [allProjectsData, setProjectsData] = useState([
    {
      projectName: "Berekuso Farming",
      progress: 0,
      status: "Pending",
      statusIndicator: 0,
      pendingTasks: 0,
      isVisible: true,
      description:
        "EcoDrone is an ecological monitoring project, drones with advanced sensors to track ...",
        link:"/view_project",

    },
    {
      projectName: "EcoDrone Tech",
      progress: 100,
      status: "On-going",
      statusIndicator: 1,
      isVisible: true,
      pendingTasks: 4,
      description:
        "EcoDrone is an ecological monitoring project, drones with advanced sensors to track ...",
        link:"/view_project",

    },
    {
      projectName: "Learning Skills",
      progress: 100,
      status: "Completed",
      statusIndicator: 0,
      isVisible: false,
      pendingTasks: 0,
      description:
        "Students find a hard time understanding the concepts; some even forget the content taught over time. How can we change that so all knowledge is preserved and their minds are utilized best?",
        link:"/view_project",

      },
    {
      projectName: "Learning Skills",
      progress: 0,
      status: "Pending",
      statusIndicator: 0,
      isVisible: true,
      pendingTasks: 0,
      description:
        "Students find a hard time understanding the concepts; some even forget the content taught over time. How can we change that so all knowledge is preserved and their minds are utilized best?",
        link:"/view_project",

      },
  ]);

  const handleRevoke = (index) => {
    //remove project from the user's prospecting project list 
    const currProjects = [...allProjectsData];
    currProjects[index].status = "Rejected";
    currProjects[index].statusIndicator = 0;
    setProjectsData(currProjects);
  };

  const handleRequest = (index) => {
    //add Projects to the prospecting project list
    const currProjects = [...allProjectsData];
    currProjects[index].status = "Awaiting";
    currProjects[index].statusIndicator = 0;
    setProjectsData(currProjects);
  };

  allProjectsData.sort((a, b) => {
    const statusOrder = { Pending: 0, Ongoing: 1, Completed: 2 };
    return statusOrder[a.status] - statusOrder[b.status];
  });

  return (
    <>
      <div className="non-expanding"></div>
      <div className="inv-content">
        <div className="project-container">
          {/*  */}
          {allProjectsData.map((project, index) => (
            <div className="req-project-div" key={index}>
              <Projects projectData={project} />
              <span>
                {/* use some indicator to identify which are the user's promising projects */}
                {project.status === "Awaiting" && project.isVisible && (
                  <button
                    className="revoke-button"
                    onClick={() => {
                      console.log("Revoked");
                      handleRevoke(index);
                    }}
                  >
                    Delete Request
                  </button>
                ) } { project.isVisible && project.status !== "Awaiting" && (
                  <button
                    className="request-button"
                    onClick={() => {
                      console.log("Requested");
                      handleRequest(index);
                    }}
                  >
                    Request
                  </button>
                )}
              
              </span>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default RequestedProjects;

import React from "react";
import "../styles/InvitedProjects.css";
import Projects from "./Projects";

function InvitedProjects() {
  const projectData = [
    {
      projectName: "Berekuso Farming",
      progress: 0,
      status: "Pending",
      statusIndicator: 0,
      pendingTasks: 0,
      description:
        "EcoDrone is an ecological monitoring project, drones with advanced sensors to track ...",
        link:"/view_project",

    },
    {
      projectName: "EcoDrone Tech",
      progress: 100,
      status: "Completed",
      statusIndicator: 1,
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
      pendingTasks: 0,
      description:
        "Students find a hard time understanding the concepts; some even forget the content taught over time. How can we change that so all knowledge is preserved and their minds are utilized best?",
        link:"/view_project",

      },
  ];

  projectData.sort((a, b) => {
    const statusOrder = { Pending: 0, Ongoing: 1, Completed: 2 };
    return statusOrder[a.status] - statusOrder[b.status];
  });

  return (
    <>
      <div className="non-expanding"></div>
      <div className="inv-content">
        <div className="project-container">
          {projectData.map((project, index) => (
            <>
              {project.status === "Pending" ? (
                <div className="project-div">
                  <Projects key={index} projectData={project} />
                  <span>
                  <button
                      className="accept-button"
                      onClick={() => {
                        // Call some function to handle this
                        projectData[index].status = "Ongoing";
                      }}
                    >
                      Accept
                    </button>
                    <button
                      className="decline-button"
                      onClick={() => {
                        // Call some function to handle this
                        projectData[index].status = "Rejected";
                      }}
                    
                      
                    >
                      Decline
                    </button>
                  </span>
                </div>
              ) : (
                <div className="project-div">
                  <Projects key={index} projectData={project} />
                </div>
              )}
            </>
          ))}
        </div>
      </div>
    </>
  );
}

export default InvitedProjects;

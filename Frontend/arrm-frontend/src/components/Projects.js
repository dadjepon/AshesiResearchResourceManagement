import React from "react";
import "../styles/Projects.css";
import { Link } from "react-router-dom";


const Projects = ({ projectData }) => {
  const progressIndicator = [
    "/icons/yellow_dot.png",
    "/icons/green_dot.png",
    "/icons/red_dot.png",
  ];

  return (
    <div className="project-task">
      <div className="component">
        <h2>{projectData.projectName}</h2>
        <h2 className="value">{`${projectData.progress}%`}</h2>
      </div>
      <div className="component">
        <h3>Status:</h3>
        <div className="group">
          <img
            src={progressIndicator[projectData.statusIndicator]}
            alt="progress"
          />
          <h3 className="value">{projectData.status}</h3>
        </div>
      </div>
      <div className="component">
        <h3>Pending Tasks:</h3>
        <h3 className="value">{projectData.pendingTasks}</h3>
      </div>
      <div className="component">
        <h3>Description:</h3>
      </div>
      <p className="value">
        {projectData.description.length > 60
          ? `${projectData.description.substring(0, 60)}...`
          : projectData.description}
      </p>
      <Link to={projectData.link}  className="view-btn">  
      <button>View Project</button>
      </Link>
      
    </div>
  );
};

export default Projects;

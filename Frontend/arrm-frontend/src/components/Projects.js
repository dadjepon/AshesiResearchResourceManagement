import React from "react";
import "../styles/Projects.css";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

const Projects = ({ projectData }) => {
  const progressIndicator ={ ongoing:
    "/icons/yellow_dot.png",completed:
    "/icons/green_dot.png",pending:
    "/icons/red_dot.png",}
  ;

  if (projectData === null) {
    console.log(projectData);
    // If projectData is not defined, you can return a placeholder or handle the case accordingly
    return <div>No project data available.</div>;
  }

const HandleClick = (e) => {
  console.log(projectData.projectName);
  let navigate = useNavigate();
  navigate("/project");

}


  return (
    <div className="project-task">
      <div className="component">
        <h2>{projectData.title}</h2>
        <h2 className="value">{`12%`}</h2>
      </div>
      <div className="component">
        <h3>Status:</h3>
        <div className="group">
          <img
            src={progressIndicator[projectData.status]}
            alt="progress"
          />
          <h3 className="value">{projectData.status}</h3>
        </div>
      </div>
      <div className="component">
        <h3>Estimated Project Hours:</h3>
        <h3 className="value">{projectData.estimated_project_hours}</h3>
      </div>
      <div className="component">
        <h3>Description:</h3>
      </div>
      <p className="value">
        {projectData.description && projectData.description.length > 60
          ? `${projectData.description.substring(0, 60)}...`
          : projectData.description}
      </p>
      <Link to={`/view_project/${projectData.id}`}  className="view-btn">  
      <button>View Project</button>
      </Link>
      
    </div>
  );
};

export default Projects;

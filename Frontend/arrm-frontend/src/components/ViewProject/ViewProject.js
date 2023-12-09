import React, { useState } from "react";
import "./ViewProject.css";

const ViewProject = ({ currProjectData }) => {
  const projectData = {
    title: "Learning Skills",
    progress: 0,
    status: "Pending",
    statusIndicator: 0,
    isVisible: true,
    pendingTasks: 0,
    description:
      "Students often face challenges in understanding complex concepts, and some may even forget the content taught over time. In response, our project, 'Learning Skills,' seeks to revolutionize traditional education methods. We acknowledge the diverse learning styles and retention capacities of students and aim to address these through innovative technologies, advanced pedagogy, and data-driven insights. Our mission is to create an inclusive and adaptive learning environment, empowering students with the tools and strategies necessary for in-depth comprehension and long-term retention. Join us on this journey to reshape education for a brighter and more enriching future" +
      "In this dynamic project, we explore novel approaches to knowledge preservation and optimal utilization of students' minds. Through collaborative efforts and cutting-edge solutions, we strive to enhance the learning experience, ensuring that every piece of information is not only understood but also retained for lasting impact. Together, let's pave the way for a transformative educational landscape.",

    start_date: "2023-01-01", // Replace with the actual start date
    end_date: "2023-12-31", // Replace with the actual end date
    assigned_ra: "John Doe", // Replace with the actual assigned RA
    tasks: [
      {
        id: 1, // Replace with the actual task ID
        name: "Task 1",
        description: "Description of Task 1.",
        status: "In Progress",
      },
      {
        id: 2, // Replace with the actual task ID
        name: "Task 2",
        description: "Description of Task 2.",
        status: "Pending",
      },
      // Add more tasks as needed
    ],
  };
  const projectPicture = "icons/ashesi_lab.jpeg"
  const [showFullDescription, setShowFullDescription] = useState(false);
  const [expandedTask, setExpandedTask] = useState(null);

  const toggleDescription = () => {
    setShowFullDescription(!showFullDescription);
  };

  const toggleTaskDetails = (taskId) => {
    setExpandedTask(expandedTask === taskId ? null : taskId);
  };

  return (
    <>
    <div className="non-expanding">
        
        
    </div>
    <div className="view-project-container">
      <div className="upper-container"> 
         <img
                    src={projectPicture}
                    alt="proj-picture"
                    className="proj-picture"
                  />
          <h1 className="view-project-title">{projectData.title}</h1>
      </div>
   
      {/* <h1 className="view-project-title">{projectData.title}</h1> */}
      <div className="view-project-details">
        <div className="detail">
          <span className="view-project-label">Description:</span>{" "}
          {showFullDescription ? (
            <span className="view-project-descr">{projectData.description}</span>
          ) : (
            <span className="view-project-descr">
              {projectData.description.substring(0, 300)}...
              <div className="view-all-link" onClick={toggleDescription}>
                View All
              </div>
            </span>
          )}
        </div>
        <div className="detail-values">
          <span className="view-project-label">Status:</span>{" "}
        
            <span className="view-project-descr">{projectData.status}</span>
       
          <span className="view-project-label">Start Date:</span>{" "}
        
            <span className="view-project-descr">{projectData.start_date}</span>
        
          <span className="view-project-label">End Date:</span>{" "}
        
            <span className="view-project-descr">{projectData.end_date}</span>
        
          <span className="view-project-label">Assigned RA:</span>{" "}
        
            <span className="view-project-descr">{projectData.assigned_ra}</span>
        </div>
        
        <div className="tasks-section">
          <span className="view-project-label">Tasks:</span>{" "}
          {projectData.tasks.map((task) => (
            <div key={task.id} className="task-item">
              <span
                className="task-name"
                onClick={() => toggleTaskDetails(task.id)}
              >
                {task.name}
              </span>
              {expandedTask === task.id && (
                <div className="task-details">
                  <p>{task.description}</p>
                  <p>Status: {task.status}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
    </>
  );
};

export default ViewProject;

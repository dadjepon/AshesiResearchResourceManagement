import React from "react";
import "../styles/MainContent.css";
import { customFetch } from "../authentication/token_middleware.js"
import Projects from "./Projects";

function MainContent() {
  var time = new Date();

  var diffTime = true;
  //retreive project data for recent work

  // const getAllProjectsData = async () => {
  //   try {
  //     const allProjectData = await customFetch (
  //       "http://127.0.0.1:8000/api/project/get/"
  //     );
  //     const projectsData = await allProjectData.json();
  //     return projectsData;
  //   } catch (error) {
  //     console.log(error);
  //   }
  // };

  // const getAllTasksData = async () => {
  //   try {
  //     const allTasksData = await customFetch (
  //       "http://127.0.0.1:8000/api/project/task/get/"
  //     );
  //     const tasksData = await allTasksData.json();
  //     return tasksData;
  //   } catch (error) {
  //     console.log(error);
  //   }
  // };

  const projectsData = getAllProjectsData();
  const tasksData = getAllTasksData();
  // Sample project data
  // const projectsData = [
  //   {
  //     projectName: "Berekuso Farming",
  //     progress: 80,
  //     status: "Ongoing",
  //     statusIndicator: 0,
  //     pendingTasks: 4,
  //     description:
  //       "EcoDrone is an ecological monitoring project, drones with advanced sensors to track ...",
  //       link:"/view_project",
  //   },
  //   {
  //     projectName: "EcoDrone Tech",
  //     progress: 100,
  //     status: "Completed",
  //     statusIndicator: 1,
  //     pendingTasks: 4,
  //     description:
  //       "EcoDrone is an ecological monitoring project, drones with advanced sensors to track ...",
  //       link:"/view_project",

  //   },
  //   {
  //     projectName: "Learning Skills",
  //     progress: 40,
  //     status: "Ongoing",
  //     statusIndicator: 0,
  //     pendingTasks: 2,
  //     description:
  //       "Students find a hard time understanding the concepts; some even forget the content taught over time. How can we change that so all knowledge is preserved and their minds are utilized best?",
  //       link:"/view_project",

  //     },
  //   {
  //     projectName: "Learning Skills",
  //     progress: 40,
  //     status: "Ongoing",
  //     statusIndicator: 0,
  //     pendingTasks: 2,
  //     description:
  //       "Students find a hard time understanding the concepts; some even forget the content taught over time. How can we change that so all knowledge is preserved and their minds are utilized best?",
  //       link:"/view_project",

  //     },
  // ];

  return (
    <>
      <div className="non-expanding"></div>
      <div className="main-content">
        <div className="content">
          <div className="recent-work">
            <h4>Recent Work</h4>
            <div className="project-container">
              {projectsData && Array.isArray(projectsData) ? (
                projectsData.map((project, index) => (
                  <Projects key={index} projectsData={project} />
                ))
              ) : (
                <h4 className="message-box">
                  You do not have any Projects. Go to Browze Project to make
                  requests
                </h4>
              )}
            </div>
          </div>
          {/* -------------PENDING TASKS SECTION--------------- */}
          <div className="pending-task">
            <h4>Pending Tasks</h4>
            <ul className="task-collection">
              {tasksData && Array.isArray(tasksData) ? (
                tasksData.map((val, key) => {
                  if (val.due_date !== time) {
                    time = val.due_date;
                    diffTime = true;
                  } else {
                    diffTime = false;
                  }

                  return (
                    <React.Fragment key={key}>
                      {diffTime && <div className="date">{val.due_date}</div>}

                      <div className="task">
                        <li
                          key={key}
                          className="tab"
                          onClick={() => {
                            // window.location.pathname = val.link;
                          }}
                        >
                          <div className="head">
                            <h3>{val.project}:</h3>
                            <h3 className="heading">{val.name} </h3>
                          </div>

                          <h4>
                            {val.description.length > 60
                              ? `${val.description.substring(0, 60)}...`
                              : val.description}
                          </h4>
                        </li>
                      </div>
                    </React.Fragment>
                  );
                })
              ) : (
                <h4 className="message-box" >No Pending Tasks ! </h4>
              )}
            </ul>
          </div>
        </div>
      </div>
    </>
  );
}

export default MainContent;

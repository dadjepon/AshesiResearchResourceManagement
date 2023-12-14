import React from "react";
import "../styles/MainContent.css";
import Projects from "./Projects";
import { TaskData } from "./TaskData";
import { customFetch } from "../authentication/token_middleware";
import { useNavigate } from "react-router-dom";

function MainContent() {

  const navigate = useNavigate();
  
  function handleUnauthorizedError() {
    // redirect to the login page
    navigate('/loginpage', { replace: true });
  }
  
  // fetch user data from api
  const [userData, setUserData] = React.useState(null);
  const [isLoading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);
 
  console.log(userData)
  React.useEffect(() => {
    async function fetchUserData() {
      try {
        const response = await customFetch('http://127.0.0.1:8000/api/project/get/', {
          method: 'GET'
        });

        if (response.ok) {
          const responseData = await response.json();
          // dump the response payload into the console
          setUserData(responseData);
          console.log(userData)
        } else {
          handleUnauthorizedError();
        }
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    }

    fetchUserData();
  }, []);

  React.useEffect(() => {
    // This useEffect logs the updated userData whenever it changes
    console.log(userData);
  }, [userData]);
  
  var time = "Thursday, Nov 23, 2002";
  var diffTime = true;

  // Sample project data
  const projectData = [
    {
      projectName: "Berekuso Farming",
      progress: 80,
      status: "Ongoing",
      statusIndicator: 0,
      pendingTasks: 4,
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
      progress: 40,
      status: "Ongoing",
      statusIndicator: 0,
      pendingTasks: 2,
      description:
        "Students find a hard time understanding the concepts; some even forget the content taught over time. How can we change that so all knowledge is preserved and their minds are utilized best?",
        link:"/view_project",

      },
    {
      projectName: "Learning Skills",
      progress: 40,
      status: "Ongoing",
      statusIndicator: 0,
      pendingTasks: 2,
      description:
        "Students find a hard time understanding the concepts; some even forget the content taught over time. How can we change that so all knowledge is preserved and their minds are utilized best?",
        link:"/view_project",

      },
  ];

  return (
    <>
      <div className="non-expanding">
        
        
      </div>
      <div className="main-content">
        <div className="content">
          <div className="recent-work">
            <h4>Recent Work</h4>
            <div className="project-container">
              {projectData.map((project, index) => (
                <Projects key={index} projectData={project} />
              ))}
            </div>
          </div>
          <div className="pending-task">
            <h4>Pending Tasks</h4>
            <ul className="task-collection">
              {TaskData.map((val, key) => {
                if (val.date !== time) {
                  time = val.date;
                  diffTime = true;
                } else {
                  diffTime = false;
                }

                return (
                  <React.Fragment key={key}>
                    {diffTime && <div className="date">{val.date}</div>}

                    <div className="task">
                      <li
                        key={key}
                        className="tab"
                        onClick={() => {
                          window.location.pathname = val.link;
                        }}
                      >
                        <div className="head">
                          <h3>{val.projectName}:</h3>
                          <h3 className="heading">{val.taskHeading} </h3>
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
              })}
            </ul>
          </div>
        </div>
      </div>
    </>
  );
}

export default MainContent;
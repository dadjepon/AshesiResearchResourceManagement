import React, { useState } from "react";
import "./ViewProject.css";
import { customFetch } from "../../authentication/token_middleware";
import { useNavigate } from "react-router-dom";
import { Button } from "@mui/material";
import { useParams } from "react-router-dom";
<<<<<<< HEAD
import DisabledByDefaultOutlinedIcon from '@mui/icons-material/DisabledByDefaultOutlined';
import CheckBoxOutlinedIcon from '@mui/icons-material/CheckBoxOutlined';


const ViewProject = () => {

  const navigate = useNavigate();

=======

const ViewProject = () => {

  const navigate = useNavigate();
  
>>>>>>> main
  function handleUnauthorizedError() {
    // redirect to the login page
    navigate('/loginpage', { replace: true });
  }
<<<<<<< HEAD

  const { id } = useParams();
  // fetch user data from api
  const [projectData, setProjectData] = React.useState(null);
  const [projectTeam, setProjectTeam] = React.useState(null);
  const [isLoading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);
=======
  
  const {id} = useParams();
  // fetch user data from api
  const [projectData, setProjectData] = React.useState(null);
  const [isLoading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);
 
  React.useEffect(() => {
    async function fetchUserData() {

      
      try {
        const response = await customFetch(`http://127.0.0.1:8000/api/project/get/${id}/`, {
          method: 'GET'
       
        
        });

console.log(`http://127.0.0.1:8000/api/project/get/${id}`);
        if (response.ok) {
          try {
            const responseData = await response.json();
            setProjectData(responseData);
          } catch (error) {
            console.error('Error parsing JSON:', error);
            const responseData = { errorMessage: "Something went wrong ..." };
            setProjectData(responseData);
          }
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


  
>>>>>>> main
  const projectPicture = "icons/ashesi_lab.jpeg"
  const [showFullDescription, setShowFullDescription] = useState(false);
  const [expandedTask, setExpandedTask] = useState(null);
  const [membershipReq, setMembershipReq] = useState([])


  React.useEffect(() => {

    async function fetchUserData() {


      // ---------------project data----------------
      try {
        const response = await customFetch(`http://127.0.0.1:8000/api/project/get/${id}/`, {
          method: 'GET'


        });

        console.log(`http://127.0.0.1:8000/api/project/get/${id}`);
        if (response.ok) {
          try {
            const responseData = await response.json();
            setProjectData(responseData);
          } catch (error) {
            console.error('Error parsing JSON:', error);
            const responseData = { errorMessage: "Something went wrong ..." };
            setProjectData(responseData);
          }
        } else {
          handleUnauthorizedError();
        }
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
      // ---------------project team data----------------
      const uData = await customFetch(`http://127.0.0.1:8000/api/account/user/`, {
          method: 'GET'
        });
        if (uData.ok) {
          try {
            const responseUserData = await uData.json();
            if (uData.ok) {
              if (responseUserData.role === "ädmin" && responseUserData.role === "faculty") {
                try {
                  const responseTeamData = await customFetch(`http://127.0.0.1:8000/api/project/team/get/${id}/`, {
                    method: 'GET'
                  });

                  if (responseTeamData.ok) {
                    try {
                      const responseTd = await responseTeamData.json();
                      setProjectTeam(responseTd);
                    } catch (error) {
                      console.error('Error parsing JSON:', error);
                      const responseTd = { errorMessage: "Something went wrong ..." };
                      setProjectTeam(responseTd);
                    }
                  } else {
                    handleUnauthorizedError();
                  }
                } catch (error) {
                  setError(error);
                } finally {
                  setLoading(false);
                }
              }
            }
          } catch (error) {
            setError(error);
          }
        }

      // ---------------project team membership request----------------
      try {
        const uData = await customFetch(`http://127.0.0.1:8000/api/account/user/`, {
          method: 'GET'
        });
        if (uData.ok) {
          try {
            const responseUserData = await uData.json();
            if (uData.ok) {
              if (responseUserData.role === "ädmin" && responseUserData.role === "faculty") {
                // User is not authorized, return or handle accordingly

                try {
                  const responseRequests = await customFetch(`http://127.0.0.1:8000/api/project/membership/request/get/${id}/`, {
                    method: 'GET'
                  });

                  if (responseRequests.ok) {
                    try {
                      const responseMembershipRequests = await responseRequests.json();
                      setMembershipReq(responseMembershipRequests);
                    } catch (error) {
                      console.error('Error parsing JSON:', error);
                      const responseMembershipRequests = { errorMessage: "Something went wrong ..." };
                      setMembershipReq(responseMembershipRequests);
                    }
                  }
                } catch (error) {
                  setError(error);
                } finally {
                  setLoading(false);
                }

              }
            }
          } catch (error) {
            console.error('Error parsing JSON:', error);
          }
        } 
      } catch (error) { 
        setError(error);
      } finally {
        setLoading(false);
      }
 }
      fetchUserData();
   
  }, []);



  const handleAccept = (memberId) => {
    // Send API request to accept the member with memberId
    setMembershipReq(membershipReq.filter(member => member.user_id !== memberId));
  };

  const handleReject = (memberId) => {
    // Send API request to reject the member with memberId
    setMembershipReq(membershipReq.filter(member => member.user_id !== memberId));
  };


  const toggleDescription = () => {
    setShowFullDescription(!showFullDescription);
  };

  const toggleTaskDetails = (taskId) => {
    setExpandedTask(expandedTask === taskId ? null : taskId);
  };

  if(projectData === null){ 
    console.log(projectData);
    // If projectData is not defined, you can return a placeholder or handle the case accordingly
    return <div>No project data available.</div>;
  }

  return (
    <>
      <div className="non-expanding">


      </div>
      <div className="view-project-container">

        <span className="project-top-descript">
          <div className="top-imgs-content">
            <img
              src={projectPicture}
              alt="default-proj-picture"
              className="default-proj-picture"
            />
            <h1 className="view-project-title">{projectData.title}</h1>
           
              <span>
                <div className="sml-group-collection">
                <h3 className="descript-label-sml">Status</h3>
                <p className="descript-txt-sml">{projectData.status}</p>
                </div>
                <div className="sml-group-collection">
                  <h3 className="descript-label-sml">Project Hours</h3>
                <p className="descript-txt-sml">{projectData.estimated_project_hours}</p>
                </div>
              </span>
              <span>
                <div className="sml-group-collection">
                <h3 className="descript-label-sml">Start Date</h3>
                <p className="descript-txt-sml">{projectData.start_date}</p>
                </div>
                <div className="sml-group-collection">
                  <h3 className="descript-label-sml">End Date</h3>
                <p className="descript-txt-sml">{projectData.end_date}</p>
                </div>
              </span>
          
          </div>
          <div className="top-descript-detail">
            <h3 className="descript-label">
              Project Description:
            </h3>
            <p className="descript-txt">
              {projectData.description && projectData.description.length > 300 ? (
                <>
                  {projectData.description.substring(0, 300)}...
                  <div className="view-all-link" onClick={toggleDescription}>
                    View All
                  </div>
                </>
              ) : (
                projectData.description
              )}
            </p>
            <h3 className="descript-label">
              Study Areas:
            </h3>
            <p className="descript-txt">
              {projectData.study_areas} 
            </p>
            <h3 className="descript-label">
              Faculty:
            </h3>
            <p className="descript-txt">
              {projectData.user} 
            </p>
            <h3 className="descript-label">
              Project Members:
            </h3>
            <p className="descript-txt">
             {/* projectData.members */}
              Sam Sam Sam Sam Sam
            </p>
            <h3 className="descript-label">
              Project Join Requests:
            </h3>
            <div className="accept-ra-request">
<p className="descript-txt">
             {/* projectData.members */}
              Sam Sam Sam Sam Sam
            </p>
            <Button className="accept-btn"/>
           <Button className="reject-btn"/>
            </div>
            
          </div>

        </span>



        {/* <h1 className="view-project-title">{projectData.title}</h1> */}
        {/* <div className="view-project-details">
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
        </div> */}
      </div>
    </>
  );
};

export default ViewProject;

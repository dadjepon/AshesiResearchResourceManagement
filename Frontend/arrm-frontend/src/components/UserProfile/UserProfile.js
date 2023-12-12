import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import InfoBox from "./InfoBox";
import SchoolIcon from "@mui/icons-material/School";
import axios from "axios";
import "./UserProfile.css";

function UserProfile() {
  const add_pic = "/icons/add_pic.png";
  const [userData, setUserData] = useState({
    userFirstname: "",
    userLastname: "",
    email: "",
    mobile: "",
    nationality: "",
    role: "",
  });

  const [categoryCompletionStatus, setCategoryCompletionStatus] = useState([
    { category: "Add Degree", status: false },
    { category: "Writing Sample", status: false },
    { category: "Update CV", status: false },
    { category: "Add Interest", status: false },
  ]);

  const [activeIndex, setActiveIndex] = useState(0);
  const [userWritingSamples, setUserWritingSamples] = useState([]);
  const [userCVData, setUserCVData] = useState([]);
  const [userDegrees, setUserDegrees] = useState([]);
  const [interestsData, setInterestsData] = useState([]);

  const handlePrevClick = () => {
    setActiveIndex((prevIndex) => Math.max(prevIndex - 1, 0));
  };

  const handleNextClick = () => {
    setActiveIndex((prevIndex) =>
      Math.min(
        prevIndex + 1,
        Math.ceil(categoryCompletionStatus.length / 4) - 1
      )
    );
  };

  useEffect(() => {
    // to be replaced with the API stuff above
    const sample1 = {
      id: 1,
      title: "Into the Middle East War",
      publication_link: "https://example.com/publication1",
      sample: "/icons/doc_example.jpg",
    };
    const sample2 = {
      id: 2,
      title: "Sarafina Exhibition",
      publication_link: "https://example.com/publication2",
      sample: "/icons/doc_example.jpg",
    };

    const writingSamplesData = [sample1, sample2];

    const cvData = {
      bio: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
      profile_picture: "/icons/user_profile_pic.jpg",
      linkedin_url: "https://www.linkedin.com/in/example",
      cv: "/icons/doc_example.jpg",
    };

    const degree1 = {
      id: 1,
      type: "Master's",
      university: "University of XYZ",
      major: "Data Science",
      graduation_year: "2024",
      transcript: "/icons/doc_example.jpg",
    };
    const degree2 = {
      id: 2,
      type: "Bachelor's",
      university: "ABC University",
      major: "Computer Science",
      graduation_year: "2022",
      transcript: "/icons/doc_example.pdf",
    };

    const degreesData = [degree1, degree2];

    const interest1 = {
      id: 1,
      name: "Machine Learning",
      study_area: "Computer Science",
    };
    const interest2 = {
      id: 2,
      name: "Environmental Science",
      study_area: "Environmental Science",
    };
    const raInterest1 = {
      id: 1,
      ra: { user: { firstname: "John", lastname: "Doe" } },
      interest: interest1,
    };

    const intData = [raInterest1];

    setInterestsData(intData);
    setCategoryCompletionStatus((prevStatus) => ({
      ...prevStatus,
      "Add Interest": intData.length > 0,
    }));

    setUserWritingSamples(writingSamplesData);
    setCategoryCompletionStatus((prevStatus) => ({
      ...prevStatus,
      "Writing Sample": writingSamplesData.length > 0,
    }));

    setUserCVData(cvData);
    setCategoryCompletionStatus((prevStatus) => ({
      ...prevStatus,
      "Update CV":
        !!cvData.bio &&
        !!cvData.profile_picture &&
        !!cvData.linkedin_url &&
        !!cvData.cv,
    }));

    setUserDegrees(degreesData);
    setCategoryCompletionStatus((prevStatus) => ({
      ...prevStatus,
      "Add Degree": degreesData.length > 0,
    }));

    setTimeout(() => {
      setUserData({
        userFirstname: "Bright",
        userLastname: "Sithole",
        email: "bsithole@ashesi.edu.gh",
        mobile: "077123456",
        nationality: "Zimbabwean",
        role: "Student",
      });
    }, 1000);
  }, []);

  // Rest of the component remains unchanged

  return (
    <>
      <div className="non-expanding"></div>
<div className="profile-content">
      <div className="upload-info">
        <div className="add-pic">
           <img
          src={userCVData.profile_picture || add_pic}
          alt="add_pic"
          
        />
        </div>
       

            {/* If bio is not added yet */}
            {!userCVData.bio && !interestsData.length && (
            <div className="add-bio">
              <div className="incomplete-category">
                <img src={add_pic} alt="sml-add_pic" className="sml-add-pic" />
                <h3>Tell us about yourself.</h3>
                <Link to={"/modal"}>
                  <button className="add-bio-btn">Add Bio</button>
                </Link>
              </div>
              </div>
            )}

            {/* Otherwise, show bio data */}
            {(userCVData.bio || interestsData.length) && (
              <div className="complete-category">
                <h4 className="category-title">Bio:</h4>
                  <p>{userCVData.bio || "No info here"}</p>
                
                  <h4 className="category-title">Interests:</h4>
                  <p>
                    {interestsData
                      .map((interest) => interest.interest.name)
                      .join(", ") || "No info here"}
                  </p>
                
              </div>
            )}
          
          {/* Display  CV */}
          <span className="user-cv">
            <h4>CV:</h4>
            {userCVData.cv ? (
              <>
                <Link to={userCVData.cv}>
                  <img src="icons/doc_example.jpg" alt="CV Preview" />
                </Link>

                {userCVData.linkedin_url ? (
                  <Link to={userCVData.linkedin_url}>
                    <img src="icons/linkedin_icon.png" alt="LinkedIn" id="linkedin"/>
                  </Link>
                ) : (
                  <p>linkedin url displays here</p>
                )}
              </>
            ) : (
              <p>No CV to display here</p>
            )}
          </span>
        
      </div>
      <h3>Profile Info:</h3>
      <div className="basic-info">
        <span>
          <div className="info-field">
            <h4 className="data-title">Firstname:</h4>{" "}
            <h4 className="data-detail">{userData.userFirstname}</h4>
          </div>
          <div className="info-field">
            <h4 className="data-title">Mobile Number:</h4>{" "}
            <h4 className="data-detail">{userData.mobile}</h4>
          </div>
        </span>
        <span>
          <div className="info-field">
            <h4 className="data-title">Lastname:</h4>{" "}
            <h4 className="data-detail">{userData.userLastname}</h4>
          </div>
          <div className="info-field">
            <h4 className="data-title">Nationality:</h4>{" "}
            <h4 className="data-detail">{userData.nationality}</h4>
          </div>
        </span>
        <span>
          <div className="info-field">
            <h4 className="data-title">Email:</h4>{" "}
            <h4 className="data-detail">{userData.email}</h4>
          </div>
          <div className="info-field">
            <h4 className="data-title">Role:</h4>{" "}
            <h4 className="data-detail">{userData.role}</h4>
          </div>
        </span>
      </div>
      <h3>Degree: </h3>
      <div className="degree">
        {!categoryCompletionStatus["Add Degree"] && (
          <div className="incomplete-category">
            <p>Nothing to show here ...</p>
          </div>
        )}

        {categoryCompletionStatus["Add Degree"] && userDegrees.length > 0 && (
          <>
            {userDegrees.map((degree) => (
              <div className="complete-category">
                <div key={degree.id} className="degree-box">
                  <a href={degree.transcript}>
                    <img
                      src={"icons/doc_example.jpg"}
                      alt={`Preview - ${degree.type}`}
                    />
                  </a>
                  <div className="degree-text-area">
                    <span className="degree-info">
                      <div className="title-data">
                        <h4>Type:</h4>
                        <p>{degree.type}</p>
                      </div>
                      <div className="title-data">
                        <h4>University:</h4>
                        <p>{degree.university}</p>
                      </div>
                    </span>
                    <span className="degree-info">
                      <div className="title-data">
                        <h4>Major:</h4>
                        <p>{degree.major}</p>
                      </div>

                      <div className="title-data">
                        <h4>Graduation Year:</h4>
                        <p>{degree.graduation_year}</p>
                      </div>
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </>
        )}
      </div>
      {/* ------------------------------WRITING SAMPLE LOGIC------------------------------------------- */}
      <h3>Writing Samples: </h3>
      <div className="writing-samples">
        {!categoryCompletionStatus["Writing Sample"] && (
          <div className="incomplete-category">
            <p>Nothing to show here ...</p>
          </div>
        )}

        {categoryCompletionStatus["Writing Sample"] && (
          <>
            {userWritingSamples.map((sample) => (
              <div className="complete-category">
                <div key={sample.id} className="writing-sample-box">
                  <a href={sample.sample}>
                    <img
                      src={"icons/doc_example.jpg"}
                      alt={`Preview - ${sample.title}`}
                    />
                  </a>
                  <span>{sample.title}</span>
                </div>
              </div>
            ))}
          </>
        )}
      </div>
      <h3>Complete your profile: </h3>
      <div className="more-info">
        {/* same here, just pass the values on the categorycompletion only */}
        <InfoBox
          completionStatus={categoryCompletionStatus}
          activeIndex={activeIndex}
          onPrevClick={handlePrevClick}
          onNextClick={handleNextClick}
        />
      </div>
    </div>
    
    </>

    
  );
}

export default UserProfile;

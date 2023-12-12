import React, { useState } from "react";
import SchoolIcon from "@mui/icons-material/School";
import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import WorkIcon from "@mui/icons-material/Work";
import ThumbUpAltIcon from "@mui/icons-material/ThumbUpAlt";
import DescriptionIcon from "@mui/icons-material/Description";

import "./UserProfile.css";
import { colors } from "@mui/material";
import Modal1 from "./modals/modal1";
import Modal2 from "./modals/modal2";
import Modal3 from "./modals/modal3";
import Modal4 from "./modals/modal4";
import Modal5 from "./modals/modal5";

const InfoBox = ({
  completionStatus,
  activeIndex,
  onPrevClick,
  onNextClick,
}) => {
  const data = [
    {
      id: 1,
      icon: <SchoolIcon style={{ fontSize: "1.2rem", color: "#4f5663" }} />,
      descript: "Add a degree programme you have undertaken.",
      button_text: "Add Degree",
      completed: completionStatus["Add Degree"],
    },
    {
      id: 2,
      icon: (
        <DescriptionIcon style={{ fontSize: "1.2rem", color: "#4f5663" }} />
      ),
      descript: "Add a writing sample from previous research works",
      button_text: "Add Sample",
      completed: completionStatus["Writing Sample"],
    },
    {
      id: 3,
      icon: <WorkIcon style={{ fontSize: "1.2rem", color: "#4f5663" }} />,
      descript: "Upload a curriculum vitae on past experiences.",
      button_text: "Update CV",
      completed: completionStatus["Update CV"],
    },
    {
      id: 4,
      icon: <ThumbUpAltIcon style={{ fontSize: "1.2rem", color: "#4f5663" }} />,
      descript: "Add an area of interest.",
      button_text: "Add Interest",
      completed: completionStatus["Add Interest"],
    },
  ];

  const next_arrow = "icons/next_arrow.png";
  const prev_arrow = "icons/prev_arrow.png";

  const [numberCompleted, setNumberCompleted] = useState(0);
  const [selectedModal, setSelectedModal] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleCompletion = (id) => {
    const newData = data.map((item) =>
      item.id === id ? { ...item, completed: true } : item
    );
    setNumberCompleted((prev) => prev + 1);
  };

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };


  const takeUserInput = (key) => {
    switch (key) {
      case 1:
        console.log("the modal4 is opening now");
        setSelectedModal(<Modal4 />
          );
        break;
      case 2:
        console.log("the modal3 is opening now");
        setSelectedModal(<Modal3 />);
        break;
      case 3:
        console.log("the modal1 is opening now");
        setSelectedModal(<Modal1 />);
        break;
      case 4:
        console.log("the modal2 is opening now");
        setSelectedModal(<Modal2 />);
        break;
      default:
        break;
    }
  };

  const startIndex = activeIndex * 4;
  const endIndex = startIndex + 4;
  const currentData = data.slice(startIndex, endIndex);

  return (
    <>
      <h4 className="num-completed">
        {numberCompleted} OF {data.length} COMPLETED
      </h4>
      <div className="info-box">
        <div className="slider-arrow" onClick={onNextClick}>
          <ArrowBackIosIcon style={{ fontSize: "1.2rem", color: "white" }} />
        </div>

        {currentData.map((item, index) => (
          <div key={index} className="individual-box">
            {item.completed ? (
              <>
                <div className="add-info-category completed">{item.icon} </div>
                <p>{item.descript}</p>
                <button onClick={() => takeUserInput(item.id)}>
                  {item.button_text}
                </button>
              </>
            ) : (
              <>
                <div className="add-info-category incomplete">{item.icon} </div>
                <div className="not-completed">
                  <p>You have nothing added so far</p>
                </div>
                <button onClick={() => takeUserInput(item.id)}>
                  {item.button_text}
                </button>
              </>
              // Render a different div when item is not completed
            )}
          </div>
        ))}

        <div className="slider-arrow" onClick={onNextClick}>
          <ArrowForwardIosIcon style={{ fontSize: "1.2rem", color: "white" }} />
        </div>
         {selectedModal && (
        <div className="modal-container">
          {selectedModal}
          {/* Add any modal styling or overlay here */}
        </div>
      )}
      </div>
     
    </>
  );
};

export default InfoBox;

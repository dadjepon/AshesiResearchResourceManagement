import React, { useState } from "react";
import SchoolIcon from "@mui/icons-material/School";
import "./UserProfile.css";

const InfoBox = ({ completionStatus, activeIndex, onPrevClick, onNextClick }) => {
  const data = [
    {
      id: 1,
      icon: <SchoolIcon />,
      descript: "Add another degree programme.",
      button_text: "Add Degree",
      completed: completionStatus["Add Degree"],
    },
    {
      id: 2,
      icon: <SchoolIcon />,
      descript:
        "Including your degree will go a long way in helping us match you!",
      button_text: "Writing Sample",
      completed: completionStatus["Writing Sample"],
    },
    {
      id: 3,
      icon: <SchoolIcon />,
      descript: "Update your curriculum vitae.",
      button_text: "Update CV",
      completed: completionStatus["Update CV"],
    },
    {
      id: 4,
      icon: <SchoolIcon />,
      descript: "Add more writing samples from previous research.",
      button_text: "Add Sample",
      completed: completionStatus["Add Interest"],
    },
  ];

  const next_arrow = "icons/next_arrow.png";
  const prev_arrow = "icons/prev_arrow.png";


  const [numberCompleted, setNumberCompleted] = useState(0);

 

  const handleCompletion = (id) => {
    const newData = data.map((item) =>
      item.id === id ? { ...item, completed: true } : item
    );
    setNumberCompleted((prev) => prev + 1);
  };

  const startIndex = activeIndex * 3;
  const endIndex = startIndex + 3;
  const currentData = data.slice(startIndex, endIndex);

  return (

    <>
     <h4 className="num-completed">
        {numberCompleted} OF {data.length} COMPLETED
      </h4>
      <div className="info-box">
       <div className="slider-arrow" onClick={onPrevClick}>
         <img src={prev_arrow} alt="prev_arrow" className="prev_arrow" />
       </div>

       {currentData.map((item, index) => (
         <div key={index} className="individual-box">
           {item.completed ? (
             <>
               <div className="add-info-category completed">
                 <SchoolIcon />{" "}
               </div>
               <p>{item.descript}</p>
               <button 
               // onClick={handle appearance of modal}
               >
                 {item.button_text}
               </button>
             </>
           ) : (
            <>
            <div className="add-info-category incomplete">
                 <SchoolIcon />{" "}
               </div>
             <div className="not-completed">
               <p>You have nothing added so far</p>
             </div>
             <button className="add-info-category not-completed"
               // onClick={handle appearance of modal}
               >
                 {item.button_text}
               </button>
            </>
             // Render a different div when item is not completed
             
           )}
         </div>
       ))}

       <div className="slider-arrow" onClick={onNextClick}>
   <img src={next_arrow} alt="nxt_arrow" className="nxt_arrow" />
 </div>
     </div>
    </>
   
  );
};

export default InfoBox;

import React, { useState } from "react";
import "../styles/admin_acad.css"; // Import your CSS file

const AdminAcad = () => {
  const [acadYear, setAcadyear] = useState("");
  const handleTypeChange = (e) => {
    setAcadyear(e.target.value);
  };

  const [acadYear2, setAcadyear2] = useState("");
  const handleTypeChange2 = (e) => {
    setAcadyear2(e.target.value);
  };
  const logo_2 = "/images/background_image.png";
  // Add logic as needed for academic year creation and handling

  return (
    <div className="modalContainer">
      <div className="back-container">
        <img src={logo_2} alt="back Logo" className="back-image" />
      </div>
      <form className="form-fields">
        <div className="type-acad-text">Create Academic Year:</div>
        <input
          type="number"
          id="startDate"
          value={acadYear}
          onChange={handleTypeChange}
          placeholder="Start Year"
          className="type-acad-box"
          min="2023" // Set the minimum year
          max="2060" // Set the maximum year
          step="1" // Set the step to 1 (increments of 1)
        />
        <input
          type="number"
          id="startDate2"
          value={acadYear2}
          placeholder="End Year"
          onChange={handleTypeChange2}
          className="type-acad-box2"
          min="2024" // Set the minimum year
          max="2060" // Set the maximum year
          step="1" // Set the step to 1 (increments of 1)
        />
      </form>
      <button className="createButton" type="button">
          Create
        </button>
    </div>
  );
};

export default AdminAcad;

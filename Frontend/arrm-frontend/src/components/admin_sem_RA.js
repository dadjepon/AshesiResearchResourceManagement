import React, { useState } from "react";
import "../styles/admin_sem_RA.css"; // Import your CSS file

const AdminSemRA = () => {
  const [RA, setRA] = useState("");
  const handleTypeChange1 = (e) => {
    setRA(e.target.value);
  };

  const [sem, setSem] = useState("");
  const handleTypeChange2 = (e) => {
    setSem(e.target.value);
  };

  const logo_2 = "/images/background_image.png";
  // Add logic as needed for academic year creation and handling

  return (
    <div className="modalContainer">
      <div className="back-container">
        <img src={logo_2} alt="back Logo" className="back-image" />
      </div>
      <form className="form-fields">
        <div className="type-acad-text">Add RA to Semester:</div>
        <select
          id="RA"
          value={RA}
          onChange={handleTypeChange1}
          className="type-acad-box"
        >
          <option value="">Select Research Assistant</option>
          <option value="1">Ayeyi</option>
          <option value="2">Richard</option>
          <option value="3">Ruvimbo</option>
          <option value="4">Ayo</option>
          <option value="5">Mercy</option>
        </select>

        <select
          id="type"
          value={sem}
          onChange={handleTypeChange2}
          className="type-acad-box2"
        >
          <option value="">Select Semester</option>
          <option value="2024">Summer</option>
          <option value="2024">Spring</option>
          <option value="2024">Fall</option>
        </select>
        <button className="createButtonSemRA" type="button">
          Add RA
        </button>
      </form>
    </div>
  );
};

export default AdminSemRA;

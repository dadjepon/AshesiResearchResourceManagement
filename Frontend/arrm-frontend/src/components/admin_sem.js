import React, { useState } from "react";
import "../styles/admin_sem.css"; // Import your CSS file

const AdminSem = () => {
  const [Year, setYear] = useState("");
  const handleTypeChange1 = (e) => {
    setYear(e.target.value);
  };

  const [sem, setSem] = useState("");
  const handleTypeChange2 = (e) => {
    setSem(e.target.value);
  };

  const [startDate, setStartDate] = useState("");
  const handleTypeChange3 = (e) => {
    setStartDate(e.target.value);
  };

  const [endDate, setEndDate] = useState("");
  const handleTypeChange4 = (e) => {
    setEndDate(e.target.value);
  };

  const logo_2 = "/images/background_image.png";
  // Add logic as needed for academic year creation and handling

  return (
    <div className="modalContainer">
      <div className="back-container">
        <img src={logo_2} alt="back Logo" className="back-image" />
      </div>
      <form className="form-fields">
        <div className="type-acad-text">Create Semester:</div>
        <select
          id="type"
          value={Year}
          onChange={handleTypeChange1}
          className="type-acad-box"
        >
          <option value="">Select Year Number</option>
          <option value="1">2023</option>
          <option value="2">2024</option>
          <option value="3">2025</option>
          <option value="4">2026</option>
          <option value="5">2027</option>
        </select>

        <select
          id="type"
          value={sem}
          onChange={handleTypeChange2}
          className="type-acad-box2"
        >
          <option value="">Select Semester</option>
          <option value="2024">Summer</option>
          <option value="2025">Spring</option>
          <option value="2026">Fall</option>
        </select>

        <input
          type="date"
          id="startDate"
          value={startDate}
          onChange={handleTypeChange3}
          className="type-acad-box3"
        />

        <input
          type="date"
          id="endDate"
          value={endDate}
          onChange={handleTypeChange4}
          className="type-acad-box4"
        />

        <button className="createButtonSem" type="button">
          Create
        </button>
      </form>
    </div>
  );
};

export default AdminSem;

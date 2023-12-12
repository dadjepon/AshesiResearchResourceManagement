import React, { useState, useRef } from 'react';
import "./modal4.css";

const Modal4 = (
  // {isOpen, onClose}
  ) => {
  const [degreeType, setDegreeType] = useState('');
  const [graduationYear, setGraduationYear] = useState('');
  const [major, setMajor] = useState('');
  const [university, setUniversity] = useState('');

  const [file, setFile] = useState(null);
  const fileInputRef = useRef(null);

  
  // if (!isOpen) {
  //   return null;
  // }
  const handleUpload = (e) => {
    setFile(URL.createObjectURL(e.target.files[0]));
  };

  const openFileInput = () => {
    fileInputRef.current.click();
  };

  const logo = '/images/Import pdf.png';

  const handleTypeChange = (e) => {
    setDegreeType(e.target.value);
  };

  const handleYearChange = (e) => {
    setGraduationYear(e.target.value);
  };

  const handleMajorChange = (e) => {
    setMajor(e.target.value);
  };

  const handleUniversityChange = (e) => {
    setUniversity(e.target.value);
  };

 

  const logo_2 = '/images/background_image.png';

  return (
    <div className="modal4-container">
        <div className="back-container">
                <img src={logo_2} alt="back Logo" className="back-image" />
            </div>
      <form className="form-fields">
        <div className="type-text">Type:</div>
        <select id="type" value={degreeType} onChange={handleTypeChange} className="type-box">
            <option value="">Select Degree Type</option>
            <option value="Bachelor's">Bachelor's</option>
            <option value="Master's">Master's</option>
            <option value="Doctorate">Doctorate</option>
        </select>

        <div className="grad-year-text">Graduation Year:</div>
        <input
          type="text"
          id="year"
          value={graduationYear}
          onChange={handleYearChange}
          placeholder="YYYY"
          className="grad-year-box"
        />

        <div className="major-text">Major:</div>
        <input
          type="text"
          id="major"
          value={major}
          onChange={handleMajorChange}
          placeholder="Enter Major"
          className="major-box"
        />

        <div className="university-text">University:</div>
        <input
          type="text"
          id="university"
          value={university}
          onChange={handleUniversityChange}
          placeholder="Enter University"
          className="university-box"
        />

<div className="transcript-rectangle">
        {/* Add the text inside the preview box as a link */}
        <a href="#!" className="upload-transcript-text" onClick={openFileInput}>
          Upload your transcript
        </a>
        {file && <img src={file} alt="Profile" />}
        <img src={logo} alt="pdf Logo" className="pdf-modal4-image" />
      </div>
      <div className="upload-section">
        {/* Hidden file input */}
        <input
          type="file"
          id="fileInput"
          onChange={handleUpload}
          className="upload-input visually-hidden"
          ref={fileInputRef}
        />
        <div className="optional-text">Optional</div>
      </div>
       {/* Button to trigger file input */}
       <button className="upload-modal4-button">
          Add Degree
        </button>
      </form>
    </div>
  );
};

export default Modal4;

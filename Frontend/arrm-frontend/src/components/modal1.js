import React, { useState, useRef } from "react";
import '../styles/modal1.css'; // Import your modal1.css file

function Modal2() {
  const [file, setFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleUpload = (e) => {
    setFile(URL.createObjectURL(e.target.files[0]));
  };

  const openFileInput = () => {
    fileInputRef.current.click();
  };

  const logo = '/images/Camera.png';  
  const logo_2 = '/images/background_image.png';

  return (
    <div className="modal1_container">
      <div className="back-container">
        <img src={logo_2} alt="back Logo" className="back-image" />
      </div>
      <div className="preview-box">
        {/* Add the text inside the preview box as a link */}
        <a href="#!" className="upload-text" onClick={openFileInput}>
          Upload a profile picture
        </a>
        {file && <img src={file} alt="Profile" />}
        <img src={logo} alt="camera Logo" className="cam-image" />
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
        {/* Button to trigger file input */}
        <button className="upload-button">
          Upload
        </button>
      </div>
    </div>
  );
};

export default Modal2;

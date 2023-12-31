import React, { useState, useRef } from "react";
import "./modal1.css";

function Modal1(
  // {isOpen, onClose}
  ) {
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

  const logo = "/images/Import pdf.png";
  const logo_2 = "/images/background_image.png";

  return (
    <div className="modal1_container">
      <div className="back-container">
        <img src={logo_2} alt="back Logo" className="back-image" />
      </div>
      
      <div className="preview-box">
        {/* Add the text inside the preview box as a link */}
        <a href="#!" className="upload-text" onClick={openFileInput}>
          Upload your CV
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
        <button className="upload-button">Upload</button>
      </div>
    </div>
  );
}

export default Modal1;

import React, { useState, useRef } from 'react';
import "./modal5.css";

function Modal5(
  // {isOpen, onClose}
  ){
  const [file, setFile] = useState(null);
  const fileInputRef = useRef(null);

  // if (!isOpen) {
  //   return null;
  // }
  const handleUpload = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setFile(event.target.result);
      };
      reader.readAsDataURL(selectedFile);
    }
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
        {/* Display the uploaded image */}
        {file && <img src={file} alt="Profile" className="uploaded-image" />}
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
        <button className="upload-button" onClick={openFileInput}>
          Upload Image
        </button>
      </div>
    </div>
  );
}

export default Modal5;

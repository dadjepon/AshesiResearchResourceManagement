import React, { useState } from 'react';

const Modal2 = () => {
  // State variables for the form fields
  const [type, setType] = useState('');
  const [year, setYear] = useState('');
  const [major, setMajor] = useState('');
  const [university, setUniversity] = useState('');
  const [transcript, setTranscript] = useState(null);

  // Function to handle the form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Implement your logic to handle the form data
    alert('Form submitted');
  };

  // Function to handle the file input change
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setTranscript(file);
    }
  };

  return (
    <div className="modal2-container">
      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <div className="type-form-field">
            <label htmlFor="type">Type</label>
            <select
              id="type"
              value={type}
              onChange={(e) => setType(e.target.value)}
              required
            >
              <option value="">Select</option>
              <option value="Bachelor">Bachelor</option>
              <option value="Master">Master</option>
              <option value="PhD">PhD</option>
            </select>
          </div>
          <div className="grad-form-field">
            <label htmlFor="year">Graduation Year</label>
            <input
              type="number"
              id="year"
              value={year}
              onChange={(e) => setYear(e.target.value)}
              required
            />
          </div>
          <div className="major-form-field">
            <label htmlFor="major">Major</label>
            <input
              type="text"
              id="major"
              value={major}
              onChange={(e) => setMajor(e.target.value)}
              required
            />
          </div>
          <div className="uni-form-field">
            <label htmlFor="university">University</label>
            <input
              type="text"
              id="university"
              value={university}
              onChange={(e) => setUniversity(e.target.value)}
              required
            />
          </div>
          <div className="trans-form-field">
            <label htmlFor="transcript">Transcript</label>
            <input
              type="file"
              id="transcript"
              accept=".pdf"
              value={transcript}
              onChange={handleFileChange}
            />
          </div>
          <div className="form-field">
            <button type="submit">Add Degree</button>
          </div>
        </form>
      </div>
      <div className="image-container">
        <img src="./degree.png" alt="Degree certificate" />
      </div>
      <div className="button-container">
        <button className="add-degree-button">Add Degree</button>
      </div>
    </div>
  );
};

export default Modal2;







// import React, { useState, useRef } from "react";
// import '../styles/modal2.css'; // Import your modal1.css file

// function Modal2() {
//   const [file, setFile] = useState(null);
//   const fileInputRef = useRef(null);

//   const handleUpload = (e) => {
//     setFile(URL.createObjectURL(e.target.files[0]));
//   };

//   const openFileInput = () => {
//     fileInputRef.current.click();
//   };
//   const logo = '/images/import Pdf.png';
//   const logo_2 = '/images/background_image.png';

//   return (
//     <div className="modal2_container">
//       <div className="back-container">
//         <img src={logo_2} alt="back Logo" className="back-image" />
//       </div>
//       <div className="transcript-box">
//         {/* Add the text inside the preview box as a link */}
//         <a href="#!" className="upload-text" onClick={openFileInput}>
//           Upload your transcript
//         </a>
//         {file && <img src={file} alt="Profile" />}
//         <img src={logo} alt="camera Logo" className="cam-image" />
//       </div>
//       <div className="upload-section">
//         {/* Hidden file input */}
//         <input
//           type="file"
//           id="fileInput"
//           onChange={handleUpload}
//           className="upload-input visually-hidden"
//           ref={fileInputRef}
//         />
//         {/* Button to trigger file input */}
//         <button className="upload-button">
//           Add Degree
//         </button>
//       </div>
//     </div>
//   );
// };

// export default Modal2;

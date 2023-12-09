import React from 'react';
import './Header.css'; // Make sure to import your styles

const Header = ({ title }) => {
  return (
    <header className="header">
      <div className='title-components'>
         <div className='vertical-bar'></div>
        <div className="title">{title}</div>
      </div>
     
        <button className="browse-projects-btn">Browse Projects</button>
    </header>
  );
};

export default Header;

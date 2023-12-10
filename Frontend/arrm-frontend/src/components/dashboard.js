import React from 'react';
import '../styles/dashboard.css';

function Dashboard() {
  return (
    <div className="flex h-screen">
      <div className="w-1/4 bg-custom-nav">
        {/* Vertical red bar */}
      </div>
      <div className="w-3/4 bg-white">
        {/* Content */}
    </div>
    </div>
  );
}

export default Dashboard;


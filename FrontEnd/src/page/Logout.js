import React from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate from react-router-dom

function Logout() {
  const navigate = useNavigate(); // Call useNavigate within the functional component
  
  const handleLogout = () => {
    // Logic for logout, such as clearing session, etc.
    // Then navigate to the desired page
    navigate('/'); // Example: navigate to the login page after logout
  };

  return (
    <p style={{"color": "white"}} onClick={handleLogout}>Logout</p>
  );
}

export default Logout;

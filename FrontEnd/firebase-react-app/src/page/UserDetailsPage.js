import React, { useState, useEffect } from 'react';
import Sidebar from './DashboardComponents/Sidebar'; 
import HeaderBar from './DashboardComponents/HeaderBar'
import '../style.css';
import { Col, Row } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import { useNavigate } from 'react-router-dom';


var result = '';
function UserDetailPage() {
  const [data, setData] = useState([]);
  const [input, handleChange] = useState("");

  useEffect(() => {
    fetch('/data')
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  const fetchData = (value) => {
    result = data.filter(
      (user) => 
        user.name.toLowerCase().includes(value) ||
        user.vehicle_number.toLowerCase().includes(value) ||
        user.email.toLowerCase().includes(value)
      )
  }
  const navigate = useNavigate();
  const handleLogout = () => {
    navigate('/details_add'); 
  };

  
  fetchData(input)
  console.log(input)
  console.log(result)

  

  return (
    <div class="siderbardiv" style={{display: 'flex'}}>
      <HeaderBar />
      <Sidebar />
      <div className="content" style={{ width: '80%', float: 'right', padding: "4.3%", paddingTop: '8%'}}>
        <Row className='mb-4'>
          <Col><p style={{"font-weight":"bold"}}>All Vehicles</p></Col>
          <Col><div style={{"float": "right"}}><Button onClick={handleLogout} variant="primary">Add Details</Button></div></Col>
        </Row>

          <div className="input-wrapper">
            <input
              placeholder="To search..."
              value={input}
              onChange={(e) => handleChange(e.target.value)}
            />
          </div>

        {result.length === 0 ? (
          <p>Loading...</p>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Vehicle Number</th>
                <th>Email</th>
              </tr>
            </thead>
            <tbody>
              {result.map((item, index) => (
                <tr key={index}>
                  <td>{item.name}</td>
                  <td>{item.vehicle_number}</td>
                  <td>{item.email}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
    
  );
}

export default UserDetailPage;
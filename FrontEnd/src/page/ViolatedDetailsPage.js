import React, { useState, useEffect } from 'react';
import Sidebar from './DashboardComponents/Sidebar'; 
import HeaderBar from './DashboardComponents/HeaderBar'
import '../style.css';

var result = '';
function UserDetailPage() {
  const [data, setData] = useState([]);
  const [input, handleChange] = useState("");

  useEffect(() => {
    fetch('/violated')
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  const fetchData = (value) => {
    result = data.filter(
      (user) => 
        user.date.toLowerCase().includes(value) ||
        user.time.toLowerCase().includes(value) ||
        user.vehicle_number.toLowerCase().includes(value) ||
        user.violation_Category.toLowerCase().includes(value)
      )
  }
  
  fetchData(input)
  console.log(input)
  console.log(result)

  

  return (
    <div class="siderbardiv" style={{display: 'flex'}}>
      <HeaderBar />
      <Sidebar />
      <div className="content" style={{ width: '80%', float: 'right', padding: "4.3%", paddingTop: '8%'}}>
      <p style={{"font-weight":"bold"}}>Violated Details</p>

      <div className="input-wrapper">
            <input
              placeholder="To search..."
              value={input}
              onChange={(e) => handleChange(e.target.value)}
            />
          </div>,
        {result.length === 0 ? (
          <p>Loading...</p>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Vehicle Number</th>
                <th>Category</th>
              </tr>
            </thead>
            <tbody>
              {result.map((item, index) => (
                <tr key={index}>
                  <td>{item.date}</td>
                  <td>{item.time}</td>
                  <td>{item.vehicle_number}</td>
                  <td>{item.violation_Category}</td>
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

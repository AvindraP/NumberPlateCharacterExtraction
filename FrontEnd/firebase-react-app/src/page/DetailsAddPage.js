import React, { useState, useEffect } from 'react';
import Sidebar from './DashboardComponents/Sidebar'; 
import HeaderBar from './DashboardComponents/HeaderBar'
import '../style.css';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function UserDetailPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [vehicle_number, setVehicleNum] = useState('');

  const showAlert = (type, message) => {
    if(type === 'success') {
      alert('Success: ' + message);
    } else if(type === 'error') {
      alert('Error: ' + message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/add_detail', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, vehicle_number }),

      });
      console.log(response);

      if (!response.ok) {
        throw new Error('Failed to add vehicle');
      }
      // Handle success
      console.log('vehicle details added successfully');
      setName('');
      setEmail('');
      setVehicleNum('');

      showAlert('success', 'Vehicle details added successfully');
    } catch (error) {
      showAlert('error', 'Invalid vehicle number. Max and Min 4 numericals, Max characters 7');
    }
  };

  return (
    <div class="siderbardiv" style={{display: 'flex'}}>
      <HeaderBar />
      <Sidebar />
      <Form style={{"margin":"10% 0% 0% 5%", "width":"70%"}} onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formBasicName">
          <Form.Label>Name</Form.Label>
          <Form.Control type="text" placeholder="Enter Name" value={name} onChange={(e) => setName(e.target.value)}/>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicVN">
          <Form.Label>Vehicle Number</Form.Label>
          <Form.Control type="text" placeholder="Enter Vehicle Number" value={vehicle_number} onChange={(e) => setVehicleNum(e.target.value)}/>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control type="email" placeholder="Enter email" value={email} onChange={(e) => setEmail(e.target.value)}/>
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </div>
    
  );
}

export default UserDetailPage;
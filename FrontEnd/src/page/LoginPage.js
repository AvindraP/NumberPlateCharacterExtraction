// LoginComponent.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../style.css';


const LoginComponent = () => {

  const [data, setData] = useState([]);  
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('/login')
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (username === data[0].username && password === data[0].password) {
      console.log('Login successful');
      navigate('/user_detail');
    } else {
      console.log(data.uname)
      setError('Invalid username or password');
    }
  };



  return (
    <section className="ftco-section">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-6 col-lg-5">
            <div className="login-wrap p-4 p-md-5">
              <div className="icon d-flex align-items-center justify-content-center">
                <span className="fa fa-user-o"></span>
              </div>
              <h3 className="text-center mb-4">Login</h3>
              <form className="login-form" onSubmit={handleSubmit}>
                <div className="form-group">
                  <input type="text" className="form-control rounded-left" placeholder="Username" required value={username} onChange={(e) => setUsername(e.target.value)} />
                </div>
                <div className="form-group d-flex">
                  <input type="password" className="form-control rounded-left" placeholder="Password" required value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>
                {error && <div className="text-danger">{error}</div>}
                <div className="form-group">
                  <button type="submit" className="btn btn-primary rounded submit p-3 px-5">Get Started</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default LoginComponent;

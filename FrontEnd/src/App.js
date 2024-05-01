import React, {} from "react";
import {BrowserRouter, Routes, Route} from 'react-router-dom';

import LoginPage from "./page/LoginPage";
import UserDetailPage from "./page/UserDetailsPage";
import ViolatedDetailsPage from "./page/ViolatedDetailsPage";
import Dashboard from "./page/Dashboard"

function App() {
  return(
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LoginPage/>} />
          <Route path="/user_detail" element={<UserDetailPage/>}/>
          <Route path="/violated_detail" element={<ViolatedDetailsPage/>}/>
          <Route path="/dashboard" element={<Dashboard/>}/>
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App;
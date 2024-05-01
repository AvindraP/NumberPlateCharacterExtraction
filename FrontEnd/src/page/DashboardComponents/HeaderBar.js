import React from "react";
import { Navbar, Nav } from "react-bootstrap";
import "./myStyles.css";
import Logout from "../Logout";

class HeaderBar extends React.Component {
  render() {
    return (
      <div className="topnav">
      <Navbar fixed="top" expand="lg" variant="dark" className="topnav">
        <Navbar.Brand href="#">
          <div style={{ padding: "1% 0% 0% 3%", }}>SL TRAFFIC MANAGEMENT SYSTEM</div>
        </Navbar.Brand>
        <div className="ml-auto me-5" style={{ marginTop: "1%", fontSize: "1rem" }}>
          <Logout />
        </div>
      </Navbar>
    </div>
    );
  }
}

export default HeaderBar;

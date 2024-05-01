import React from 'react';

import {
  CDBSidebar,
  CDBSidebarContent,
  CDBSidebarFooter,
  CDBSidebarHeader,
  CDBSidebarMenu,
  CDBSidebarMenuItem,
} from 'cdbreact';
import { NavLink } from 'react-router-dom';
import { Link } from 'react-router-dom';

import policeLogo from '../images/police_logo-154x196x0x0x154x196x1660997870.png';

const Sidebar = () => {
  return (
    <div style={{ display: 'flex', height: '90vh', overflow: 'scroll initial', marginTop: '4.3%' }}>
      <CDBSidebar textColor="#fff" backgroundColor="#2b286d">
        <CDBSidebarHeader prefix={<i className="fa fa-bars fa-large"></i>}>
          <a href="/" className="text-decoration-none" style={{ color: 'inherit' }}>
            <img src={policeLogo} alt="Logo" style={{ width: '150px', height: 'auto' }} />
          </a>
        </CDBSidebarHeader>

        <CDBSidebarContent className="sidebar-content">
          <CDBSidebarMenu>
            <NavLink exact to="" activeClassName="activeClicked">
              <Link to="/user_detail">
              <CDBSidebarMenuItem icon="columns">All Vehicles</CDBSidebarMenuItem>
              </Link>
            </NavLink>
            <NavLink exact to="" activeClassName="activeClicked">
              <Link to="/violated_detail">
              <CDBSidebarMenuItem icon="table">Violated Details</CDBSidebarMenuItem>
              </Link>
            </NavLink>
          </CDBSidebarMenu>
        </CDBSidebarContent>

        
      </CDBSidebar>
      
    </div>
  );
};

export default Sidebar;
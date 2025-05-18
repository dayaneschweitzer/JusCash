import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FiLogOut } from 'react-icons/fi'; 
import '../styles/Navbar.css';

const Navbar = ({ onLogout }) => {
  const navigate = useNavigate();

  const logout = () => {
    onLogout();
    navigate('/login');
  };

  return (
    <nav className="navbar-modern">
      <div className="navbar-left">
        <img src="/logo.png" alt="JusCash" className="navbar-logo" />
        <div className="navbar-title-with-icon">
          <img src="/balança.png" alt="Ícone" className="navbar-icon" />
          <h1 className="navbar-title">Publicações</h1>
        </div>

      </div>
      <button className="logout-button" onClick={logout}>
        <FiLogOut size={18} />
        <span>Sair</span>
      </button>
    </nav>
  );
};

export default Navbar;

import React, { useState } from 'react';
import Header from '../Header/Header';
import './Register.css';

const Register = () => {
  const [userName, setUserName] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const register = async (e) => {
    e.preventDefault();
    const res = await fetch(window.location.origin + '/djangoapp/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userName, firstName, lastName, email, password }),
    });
    const json = await res.json();
    if (json.status) {
      sessionStorage.setItem('username', json.userName);
      sessionStorage.setItem('firstname', json.firstName || firstName);
      sessionStorage.setItem('lastname', json.lastName || lastName);
      window.location.href = window.location.origin;
    } else if (json.error === 'Already Registered') {
      alert('User already registered. Please log in.');
    } else {
      alert('Registration failed.');
    }
  };

  return (
    <div>
      <Header />
      <form className="register_container" onSubmit={register}>
        <div className="header">Sign Up</div>
        <div className="inputs">
          <input className="input_field" type="text" placeholder="Username" onChange={(e) => setUserName(e.target.value)} required />
          <input className="input_field" type="text" placeholder="First Name" onChange={(e) => setFirstName(e.target.value)} required />
          <input className="input_field" type="text" placeholder="Last Name" onChange={(e) => setLastName(e.target.value)} required />
          <input className="input_field" type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} required />
          <input className="input_field" type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <div className="submit_panel">
          <button className="submit" type="submit">Register</button>
        </div>
      </form>
    </div>
  );
};

export default Register;

// components/Register.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Register = ({ onRegister }) => {
  const [name, setName]               = useState('');
  const [email, setEmail]             = useState('');
  const [password, setPassword]       = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError]             = useState('');
  const [loading, setLoading]         = useState(false);
  const navigate = useNavigate();

  const validatePassword = () => {
    // A senha deve ter no mínimo 8 caracteres, ao menos uma letra maiúscula,
    // uma minúscula, um número e um caractere especial.
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
    return regex.test(password);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (password !== confirmPassword) {
      setError("A confirmação de senha não corresponde.");
      return;
    }
    if (!validatePassword()) {
      setError("A senha deve ter no mínimo 8 caracteres, uma letra maiúscula, uma letra minúscula, um número e um caractere especial.");
      return;
    }
    setLoading(true);
    try {
      // Substitua pela URL do seu endpoint de cadastro
      const response = await axios.post('http://seu-endpoint-api/register', { name, email, password });
      onRegister(response.data.user);
      navigate('/dashboard');
    } catch (err) {
      console.error(err);
      setError("Ocorreu um erro no cadastro. Verifique se o e-mail já está registrado.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <h2>Cadastro - JusCash</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Seu nome completo:</label>
          <input type="text" id="name" required value={name} onChange={(e) => setName(e.target.value)} />
        </div>
        <div>
          <label htmlFor="email">E-mail:</label>
          <input type="email" id="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>
        <div>
          <label htmlFor="password">Senha:</label>
          <input type="password" id="password" required value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <div>
          <label htmlFor="confirmPassword">Confirme sua senha:</label>
          <input
            type="password"
            id="confirmPassword"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>
        {error && <div className="error">{error}</div>}
        <button type="submit" disabled={loading}>
          {loading ? 'Carregando...' : 'Criar Conta'}
        </button>
      </form>
      <p>
        Já possui uma conta?{' '}
        <span className="link" onClick={() => navigate('/login')}>
          Fazer o login
        </span>
      </p>
    </div>
  );
};

export default Register;

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../services/api'; // usa baseURL configurada com axios

const Login = ({ onLogin }) => {
  const [email, setEmail]       = useState('');
  const [password, setPassword] = useState('');
  const [error, setError]       = useState('');
  const [loading, setLoading]   = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/login', {
        email,
        password
      });

      const { token, user } = response.data;

      const userData = {
        email: user?.email || email,
        name: user?.name || '',
        token: token
      };

      localStorage.setItem('token', token);
      onLogin(userData);
      navigate('/dashboard');

    } catch (err) {
      if (err.response?.status === 401) {
        setError('Credenciais inválidas. Verifique e tente novamente.');
      } else {
        setError('Erro ao conectar com o servidor. Tente mais tarde.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <h2>Login - JusCash</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">E-mail:</label>
          <input
            type="email"
            id="email"
            required
            placeholder="Digite seu e-mail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password">Senha:</label>
          <input
            type="password"
            id="password"
            required
            placeholder="Digite sua senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {error && <div className="error" style={{ color: 'red' }}>{error}</div>}
        <button type="submit" disabled={loading}>
          {loading ? 'Carregando...' : 'Login'}
        </button>
      </form>
      <p>
        Não possui uma conta?{' '}
        <span className="link" onClick={() => navigate('/register')} style={{ color: 'blue', cursor: 'pointer' }}>
          Cadastre-se
        </span>
      </p>
    </div>
  );
};

export default Login;
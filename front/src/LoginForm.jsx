import React from 'react';
import { useForm } from 'react-hook-form';
import * as yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { useNavigate } from 'react-router-dom';

// Esquema de validación
const schema = yup.object().shape({
  email: yup
    .string()
    .email('Correo no válido')
    .required('El correo es obligatorio'),
  password: yup
    .string()
    .required('La contraseña es obligatoria'),
});

const LoginForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    reset,
  } = useForm({
    mode: 'onChange',
    resolver: yupResolver(schema),
  });

  const navigate = useNavigate();

  const onSubmit = async (data) => {
    try {
      const response = await fetch("http://localhost:8000/users/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: data.email,
          password: data.password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(`❌ Error: ${errorData.detail || "Credenciales inválidas"}`);
        return;
      }
      const result = await response.json();
      alert("🎉 Login exitoso");
      localStorage.setItem("token", result.access_token);
      reset();
      navigate("/candle-list");

    } catch (error) {
      console.error("❌ Error de red:", error);
      alert("Error de conexión con el servidor.");
    }
  };

  return (
    <div style={{ maxWidth: '450px', margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h2 style={{ textAlign: 'center', color: '#5a2d82' }}>Iniciar Sesión</h2>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        {/* Correo */}
        <div style={{ marginBottom: '1rem' }}>
          <label>Correo electrónico</label>
          <input
            type="email"
            {...register('email')}
            style={{
              width: '100%',
              padding: '.5rem',
              border: errors.email ? '1px solid red' : '1px solid #ccc',
            }}
          />
          {errors.email && <p style={{ color: 'red' }}>{errors.email.message}</p>}
        </div>

        {/* Contraseña */}
        <div style={{ marginBottom: '1rem' }}>
          <label>Contraseña</label>
          <input
            type="password"
            {...register('password')}
            style={{ width: '100%', padding: '.5rem', border: errors.password ? '1px solid red' : '1px solid #ccc' }}
          />
          {errors.password && <p style={{ color: 'red' }}>{errors.password.message}</p>}
        </div>

        {/* Botón */}
        <button
          type="submit"
          disabled={!isValid}
          style={{
            width: '100%',
            padding: '0.75rem',
            backgroundColor: isValid ? '#5a2d82' : '#ccc',
            color: '#fff',
            border: 'none',
            cursor: isValid ? 'pointer' : 'not-allowed',
            fontWeight: 'bold',
          }}
        >
          Iniciar sesión
        </button>

        {/* Botón para ir a registro */}
        <button
        type="button"
        onClick={() => navigate('/register')}
        style={{
            width: '100%',
            marginTop: '0.5rem',
            padding: '0.75rem',
            backgroundColor: '#fff',
            color: '#5a2d82',
            border: '2px solid #5a2d82',
            cursor: 'pointer',
            fontWeight: 'bold',
        }}
        >
        ¿No tienes cuenta? Registrarse
        </button>

      </form>
    </div>
  );
};

export default LoginForm;

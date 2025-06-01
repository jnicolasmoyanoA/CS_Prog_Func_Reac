import React from 'react';
import { useForm } from 'react-hook-form';
import * as yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';

// Esquema de validación
const schema = yup.object().shape({
  nombre: yup
    .string()
    .required('El nombre es obligatorio')
    .min(2, 'Debe tener al menos 2 caracteres'),
  apellido: yup
    .string()
    .required('El apellido es obligatorio')
    .min(2, 'Debe tener al menos 2 caracteres'),
  edad: yup
    .number()
    .typeError('La edad debe ser un número')
    .required('La edad es obligatoria')
    .min(1, 'Edad no válida')
    .max(120, 'Edad no válida'),
    email: yup
    .string()
    .email('Correo no válido')
    .required('El correo es obligatorio'),
  password: yup
    .string()
    .required('La contraseña es obligatoria')
    .min(6, 'Debe tener mínimo 6 caracteres')
    .matches(/[A-Z]/, 'Debe tener al menos una letra mayúscula')
    .matches(/[a-z]/, 'Debe tener al menos una letra minúscula')
    .matches(/[0-9]/, 'Debe tener al menos un número')
    .matches(/[!@#$%^&*(),.?":{}|<>]/, 'Debe tener al menos un carácter especial'),
  confirmarPassword: yup
    .string()
    .required('Debes confirmar tu contraseña')
    .oneOf([yup.ref('password')], 'Las contraseñas no coinciden'),
});

const ReactiveForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    reset,
  } = useForm({
    mode: 'onChange',
    resolver: yupResolver(schema),
  });

  const onSubmit = (data) => {
    console.log('📝 Registro completo:', data);
    alert('🎉 Registro exitoso');
    reset(); // limpia el formulario
  };

  return (
    <div style={{ maxWidth: '450px', margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h2 style={{ textAlign: 'center', color: '#5a2d82' }}>Registro</h2>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        {/* Nombre */}
        <div style={{ marginBottom: '1rem' }}>
          <label>Nombre</label>
          <input
            type="text"
            {...register('nombre')}
            style={{ width: '100%', padding: '.5rem', border: errors.nombre ? '1px solid red' : '1px solid #ccc' }}
          />
          {errors.nombre && <p style={{ color: 'red' }}>{errors.nombre.message}</p>}
        </div>

        {/* Apellido */}
        <div style={{ marginBottom: '1rem' }}>
          <label>Apellido</label>
          <input
            type="text"
            {...register('apellido')}
            style={{ width: '100%', padding: '.5rem', border: errors.apellido ? '1px solid red' : '1px solid #ccc' }}
          />
          {errors.apellido && <p style={{ color: 'red' }}>{errors.apellido.message}</p>}
        </div>

        {/* Edad */}
        <div style={{ marginBottom: '1rem' }}>
          <label>Edad</label>
          <input
            type="number"
            {...register('edad')}
            style={{ width: '100%', padding: '.5rem', border: errors.edad ? '1px solid red' : '1px solid #ccc' }}
          />
          {errors.edad && <p style={{ color: 'red' }}>{errors.edad.message}</p>}
        </div>

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
            <p style={{ fontSize: '0.85rem', color: '#555', marginTop: '.25rem' }}>
                El correo debe tener un formato válido, como: <strong>ejemplo@correo.com</strong>
            </p>
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

        {/* Confirmar contraseña */}
        <div style={{ marginBottom: '1rem' }}>
          <label>Confirmar contraseña</label>
          <input
            type="password"
            {...register('confirmarPassword')}
            style={{ width: '100%', padding: '.5rem', border: errors.confirmarPassword ? '1px solid red' : '1px solid #ccc' }}
          />
          {errors.confirmarPassword && <p style={{ color: 'red' }}>{errors.confirmarPassword.message}</p>}
        </div>

        {/* Botón de enviar */}
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
          Registrarse
        </button>
      </form>
    </div>
  );
};

export default ReactiveForm;

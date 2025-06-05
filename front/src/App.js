import React from 'react';
import ReactiveForm from './ReactiveForm';
import LoginForm from './LoginForm';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CandleList from './CandleList';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/**" element={<LoginForm />} />
          <Route path="/register" element={<ReactiveForm />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/candle-list" element={<CandleList />} />
          <Route path="/" element={<LoginForm />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;


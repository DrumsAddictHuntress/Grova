import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Form from './components/Form';
import Stats from './components/Stats';
import Reports from './components/Reports';
import './App.css';

function App() {
    return (
        <Router>
            <div className="App">
                <Navbar />
                <main className="main-content">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/form" element={<Form />} />
                        <Route path="/stats" element={<Stats />} />
                        <Route path="/reports" element={<Reports />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
}

export default App;
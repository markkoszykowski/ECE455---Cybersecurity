import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  NavLink
} from 'react-router-dom';
import Login from './components/Login';
import Home from './components/Home';

function App() {
    return (
        <main>
        <Router>
            <Routes>
                <Route path="/" element={<Home></Home>}/>
                <Route path="/login" element={<Login></Login>} />
            </Routes>
        </Router>
        </main>
    )
}

export default App;

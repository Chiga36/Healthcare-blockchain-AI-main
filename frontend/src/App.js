import React, { useState } from "react";
import PatientPortal from "./components/PatientPortal";
import HealthInsights from "./components/HealthInsights";
import "./App.css";

function App() {
  const [language, setLanguage] = useState("en");

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4">
        <h1 className="text-2xl">e-Health Blockchain & AI Platform</h1>
        <select
          className="ml-4 p-1 text-black"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          <option value="en">English</option>
          <option value="es">Spanish</option>
          {/* Placeholder for multilingual support */}
        </select>
      </header>
      <main className="container mx-auto p-4">
        <PatientPortal language={language} />
        <HealthInsights language={language} />
      </main>
    </div>
  );
}

export default App;
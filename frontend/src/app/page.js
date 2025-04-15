'use client';

import { useState } from "react";
import Sidebar from "scenes/global/Sidebar.jsx";
import Dashboard from "scenes/dashboard/index.jsx";
import { CssBaseline } from "@mui/material";

export default function App() {
  const [isSidebar, setIsSidebar] = useState(true);

  return (
    <>
      <CssBaseline />
      <div className="app">
        <Sidebar isSidebar={isSidebar} />
        <main className="content">
          <Dashboard /> 
        </main>
      </div>
    </>
  );
}
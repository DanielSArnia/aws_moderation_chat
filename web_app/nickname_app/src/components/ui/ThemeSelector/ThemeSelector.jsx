// src/components/LegoThemeSelector.jsx
import React from 'react';
import "./ThemeSelector.css"

const ThemeSelector = ({ selectedThemes, onSelectTheme }) => {
  const themes = [
    'LEGO City',
    'Ninjago',
    'Minecraft',
    'Friends',
    'Star Wars',
    'Technic',
  ];

  const handleToggleTheme = (theme) => {
    if (selectedThemes.includes(theme)) {
      onSelectTheme(selectedThemes.filter((t) => t !== theme));
    } else {
      onSelectTheme([...selectedThemes, theme]);
    }
  };

  return (
    <div className="lego-theme-selector">
      <h3>Select LEGO Themes:</h3>
      <div className="theme-buttons">
        {themes.map((theme, index) => (
          <button
            key={index}
            className={`theme-button ${selectedThemes.includes(theme) ? 'selected' : ''}`}
            onClick={() => handleToggleTheme(theme)}
          >
            {theme}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ThemeSelector;

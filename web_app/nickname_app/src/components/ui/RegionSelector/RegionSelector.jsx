import React, { useState } from "react";
import "./RegionSelector.css";

const regions = [
  "Denmark",
  "United States",
  "Canada",
  "United Kingdom",
  "Australia",
  "Germany",
  "France",
  "Japan",
  "South Korea",
];

const RegionSelector = ({selectedRegion, onRegionChange}) => {
  const handleChange = (e) => {
    const newValue = e.target.value;
    onRegionChange(newValue);
  };

  return (
    <div className="region-selector-container">
      <label htmlFor="region" className="region-label">
        Your Region
      </label>
      <select
        id="region"
        value={selectedRegion}
        onChange={handleChange}
        className="region-dropdown"
      >
        {regions.map((region) => (
          <option key={region} value={region}>
            {region}
          </option>
        ))}
      </select>
    </div>
  );
};

export default RegionSelector;
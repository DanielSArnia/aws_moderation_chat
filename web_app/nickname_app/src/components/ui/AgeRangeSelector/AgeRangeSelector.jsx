import React from "react";
import "./AgeRangeSelector.css";

const ageRanges = [
  "3-5 years",
  "6-8 years",
  "9-12 years",
  "13-16 years",
  "17+ years",
];

const AgeRangeSelector = ({ selectedAgeRange, onAgeRangeChange }) => {
  const handleChange = (e) => {
    const newRange = e.target.value;
    onAgeRangeChange(newRange);
  };

  return (
    <div className="age-range-selector-container">
      <label htmlFor="ageRange" className="age-range-label">
        Select Age Range
      </label>
      <select
        id="ageRange"
        value={selectedAgeRange}
        onChange={handleChange}
        className="age-range-dropdown"
      >
        {ageRanges.map((range) => (
          <option key={range} value={range}>
            {range}
          </option>
        ))}
      </select>
    </div>
  );
};

export default AgeRangeSelector;

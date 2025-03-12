import React, { useState } from 'react';
import './PopUp.css'; // Import the CSS for the modal

const Popup = ({ data }) => {
  const [show, setShow] = useState(false); // Modal visibility state

  const handleOpenPopup = () => {
    setShow(true); // Show the modal
  };

  const handleClosePopup = () => {
    setShow(false); // Hide the modal
  };

  // Helper function to safely get a key's value or fallback to string
  const safeGet = (obj, path, defaultValue = "N/A") => {
    const keys = path.split(".");
    let result = obj;
    for (let key of keys) {
      if (result && result[key] !== undefined) {
        result = result[key];
      } else {
        return defaultValue; // Return the default value if the key doesn't exist
      }
    }
    return result;
  };

  const renderScoreCard = (title, score, pass, explanation) => (
    <div className="score-card">
      <h3>{title}</h3>
      <p><strong>Score:</strong> {score}</p>
      <p><strong>Pass:</strong> {pass ? "Yes" : "No"}</p>
      <p><strong>Explanation:</strong> {explanation}</p>
    </div>
  );

  const renderOverallResult = (result) => (
    <div className="overall-result">
      <h3>Overall Result</h3>
      <p><strong>Valid:</strong> {safeGet(result, "valid") ? "Yes" : "No"}</p>
      <p><strong>Confidence:</strong> {safeGet(result, "confidence")}</p>
      <p><strong>Risk Level:</strong> {safeGet(result, "risk_level")}</p>
      <p><strong>Decision Explanation:</strong> {safeGet(result, "decision_explanation")}</p>
    </div>
  );

  return (
    <div>
      <button
        style={{ marginTop: '10px', backgroundColor: "#2196f3", color: "white", padding: "10px 20px", border: "none", borderRadius: "5px" }}
        onClick={handleOpenPopup}
      >
        Show Data
      </button>

      {show && (
        <div className="popup-overlay" onClick={handleClosePopup}>
          <div className="popup-content" onClick={(e) => e.stopPropagation()}>
            <span className="close-btn" onClick={handleClosePopup}>&times;</span>
            <h2>Nickname Analysis</h2>

            {/* Render Inappropriate Content Score */}
            {renderScoreCard(
              "Inappropriate Content",
              safeGet(data, "analysis.inappropriate_content.score"),
              safeGet(data, "analysis.inappropriate_content.pass"),
              safeGet(data, "analysis.inappropriate_content.explanation")
            )}

            {/* Render Personal Information Score */}
            {renderScoreCard(
              "Personal Information",
              safeGet(data, "analysis.personal_information.score"),
              safeGet(data, "analysis.personal_information.pass"),
              safeGet(data, "analysis.personal_information.explanation")
            )}

            {/* Render Brand Alignment Score */}
            {renderScoreCard(
              "Brand Alignment",
              safeGet(data, "analysis.brand_alignment.score"),
              safeGet(data, "analysis.brand_alignment.pass"),
              safeGet(data, "analysis.brand_alignment.explanation")
            )}

            {/* Render Age Appropriate Score */}
            {renderScoreCard(
              "Age Appropriate",
              safeGet(data, "analysis.age_appropriate.score"),
              safeGet(data, "analysis.age_appropriate.pass"),
              safeGet(data, "analysis.age_appropriate.explanation")
            )}

            {/* Render Regional Compliance */}
            {renderScoreCard(
              "Regional Compliance",
              "N/A", // No score for compliance
              safeGet(data, "analysis.regional_compliance.pass"),
              safeGet(data, "analysis.regional_compliance.explanation")
            )}

            {/* Render Overall Result */}
            {renderOverallResult(safeGet(data, "overall_result"))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Popup;

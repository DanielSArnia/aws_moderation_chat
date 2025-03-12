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
      <p><strong>Valid:</strong> {result.valid ? "Yes" : "No"}</p>
      <p><strong>Confidence:</strong> {result.confidence}</p>
      <p><strong>Risk Level:</strong> {result.risk_level}</p>
      <p><strong>Decision Explanation:</strong> {result.decision_explanation}</p>
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
              data.analysis.inappropriate_content.score,
              data.analysis.inappropriate_content.pass,
              data.analysis.inappropriate_content.explanation
            )}

            {/* Render Personal Information Score */}
            {renderScoreCard(
              "Personal Information",
              data.analysis.personal_information.score,
              data.analysis.personal_information.pass,
              data.analysis.personal_information.explanation
            )}

            {/* Render Brand Alignment Score */}
            {renderScoreCard(
              "Brand Alignment",
              data.analysis.brand_alignment.score,
              data.analysis.brand_alignment.pass,
              data.analysis.brand_alignment.explanation
            )}

            {/* Render Age Appropriate Score */}
            {renderScoreCard(
              "Age Appropriate",
              data.analysis.age_appropriate.score,
              data.analysis.age_appropriate.pass,
              data.analysis.age_appropriate.explanation
            )}

            {/* Render Regional Compliance */}
            {renderScoreCard(
              "Regional Compliance",
              "N/A", // No score for compliance
              data.analysis.regional_compliance.pass,
              data.analysis.regional_compliance.explanation
            )}

            {/* Render Overall Result */}
            {renderOverallResult(data.overall_result)}
          </div>
        </div>
      )}
    </div>
  );
};

export default Popup;

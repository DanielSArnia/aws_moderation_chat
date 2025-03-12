// src/components/ui/NicknameList.jsx
import React, { useState } from 'react';
import './GeneratedNicknameList.css'; // import the CSS file

const GeneratedNicknameList = ({ nicknames }) => {
  const [loadingStates, setLoadingStates] = useState({});
  const [validationMessage, setValidationMessage] = useState('');
  const [isValid, setIsValid] = useState(false);

  const checkNickname = async (nickname) => {
    if (nickname.trim()) {
      setLoadingStates((prevState) => ({ ...prevState, [nickname]: true }));
      setValidationMessage('');
      
      try {
        const apiUrl = import.meta.env.VITE_BEDROCK_API_URL + "check-nickname";
        const response = await fetch(apiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem('idToken')
          },
          body: JSON.stringify({ nickname: nickname }),
        });
        if (response.ok) {
          const data = await response.json();
          const processed_data = data['result'];
          console.log(processed_data);
          const responseIsValid = processed_data.overall_result.valid ? 'valid' : 'invalid';
          if (responseIsValid == 'valid') {
            setIsValid(true)
          }
          else {
            setIsValid(false)
          }
          setValidationMessage(`The nickname "${nickname}" is ${responseIsValid}. ${processed_data.overall_result.decision_explanation}`);
        } else {
          const errorData = await response.json();
          setIsValid(false)
          setValidationMessage(errorData['error']);
        }
      } catch (error) {
        console.error('Error:', error);
        setIsValid(false)
        setValidationMessage('Failed to check nickname. Please try again later.');
      } finally {
        setLoadingStates((prevState) => ({ ...prevState, [nickname]: false }));
      }
    } else {
      setIsValid(false)
      setValidationMessage('Please enter a nickname.');
    }
  };

  return (
    <div className="nickname-list-container">
      <h3 className="nickname-list-title">Generated Nicknames</h3>
      {validationMessage && (
        <div className={`validation-message ${isValid ? 'success' : 'error'}`}>
          {validationMessage}
        </div>
      )}
      {nicknames.length === 0 ? (
        <p className="nickname-list-empty">No nicknames generated yet.</p>
      ) : (
        <div className="nickname-list-grid">
          {nicknames.map((nicknameObj, index) => (
            <div
              key={index}
              className={`nickname-card ${
                nicknameObj.passes_validation ? 'valid' : 'invalid'
              }`}
            >
              <div className="nickname-card-header">
                <h4 className="nickname-name">{nicknameObj.nickname}</h4>
                <span
                  className={`nickname-validation ${
                    nicknameObj.passes_validation ? 'valid-badge' : 'invalid-badge'
                  }`}
                >
                  {nicknameObj.passes_validation ? 'Valid' : 'Invalid'}
                </span>
              </div>
              <p className="nickname-info">
                <strong>Inspiration:</strong> {nicknameObj.inspiration}
              </p>
              <p className="nickname-info">
                <strong>LEGO Theme:</strong> {nicknameObj.theme_connection}
              </p>
              <button
                className="choose-button"
                onClick={() => checkNickname(nicknameObj.nickname)}
                disabled={loadingStates[nicknameObj.nickname]}
              >
                {loadingStates[nicknameObj.nickname] ? 'Final checks...' : 'Choose'}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GeneratedNicknameList;

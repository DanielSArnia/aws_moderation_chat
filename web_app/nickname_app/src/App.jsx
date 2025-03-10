import { useState } from 'react';
import './App.css';

function App() {
  const [nickname, setNickname] = useState('');
  const [validationMessage, setValidationMessage] = useState('');
  const [loading, setLoading] = useState(false);

  // Function to check nickname validity
  const checkNickname = async () => {
    if (nickname.trim()) {
      setLoading(true);
      setValidationMessage('');
      
      try {
        // Replace with your API endpoint
        // const apiUrl = process.env.REACT_APP_BEDROCK_API_URL;
        // const apiUrl = 'https://0m9vm2cd24.execute-api.eu-west-1.amazonaws.com/prod/check-nickname'; // Use your actual API Gateway URL here
        const apiUrl = 'https://80oxzpkz64.execute-api.eu-west-1.amazonaws.com/prod/check-nickname'; // Use your actual API Gateway URL here
        const response = await fetch(apiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ nickname: nickname }),
        });
        if (response.ok) {
          const data = await response.json();
          const processed_data = JSON.parse(data['result'])
          // Display the response from Lambda that checks validity
          const isValid = processed_data.overall_result.valid ? 'valid' : 'invalid';
          setValidationMessage(`The nickname "${nickname}" is ${isValid}. ${processed_data.overall_result.decision_explanation}`);
        } else {
          const errorData = await response.json();
          setValidationMessage(errorData['error']);
        }
      } catch (error) {
        console.error('Error:', error);
        setValidationMessage('Failed to check nickname. Please try again later.');
      } finally {
        setLoading(false);
      }
    } else {
      setValidationMessage('Please enter a nickname.');
    }
  };

  return (
    <>
      <h1>Nickname Validator</h1>
      <div className="app-container">
        <div className="nickname-checker">
          <input
            type="text"
            value={nickname}
            onChange={(e) => setNickname(e.target.value)}
            placeholder="Enter a nickname"
          />
          <button onClick={checkNickname} disabled={loading}>
            {loading ? 'Checking...' : 'Check Nickname'}
          </button>
        </div>

        {validationMessage && (
          <div className={`validation-message ${validationMessage.includes('invalid') ? 'error' : 'success'}`}>
            {validationMessage}
          </div>
        )}
      </div>
    </>
  );
}

export default App;

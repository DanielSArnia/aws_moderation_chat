import { useState } from 'react';
import Popup from './ui/PopUp/PopUp';

function SimpleSearch() {
  const [nickname, setNickname] = useState('');
  const [validationMessage, setValidationMessage] = useState('');
  const [responseData, setResponseData] = useState({});
  const [isValid, setIsValid] = useState(true);
  const [loading, setLoading] = useState(false);

  // Function to check nickname validity
  const checkNickname = async () => {
    if (nickname.trim()) {
      setLoading(true);
      setValidationMessage('');
      setResponseData({});
      
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
          setResponseData(processed_data);
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
        setLoading(false);
      }
    } else {
      setIsValid(false)
      setValidationMessage('Please enter a nickname.');
    }
  };

  return (
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

      {validationMessage && (
        <>
          <div className={`validation-message ${isValid ? 'success' : 'error'}`}>
            {validationMessage}
          </div>
          <Popup data={responseData} />
        </>
      )}
    </div>
  );
}

export default SimpleSearch;

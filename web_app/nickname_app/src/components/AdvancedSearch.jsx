import { useState } from 'react';

function AdvancedSearch() {
  const [nickname, setNickname] = useState('');
  const [region, setRegion] = useState('');
  const [ageRange, setAgeRange] = useState('');
  const [validationMessage, setValidationMessage] = useState('');
  const [isValid, setIsValid] = useState(true);
  const [loading, setLoading] = useState(false);

  const checkNickname = async () => {
    if (nickname.trim() && region.trim() && ageRange.trim()) {
      setLoading(true);
      setValidationMessage('');
      
      try {
        const apiUrl = import.meta.env.VITE_BEDROCK_API_URL + "check-nickname";
        const response = await fetch(apiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ nickname:nickname, region_code:region, age_range:ageRange }),
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
        setLoading(false);
      }
    } else {
      setIsValid(false)
      setValidationMessage('Please enter all fields: nickname, region, and age range.');
    }
  };

  return (
    <div className="advanced-search">
      <input
        type="text"
        value={nickname}
        onChange={(e) => setNickname(e.target.value)}
        placeholder="Enter a nickname"
      />
      <input
        type="text"
        value={region}
        onChange={(e) => setRegion(e.target.value)}
        placeholder="Enter region"
      />
      <input
        type="text"
        value={ageRange}
        onChange={(e) => setAgeRange(e.target.value)}
        placeholder="Enter age range"
      />
      <button onClick={checkNickname} disabled={loading}>
        {loading ? 'Checking...' : 'Check Nickname'}
      </button>

      {validationMessage && (
        <div className={`validation-message ${isValid ? 'success' : 'error'}`}>
          {validationMessage}
        </div>
      )}
    </div>
  );
}

export default AdvancedSearch;

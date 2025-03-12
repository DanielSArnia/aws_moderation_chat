import { useState } from 'react';
import RegionSelector from './ui/RegionSelector/RegionSelector';
import AgeRangeSelector from './ui/AgeRangeSelector/AgeRangeSelector';

function AdvancedSearch() {
  const [nickname, setNickname] = useState('');
  const [region, setRegion] = useState("Denmark",);
  const [ageRange, setAgeRange] = useState("3-5 years",);
  const [validationMessage, setValidationMessage] = useState('');
  const [isValid, setIsValid] = useState(true);
  const [loading, setLoading] = useState(false);

  const handleRegionChange = (newRegion) => {
    setRegion(newRegion);
    console.log("Selected region:", newRegion); // or do something useful!
  };

  const handleAgeRangeChange = (newRange) => {
    setAgeRange(newRange);
    console.log("Selected age range:", newRange);
  };

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
            'Authorization': localStorage.getItem('idToken')
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
      <AgeRangeSelector
        selectedAgeRange={ageRange}
        onAgeRangeChange={handleAgeRangeChange}
      />
      <RegionSelector
        selectedRegion={region}
        onRegionChange={handleRegionChange}
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

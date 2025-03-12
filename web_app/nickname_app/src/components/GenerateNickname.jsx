import { useState } from 'react';
import RegionSelector from './ui/RegionSelector/RegionSelector';
import AgeRangeSelector from './ui/AgeRangeSelector/AgeRangeSelector';
import ThemeSelector from './ui/ThemeSelector/ThemeSelector';
import GeneratedNicknameList from './ui/GeneratedNicknameList/GeneratedNicknameList';

function GenerateNickname() {
  const [interests, setInterests] = useState('');
  const [region, setRegion] = useState("Denmark",);
  const [selectedThemes, setSelectedThemes] = useState([]);
  const [ageRange, setAgeRange] = useState("3-5 years",);

  const [validationMessage, setValidationMessage] = useState('');
  const [isValid, setIsValid] = useState(true);
  const [loading, setLoading] = useState(false);
  const [generatedNicknames, setGeneratedNicknames] = useState([]);

  const handleRegionChange = (newRegion) => {
    setRegion(newRegion);
    console.log("Selected region:", newRegion); // or do something useful!
  };

  const handleAgeRangeChange = (newRange) => {
    setAgeRange(newRange);
    console.log("Selected age range:", newRange);
  };

  const handleSelectTheme = (themes) => {
    setSelectedThemes(themes);
    console.log("Selected themes:", themes);
  };

  const generateRandomNickname = async () => {
    if (interests.trim() && region.trim() && ageRange.trim()) {
      setLoading(true);
      setValidationMessage('');
      
      try {
        const apiUrl = import.meta.env.VITE_BEDROCK_API_URL + "generate-nickname";
        const response = await fetch(apiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem('idToken')
          },
          body: JSON.stringify({ 
            interests:interests, 
            region_code:region, 
            age_range:ageRange,
            themes:selectedThemes
          }),
        });
        if (response.ok) {
          const data = await response.json();
          const processed_data = data['result'];
          console.log(processed_data);
          setGeneratedNicknames(processed_data)
          // const responseIsValid = processed_data.overall_result.valid ? 'valid' : 'invalid';
          // if (responseIsValid == 'valid') {
          //   setIsValid(true)
          // }
          // else {
          //   setIsValid(false)
          // }
          // setValidationMessage(`The nickname "${nickname}" is ${responseIsValid}. ${processed_data.overall_result.decision_explanation}`);
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
      setValidationMessage('Please enter all fields: interests, region, and age range.');
    }
  };

  return (
    <div className="advanced-search">
      <input
        type="text"
        value={interests}
        onChange={(e) => setInterests(e.target.value)}
        placeholder="Enter your interests, e.g. robots, dinosaur, adventure, dolls"
      />
      <AgeRangeSelector
        selectedAgeRange={ageRange}
        onAgeRangeChange={handleAgeRangeChange}
      />
      <ThemeSelector 
        selectedThemes={selectedThemes}
        onSelectTheme={handleSelectTheme} 
      />

      <RegionSelector
        selectedRegion={region}
        onRegionChange={handleRegionChange}
      />
      <button onClick={generateRandomNickname} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Nicknames'}
      </button>

      {generatedNicknames?.length > 0 && (
        <GeneratedNicknameList nicknames={generatedNicknames} />
      )}
      {validationMessage && (
        <div className={`validation-message ${isValid ? 'success' : 'error'}`}>
          {validationMessage}
        </div>
      )}
    </div>
  );
}

export default GenerateNickname;
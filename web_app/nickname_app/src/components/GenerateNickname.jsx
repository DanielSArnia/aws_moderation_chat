import { useState } from 'react';

function GenerateNickname() {
  const [generatedNickname, setGeneratedNickname] = useState('');

  const generateRandomNickname = () => {
    const randomAdjectives = ['Cool', 'Smart', 'Awesome', 'Mighty', 'Speedy'];
    const randomNouns = ['Tiger', 'Lion', 'Eagle', 'Shark', 'Dragon'];
    const randomAdjective = randomAdjectives[Math.floor(Math.random() * randomAdjectives.length)];
    const randomNoun = randomNouns[Math.floor(Math.random() * randomNouns.length)];
    setGeneratedNickname(`${randomAdjective}${randomNoun}${Math.floor(Math.random() * 100)}`);
  };

  return (
    <div className="generate-nickname">
      <button onClick={generateRandomNickname}>Generate Nickname</button>
      {generatedNickname && (
        <div className="generated-nickname">
          <strong>Generated Nickname: </strong>{generatedNickname}
        </div>
      )}
    </div>
  );
}

export default GenerateNickname;

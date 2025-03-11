// src/components/ui/NicknameList.jsx
import React from 'react';

const GeneratedNicknameList = ({ nicknames }) => {
  return (
    <div className="nickname-list">
      <h3>Generated Nicknames</h3>
      {nicknames.length === 0 ? (
        <p>No nicknames generated yet.</p>
      ) : (
        <ul>
          {nicknames.map((nickname, index) => (
            <li key={index} className={nickname.passes_validation ? 'valid' : 'invalid'}>
              <strong>{nickname.nickname}</strong> - {nickname.passes_validation ? 'Valid' : 'Invalid'}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default GeneratedNicknameList;

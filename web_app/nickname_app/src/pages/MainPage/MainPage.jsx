import React, { useState } from 'react';
import SimpleSearch from '../../components/SimpleSearch';
import AdvancedSearch from '../../components/AdvancedSearch';
import GenerateNickname from '../../components/GenerateNickname';

const MainPage = () => {
  const [activeTab, setActiveTab] = useState('generate'); // Track active tab

  return (
    <>
      <div className="tabs">
        <button
          className={activeTab === 'simple' ? 'active' : ''}
          onClick={() => setActiveTab('simple')}
        >
          Simple Validation
        </button>
        <button
          className={activeTab === 'advanced' ? 'active' : ''}
          onClick={() => setActiveTab('advanced')}
        >
          Advanced Validation
        </button>
        <button
          className={activeTab === 'generate' ? 'active' : ''}
          onClick={() => setActiveTab('generate')}
        >
          Generate Nickname
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'simple' && <SimpleSearch />}
        {activeTab === 'advanced' && <AdvancedSearch />}
        {activeTab === 'generate' && <GenerateNickname />}
      </div>
    </>
  );
};

export default MainPage;

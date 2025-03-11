import { useState } from 'react';
import './App.css';
import SimpleSearch from './components/SimpleSearch';
import AdvancedSearch from './components/AdvancedSearch';
import GenerateNickname from './components/GenerateNickname';

function App() {
  const [activeTab, setActiveTab] = useState('simple'); // Track active tab

  return (
    <>
      <h1>Nickname Validator</h1>
      <div className="tabs">
        <button
          className={activeTab === 'simple' ? 'active' : ''}
          onClick={() => setActiveTab('simple')}
        >
          Simple Search
        </button>
        <button
          className={activeTab === 'advanced' ? 'active' : ''}
          onClick={() => setActiveTab('advanced')}
        >
          Advanced Search
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
}

export default App;

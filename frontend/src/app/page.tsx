'use client';

import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('Overview');
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([
    { role: 'ai', content: 'Hello! 🌿 I am your ELITE HR Co-pilot. How can I help you today?' }
  ]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!query.trim()) return;
    
    const userMsg = { role: 'user', content: query };
    setMessages(prev => [...prev, userMsg]);
    setQuery('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'ai', content: data.response }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', content: 'Oh no! I lost my connection for a moment. Please check the backend. 🌿' }]);
    } finally {
      setLoading(false);
    }
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'Overview':
        return (
          <>
            <section className="metrics-grid">
              <div className="glass-card metric-card">
                <h3>Active Workforce</h3>
                <div className="value">42</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--success)', marginTop: '0.5rem' }}>+2 this month</div>
              </div>
              <div className="glass-card metric-card">
                <h3>Compliance Risks</h3>
                <div className="value" style={{ color: 'var(--danger)' }}>08</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--danger)', marginTop: '0.5rem' }}>3 critical alerts</div>
              </div>
              <div className="glass-card metric-card">
                <h3>Avg Productivity</h3>
                <div className="value">8.4<span style={{ fontSize: '1rem', fontWeight: 500 }}>h</span></div>
                <div style={{ fontSize: '0.8rem', color: 'var(--success)', marginTop: '0.5rem' }}>Above benchmark</div>
              </div>
              <div className="glass-card metric-card">
                <h3>Identity Health</h3>
                <div className="value">96<span style={{ fontSize: '1rem', fontWeight: 500 }}>%</span></div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginTop: '0.5rem' }}>MFA Enrolled</div>
              </div>
            </section>

            <section style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '2rem' }}>
              <div className="glass-card">
                <h2 style={{ marginBottom: '1.5rem', fontSize: '1.3rem' }}>Wazuh Security Intelligence 🛡️</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: 'var(--bg)', borderRadius: '1.5rem' }}>
                    <div>
                      <div style={{ fontWeight: 600 }}>Orphaned Account: Priya Harris</div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>Offboarded but Keycloak active</div>
                    </div>
                    <span className="badge critical">Critical</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: 'var(--bg)', borderRadius: '1.5rem' }}>
                    <div>
                      <div style={{ fontWeight: 600 }}>MFA Gap: Kiran Verma</div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>Keycloak policy violation</div>
                    </div>
                    <span className="badge warning">Warning</span>
                  </div>
                </div>
              </div>
              <div className="glass-card">
                <h2 style={{ marginBottom: '1.5rem', fontSize: '1.3rem' }}>Attrition Analytics 📊</h2>
                <div style={{ height: '150px', display: 'flex', alignItems: 'flex-end', gap: '1.5rem', paddingBottom: '1rem' }}>
                  <div style={{ flex: 1, height: '40%', background: 'var(--accent)', opacity: 0.3, borderRadius: '1rem' }}></div>
                  <div style={{ flex: 1, height: '60%', background: 'var(--accent)', opacity: 0.5, borderRadius: '1rem' }}></div>
                  <div style={{ flex: 1, height: '80%', background: 'var(--accent)', borderRadius: '1rem' }}></div>
                  <div style={{ flex: 1, height: '30%', background: 'var(--accent)', opacity: 0.2, borderRadius: '1rem' }}></div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-dim)' }}>
                  <span>Q1</span><span>Q2</span><span>Q3</span><span>Q4</span>
                </div>
              </div>
            </section>
          </>
        );
      case 'Analytics':
        return (
          <div className="glass-card" style={{ height: '500px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '4rem' }}>📊</div>
              <h2 style={{ marginTop: '1rem' }}>Detailed Workforce Analytics</h2>
              <p style={{ color: 'var(--text-dim)' }}>Connecting to live PowerBI / Excel data...</p>
            </div>
          </div>
        );
      case 'Wazuh XDR':
        return (
          <div className="glass-card" style={{ height: '500px' }}>
            <h2 style={{ marginBottom: '1.5rem' }}>Wazuh Cloud Intelligence Feed</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {[1, 2, 3, 4, 5].map(i => (
                <div key={i} style={{ padding: '1rem', background: 'var(--bg)', borderRadius: '1.5rem', borderLeft: '4px solid var(--accent)' }}>
                  <div style={{ fontWeight: 600 }}>Security Event #{i * 1234}</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>Endpoint: LAPTOP-IN-{1000 + i} | Source: Wazuh Agent</div>
                </div>
              ))}
            </div>
          </div>
        );
      case 'Keycloak IAM':
        return (
          <div className="glass-card" style={{ height: '500px' }}>
            <h2 style={{ marginBottom: '1.5rem' }}>Keycloak Identity Directory</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem' }}>
              {['Active Sessions', 'MFA Compliance', 'Group Sync', 'Orphaned Sweep'].map(service => (
                <div key={service} style={{ padding: '2rem', background: 'var(--accent-soft)', borderRadius: '2rem', textAlign: 'center' }}>
                  <div style={{ fontWeight: 600 }}>{service}</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--success)', fontWeight: 700 }}>OPERATIONAL</div>
                </div>
              ))}
            </div>
          </div>
        );
      case 'Settings':
        return (
          <div className="glass-card" style={{ maxWidth: '600px' }}>
            <h2 style={{ marginBottom: '2rem' }}>Platform Settings</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '0.5rem', fontWeight: 600 }}>OpenAI API Key</label>
                <input type="password" value="••••••••••••••••" readOnly style={{ width: '100%' }} />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '0.5rem', fontWeight: 600 }}>Wazuh Cloud ID</label>
                <input type="text" value="wazuh-cloud-production-01" readOnly style={{ width: '100%' }} />
              </div>
              <button className="primary" style={{ marginTop: '1rem' }}>Save Changes</button>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="dashboard-container">
      <aside>
        <div className="logo" style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent)', marginBottom: '1rem' }}>
          ELITE HR 🌿
        </div>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {['Overview', 'Analytics', 'Wazuh XDR', 'Keycloak IAM', 'Settings'].map(tab => (
            <div 
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{ 
                cursor: 'pointer',
                padding: '0.75rem 1.5rem', 
                borderRadius: '1.5rem',
                fontWeight: 600,
                transition: 'var(--transition-smooth)',
                background: activeTab === tab ? 'var(--accent-soft)' : 'transparent',
                color: activeTab === tab ? 'var(--accent)' : 'var(--text-dim)'
              }}
            >
              {tab}
            </div>
          ))}
        </nav>
        
        <div style={{ marginTop: 'auto', padding: '1.5rem', background: 'var(--bg)', borderRadius: '2rem' }}>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '0.5rem' }}>Stack Status</div>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '0.7rem', background: '#e8f0e8', color: '#88b088', padding: '0.2rem 0.5rem', borderRadius: '0.5rem' }}>Wazuh OK</span>
            <span style={{ fontSize: '0.7rem', background: '#e8f0e8', color: '#88b088', padding: '0.2rem 0.5rem', borderRadius: '0.5rem' }}>Keycloak OK</span>
          </div>
        </div>
      </aside>

      <main>
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <div>
            <h1>{activeTab === 'Overview' ? 'Good morning! ☕' : activeTab}</h1>
            <p style={{ color: 'var(--text-dim)' }}>
              {activeTab === 'Overview' ? "Here is what's happening in your HR platform today." : `Managing your ${activeTab} configurations.`}
            </p>
          </div>
          <div className="user-profile" style={{ display: 'flex', alignItems: 'center', gap: '1rem', background: 'var(--surface)', padding: '0.75rem 1.5rem', borderRadius: '2rem', boxShadow: 'var(--shadow)' }}>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontWeight: 600, fontSize: '1rem' }}>Naman</div>
              <div style={{ fontSize: '0.8rem', opacity: 0.6 }}>Global HR Director</div>
            </div>
            <div style={{ width: 50, height: 50, borderRadius: '1.5rem', background: 'var(--accent-soft)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.2rem' }}>👤</div>
          </div>
        </header>

        {renderContent()}

        <div className="ai-panel glass-card">
          <div className="chat-header">
            <span>🌿</span> ELITE HR Co-pilot
          </div>
          <div className="chat-messages">
            {messages.map((m, i) => (
              <div key={i} className={`message ${m.role}`}>
                {m.content}
              </div>
            ))}
            {loading && <div className="message ai">Thinking... 🌿</div>}
          </div>
          <div className="input-area">
            <input 
              value={query} 
              onChange={e => setQuery(e.target.value)} 
              onKeyDown={e => e.key === 'Enter' && handleSend()}
              placeholder="Ask me anything..."
            />
            <button className="primary" onClick={handleSend}>Send</button>
          </div>
        </div>
      </main>
    </div>
  );
}

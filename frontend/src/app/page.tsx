'use client';

import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('Overview');
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([
    { role: 'ai', content: 'Hello! 🌿 I am your ELITE HR Co-pilot. How can I help you today?' }
  ]);
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadStatus('Uploading... 🌿');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setUploadStatus(data.status || 'Upload failed');
      setTimeout(() => setUploadStatus(''), 3000);
    } catch (err) {
      setUploadStatus('Error uploading file');
    }
  };

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
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                  <h2 style={{ fontSize: '1.3rem' }}>Wazuh Security Intelligence 🛡️</h2>
                  <div style={{ fontSize: '0.7rem', color: 'var(--accent)', background: 'var(--accent-soft)', padding: '0.25rem 0.75rem', borderRadius: '1rem' }}>Device Security Monitor</div>
                </div>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-dim)', marginBottom: '1rem' }}>
                  Wazuh monitors all employee laptops for viruses, unauthorized USB usage, and missing security updates. 
                  <span style={{ fontWeight: 600 }}> If you see a Red alert, it means a device is at risk.</span>
                </p>
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
                <h2 style={{ marginBottom: '1rem', fontSize: '1.3rem' }}>Attrition Analytics 📊</h2>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-dim)', marginBottom: '1rem' }}>
                  Tracking employee exits by quarter to help you predict future hiring needs.
                </p>
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
          <div className="glass-card">
            <h2 style={{ marginBottom: '1.5rem' }}>Workforce Performance 📈</h2>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
              <div style={{ background: 'var(--bg)', padding: '2rem', borderRadius: '2rem' }}>
                <h4 style={{ marginBottom: '1rem' }}>Headcount Distribution</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {[
                    { label: 'Engineering', val: 18, color: '#a7c0a7' },
                    { label: 'Sales', val: 12, color: '#e6b38a' },
                    { label: 'Operations', val: 8, color: '#d98888' },
                    { label: 'HR', val: 4, color: '#88b088' }
                  ].map(item => (
                    <div key={item.label}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '0.25rem' }}>
                        <span>{item.label}</span>
                        <span>{item.val} members</span>
                      </div>
                      <div style={{ height: '8px', background: '#eee', borderRadius: '4px' }}>
                        <div style={{ height: '100%', width: `${(item.val / 18) * 100}%`, background: item.color, borderRadius: '4px' }}></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <div style={{ background: 'var(--bg)', padding: '2rem', borderRadius: '2rem' }}>
                <h4 style={{ marginBottom: '1rem' }}>Average Productivity (Monthly)</h4>
                <div style={{ height: '200px', borderLeft: '2px solid var(--border)', borderBottom: '2px solid var(--border)', position: 'relative', display: 'flex', alignItems: 'flex-end', justifyContent: 'space-around', padding: '0 1rem' }}>
                  {[7.2, 8.1, 7.8, 8.4, 8.9, 8.2].map((h, i) => (
                    <div key={i} style={{ width: '20px', height: `${(h / 10) * 100}%`, background: 'var(--accent)', borderRadius: '4px 4px 0 0' }}></div>
                  ))}
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', color: 'var(--text-dim)', marginTop: '0.5rem' }}>
                  <span>Jan</span><span>Feb</span><span>Mar</span><span>Apr</span><span>May</span><span>Jun</span>
                </div>
              </div>
            </div>
          </div>
        );
      case 'Wazuh XDR':
        return (
          <div className="glass-card">
            <div style={{ marginBottom: '2rem' }}>
              <h2 style={{ marginBottom: '0.5rem' }}>Device Compliance Center 🛡️</h2>
              <p style={{ color: 'var(--text-dim)', fontSize: '0.9rem' }}>
                This panel shows the safety status of every employee's computer. 
                <br/><strong>Endpoint:</strong> The name of the laptop.
                <br/><strong>XDR Status:</strong> Green means the security software is active and updated.
              </p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {[
                { name: 'Aditya Taylor', device: 'LAPTOP-IN-1040', risk: 'Safe', color: 'var(--success)' },
                { name: 'Kiran Verma', device: 'LAPTOP-IN-1005', risk: 'MFA Warning', color: 'var(--warning)' },
                { name: 'Priya Harris', device: 'LAPTOP-US-2013', risk: 'Account Orphaned', color: 'var(--danger)' },
                { name: 'Deepa Pillai', device: 'LAPTOP-IN-1045', risk: 'Safe', color: 'var(--success)' }
              ].map(item => (
                <div key={item.name} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1.25rem', background: 'var(--bg)', borderRadius: '1.5rem' }}>
                  <div>
                    <div style={{ fontWeight: 600 }}>{item.name}</div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>{item.device}</div>
                  </div>
                  <div style={{ color: item.color, fontWeight: 700, fontSize: '0.9rem' }}>{item.risk}</div>
                </div>
              ))}
            </div>
          </div>
        );
      case 'Keycloak IAM':
        return (
          <div className="glass-card">
            <div style={{ marginBottom: '2rem' }}>
              <h2 style={{ marginBottom: '0.5rem' }}>Identity & Login Health 🔐</h2>
              <p style={{ color: 'var(--text-dim)', fontSize: '0.9rem' }}>
                Managing how employees log in. We ensure everyone uses Multi-Factor Authentication (MFA) for safety.
                <br/><strong>MFA Compliance:</strong> Percentage of employees who have set up their secondary login code.
              </p>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1.5rem' }}>
              <div style={{ padding: '2rem', background: 'var(--accent-soft)', borderRadius: '2.5rem', textAlign: 'center' }}>
                <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>✅</div>
                <div style={{ fontWeight: 700, fontSize: '1.2rem' }}>96% MFA</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text)' }}>Overall Compliance</div>
              </div>
              <div style={{ padding: '2rem', background: 'var(--bg)', borderRadius: '2.5rem', textAlign: 'center', border: '1px solid var(--border)' }}>
                <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🚨</div>
                <div style={{ fontWeight: 700, fontSize: '1.2rem' }}>2 Orphans</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text)' }}>Pending Revocation</div>
              </div>
            </div>
          </div>
        );
      case 'Settings':
        return (
          <div className="glass-card" style={{ maxWidth: '600px' }}>
            <h2 style={{ marginBottom: '2rem' }}>System Management</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
              <div style={{ background: 'var(--bg)', padding: '1.5rem', borderRadius: '1.5rem' }}>
                <h4 style={{ marginBottom: '1rem' }}>Update HR Master Data</h4>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '1rem' }}>
                  Upload a new `.xlsx` file to update all employee records, finance, and productivity metrics.
                </p>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <label className="primary" style={{ 
                    cursor: 'pointer', 
                    padding: '0.75rem 1.5rem', 
                    background: 'var(--accent)', 
                    color: '#fff', 
                    borderRadius: '1.5rem',
                    fontSize: '0.9rem',
                    fontWeight: 600
                  }}>
                    Browse Files
                    <input type="file" onChange={handleFileUpload} style={{ display: 'none' }} accept=".xlsx" />
                  </label>
                  <span style={{ fontSize: '0.8rem', color: 'var(--accent)' }}>{uploadStatus}</span>
                </div>
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '0.5rem', fontWeight: 600 }}>OpenAI API Key</label>
                <input type="password" value="••••••••••••••••" readOnly style={{ width: '100%' }} />
              </div>
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
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
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
          <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '0.5rem' }}>Quick Upload</div>
          <input 
            type="file" 
            onChange={handleFileUpload} 
            style={{ fontSize: '0.7rem', width: '100%' }} 
            accept=".xlsx"
          />
          {uploadStatus && <div style={{ fontSize: '0.7rem', color: 'var(--accent)', marginTop: '0.5rem' }}>{uploadStatus}</div>}
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

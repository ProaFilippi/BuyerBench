interface Tab {
  id: string;
  label: string;
}

interface PillarTabsProps {
  activeTab: string;
  onChange: (tab: string) => void;
  tabs: Tab[];
}

export default function PillarTabs({ activeTab, onChange, tabs }: PillarTabsProps) {
  return (
    <div style={{ display: 'flex', gap: '0', marginBottom: '1.5rem' }}>
      {tabs.map((tab) => {
        const isActive = tab.id === activeTab;
        return (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            style={{
              padding: '0.6rem 1.2rem',
              fontFamily: 'var(--font-mono)',
              fontSize: '0.78rem',
              fontWeight: 700,
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
              cursor: 'pointer',
              border: 'var(--border)',
              borderRadius: 0,
              marginRight: '-3px', // collapse adjacent borders
              background: isActive ? 'var(--fg)' : 'var(--bg)',
              color: isActive ? 'var(--bg)' : 'var(--fg)',
              position: 'relative',
              zIndex: isActive ? 1 : 0,
            }}
          >
            {tab.label}
          </button>
        );
      })}
    </div>
  );
}

:root {
  --bg: #f4f7fb;
  --panel: #ffffff;
  --ink: #1e293b;
  --muted: #64748b;
  --primary: #1d4ed8;
  --primary-soft: #dbeafe;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --line: #e2e8f0;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: var(--bg);
  color: var(--ink);
}

.container {
  max-width: 1200px;
  margin: 32px auto;
  padding: 0 20px;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 24px;
}

.topbar h1 {
  margin: 0;
  font-size: 1.9rem;
}

.topbar p {
  margin: 8px 0 0;
  color: var(--muted);
}

.badge {
  background: var(--primary-soft);
  color: var(--primary);
  border-radius: 999px;
  padding: 8px 12px;
  font-weight: 700;
}

.summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 18px 20px;
}

.card span {
  display: block;
  color: var(--muted);
  margin-bottom: 6px;
}

.card strong {
  font-size: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 12px;
  overflow: hidden;
}

th, td {
  text-align: left;
  padding: 14px 16px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}

th {
  background: #f8fafc;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--muted);
}

.tag {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 700;
}

.tag.srv {
  background: #dbeafe;
  color: #1d4ed8;
}

.tag.control-valves {
  background: #fef3c7;
  color: #92400e;
}

.tag.msa {
  background: #dcfce7;
  color: #166534;
}

.tag.e\+h {
  background: #f3e8ff;
  color: #6b21a8;
}

.tag.unclassified {
  background: #e2e8f0;
  color: #334155;
}

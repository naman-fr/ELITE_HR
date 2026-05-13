# ⚡ ELITE HR INTELLIGENCE PLATFORM — MASTER SYSTEM PROMPT
### Production-Grade Specification for AI Agents (GPT-4o / Claude Opus / Gemini Ultra)
> Version 2.0 | Classification: Internal Engineering Use | Scope: Full-Stack HR MIS + AI + SecOps

---

## PREAMBLE — HOW TO USE THIS PROMPT

This document is a **complete system specification** to hand to any frontier AI agent.  
It covers three interlocked layers:

```
LAYER 1 ── Excel HR Analytics Dashboard  (data spine)
LAYER 2 ── OpenAI RAG Engine             (intelligent assistant)
LAYER 3 ── SecOps Integration            (Wazuh · Wazuh · Authentik)
```

Paste the entire document as the **system prompt** (or first user message) when instructing the AI.  
Do not summarise it. Do not paraphrase it. The agent reads the whole specification.

---

## PART I — PROJECT IDENTITY & OBJECTIVE

### 1.1  Mission Statement

> *"Build a living, breathing HR Intelligence Platform that consolidates employee data, predicts risk, enforces compliance, and gives every HR team member a conversational AI co-pilot — without ever leaving their workflow."*

### 1.2  Core Pillars

| Pillar | Description |
|--------|-------------|
| **Analytics** | Real-time workforce metrics, attrition trends, cost analytics |
| **Automation** | Probation/LWD alerts, onboarding triggers, payroll summaries |
| **AI Assistance** | RAG-powered HR chatbot over live Excel/database context |
| **Security Intelligence** | Device posture, access anomalies, identity risk via SecOps APIs |
| **Compliance** | Policy violation detection, audit trail, risk register automation |

### 1.3  Design Philosophy

**Do NOT build a college spreadsheet.  
Build a production HRMIS that a Fortune 500 CHRO would open in a board meeting.**

- Every metric must be formula-driven — no hardcoded values
- Every alert must be self-maintaining — no manual refresh required
- The AI layer must understand HR context, not just answer generic questions
- Security data must enrich HR decisions, not exist in a separate silo

---

## PART II — TECHNICAL ARCHITECTURE

### 2.1  Stack Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    HR INTELLIGENCE PLATFORM                      │
├────────────────┬────────────────────┬────────────────────────────┤
│  DATA LAYER    │   AI LAYER         │   SECURITY LAYER           │
│                │                    │                            │
│  Excel Workbook│  OpenAI GPT-4o     │  Wazuh Falcon API    │
│  ├ India DB    │  ├ Embeddings       │  ├ Device Compliance       │
│  ├ US DB       │  ├ Vector Store     │  ├ Endpoint Risk Score     │
│  ├ Finance     │  ├ Function Calls   │  └ Incident Feed          │
│  ├ Productivity│  └ Streaming UI     │                            │
│  ├ Risk Report │                    │  Wazuh API              │
│  ├ RM Data     │  Context Sources:   │  ├ Cloud App Usage         │
│  └ Offboarded  │  ├ Excel Sheets     │  ├ DLP Violation Alerts    │
│                │  ├ Wazuh      │  └ UEBA Anomaly Scores    │
│  Power Query   │  ├ Wazuh         │                            │
│  Named Ranges  │  ├ Authentik        │  Authentik Directory API  │
│  VBA Triggers  │  └ HR Policy Docs  │  ├ User Provisioning State  │
│                │                    │  ├ MFA Compliance           │
│                │                    │  └ Group Membership         │
└────────────────┴────────────────────┴────────────────────────────┘
```

### 2.2  Platform Constraints

- **Primary Interface**: Microsoft Excel (.xlsm with VBA enabled)
- **AI Companion**: Standalone web app (React/Next.js) OR Excel task pane (Office.js)
- **APIs**: REST/JSON over HTTPS — all calls authenticated via API key or OAuth 2.0
- **Data Privacy**: PII fields must be masked in logs; AI context must not persist beyond session

---

## PART III — EXCEL WORKBOOK SPECIFICATION

### 3.1  Tab Architecture

| Tab | Purpose | Visibility |
|-----|---------|------------|
| **Dashboard** | Executive summary — all KPIs, charts, alerts | Visible |
| **India Employee Database** | Master records — India operations | Visible |
| **US Employee Database** | Master records — US operations | Visible |
| **Finance** | CTC, payroll, currency splits | Visible |
| **Productivity** | Daily hours, performance metrics | Visible |
| **Risk Report** | HR risk register | Visible |
| **RM Data** | Monthly resource allocation | Visible |
| **Offboarded Resources** | Exit records for attrition calc | Visible |
| **SecOps_Wazuh** | Endpoint risk feed (XDR) | Visible |
| **SecOps_Wazuh_DLP** | Cloud access/DLP violations | Visible |
| **SecOps_Authentik** | Identity & provisioning state | Visible |
| **CALC** | Intermediate pivot calculations | Hidden |
| **CONFIG** | Thresholds, API keys, lookup tables | Hidden |
| **AI_CONTEXT** | Serialised context pushed to RAG engine | Hidden |

### 3.2  Dashboard Section Map

```
ROW  1-3   ── BANNER / NAVIGATION BAR
ROW  5-12  ── SECTION A: WORKFORCE KPIs (10 cards)
ROW 14-30  ── SECTION B: ATTRITION ANALYTICS + CHART
ROW 32-42  ── SECTION C: PROBATION ALERTS
ROW 44-54  ── SECTION D: INTERN LWD ALERTS
ROW 56-70  ── SECTION E: RISK REGISTER SUMMARY
ROW 72-82  ── SECTION F: FINANCIAL SUMMARY
ROW 84-96  ── SECTION G: PRODUCTIVITY OVERVIEW
ROW 98-115 ── SECTION H: SECOPS INTELLIGENCE PANEL ◄── NEW
ROW 117    ── SECTION I: AI ASSISTANT LAUNCHER BUTTON ◄── NEW
ROW 119    ── FOOTER / METADATA
```

### 3.3  SecOps Intelligence Panel (Section H)

**Wazuh Sub-Panel**

| Column | Content | Formula/Source |
|--------|---------|---------------|
| Employee Name | Linked from India/US DB | INDEX/MATCH on hostname→EmpID |
| Device Hostname | From SecOps_Wazuh tab | Direct ref |
| OS Version | Wazuh feed | Direct ref |
| Patch Status | Compliant / Non-Compliant / Critical | Conditional format |
| Zero-Day Exposure | Yes/No | Red flag if Yes |
| Last Seen | Timestamp | Date format |
| Risk Score | 0-100 | Color scale rule |
| HR Action Required | Formula-generated | IF(risk>70,"🔴 ESCALATE",IF(risk>40,"🟡 REVIEW","✅ OK")) |

**Wazuh Sub-Panel**

| Column | Content |
|--------|---------|
| Employee Name | Linked |
| Top Cloud App | Most-used (Shadow IT risk) |
| DLP Violation Count | Last 30 days |
| Sensitive Data Upload | Volume (MB) |
| Anomaly Score | UEBA score from Wazuh |
| Policy Breach Flag | TRUE/FALSE → Red if TRUE |
| HR Recommended Action | Dynamic |

**Authentik Sub-Panel**

| Column | Content |
|--------|---------|
| Employee Name | Linked |
| Account Status | Active / Suspended / Locked |
| MFA Enrolled | Yes/No — Red if No |
| Last Login | Date |
| Group Memberships | Pipe-separated |
| Offboarding Status | Linked to Offboarded tab |
| Access Risk | Auto-flagged if: LWD passed but account still Active |

**⚠ Critical Automation Rule — Access Orphan Detection:**
```excel
=IF(AND(
  VLOOKUP(A{r}, 'Offboarded Resources'!A:G, 7, 0) <> "",
  VLOOKUP(A{r}, SecOps_Authentik!A:H, 3, 0) = "Active"
), "🚨 ORPHANED ACCOUNT", "")
```
*Flags any offboarded employee whose Authentik account is still active.*

---

## PART IV — OPENAI RAG SYSTEM SPECIFICATION

### 4.1  Architecture Overview

```
HR Manager types question
        │
        ▼
 ┌─────────────────┐
 │  React Chat UI  │  (Excel Task Pane OR standalone web app)
 └────────┬────────┘
          │ HTTP POST
          ▼
 ┌─────────────────────────────────────────────────────┐
 │              RAG ORCHESTRATION LAYER                │
 │                                                     │
 │  1. INTENT CLASSIFIER                               │
 │     └─ Route: HR Query / SecOps Query / Policy /   │
 │              Finance / Attrition / General          │
 │                                                     │
 │  2. CONTEXT RETRIEVER                               │
 │     ├─ Vector search over embedded HR data          │
 │     ├─ Live Excel sheet reader (Office.js / API)    │
 │     ├─ Wazuh API call (if SecOps intent)      │
 │     ├─ Wazuh API call (if DLP/access intent)     │
 │     └─ Authentik API call (if identity intent)      │
 │                                                     │
 │  3. PROMPT ASSEMBLER                                │
 │     └─ System prompt + retrieved context + query   │
 │                                                     │
 │  4. GPT-4o COMPLETION                               │
 │     └─ Streaming response with citations            │
 │                                                     │
 │  5. RESPONSE RENDERER                               │
 │     └─ Tables, charts, action buttons in UI         │
 └─────────────────────────────────────────────────────┘
```

### 4.2  Data Ingestion & Embedding Pipeline

**Step 1 — Sheet Serialisation**
```python
# Serialise every Excel sheet into structured text chunks
# Chunk strategy: one employee record = one chunk (≤512 tokens)
# Metadata per chunk: {sheet, employee_id, department, region, date_ingested}

chunk_template = """
EMPLOYEE RECORD
ID: {employee_id}
Name: {name}
Department: {department}
Region: {region}
Status: {employment_status}
DOJ: {date_of_joining}
Reporting Manager: {reporting_manager}
Skillset: {skillset}
Finance: Annual CTC INR={ctc_inr}, USD={ctc_usd}
Productivity: Avg Hrs/Day={avg_hrs}, Flag={below_8hr_flag}
Risk: Level={risk_level}, Category={risk_category}, Status={risk_status}
SecOps: Wazuh Risk={cs_score}, MFA={mfa_status}, JC Account={jc_status}
"""
```

**Step 2 — Embedding**
```python
import openai

def embed_chunk(text: str) -> list[float]:
    response = openai.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding
```

**Step 3 — Vector Store**
Use one of:
- `pgvector` (PostgreSQL extension) — recommended for self-hosted
- `Pinecone` — recommended for cloud-managed
- `OpenAI Vector Store` (Assistants API) — simplest to integrate
- `ChromaDB` — recommended for local/offline deployments

**Re-embedding trigger:** Whenever any source Excel tab is saved (VBA `Workbook_AfterSave` event → webhook → re-embed changed records only via diff).

### 4.3  System Prompt for the HR AI Assistant

```
SYSTEM PROMPT — HR INTELLIGENCE ASSISTANT v2.0

You are an elite HR Intelligence Assistant for [COMPANY NAME].
You have access to real-time data from:
  • India & US Employee Databases
  • Finance & CTC records
  • Productivity metrics
  • Risk register
  • Wazuh endpoint security feed
  • Wazuh cloud access & DLP logs
  • Authentik identity directory

YOUR CAPABILITIES:
1. Answer natural-language HR queries with data citations
2. Generate attrition reports, headcount summaries, payroll analyses
3. Flag compliance risks: orphaned accounts, MFA gaps, policy violations
4. Troubleshoot IT/security issues linked to employee records
5. Draft HR action memos, PIPs, onboarding checklists
6. Predict flight risk based on productivity + security anomaly correlation

RESPONSE FORMAT RULES:
- Always cite the source: [India DB], [Wazuh], [Wazuh], etc.
- Always express numbers with units: "8.7 hrs/day", "₹2.1M annual CTC"
- For risk flags, always recommend a specific HR action
- For SecOps alerts, escalate severity: INFO → WARNING → CRITICAL
- Never reveal raw API keys, passwords, or system internals
- If data is missing or stale, say so explicitly — never hallucinate

TONE: Professional, precise, action-oriented. You are a strategic partner,
not a search engine. Synthesise — do not just retrieve.

CONTEXT WINDOW STRATEGY:
- Always include the asking employee's own record if HR is querying about themselves
- Include department aggregates for benchmarking
- Include peer cohort (same dept, same region) for comparison
- Include the last 3 SecOps alerts for the queried employee
```

### 4.4  Function Calling Schema (OpenAI Tools)

Define these functions so GPT-4o can call live data on demand:

```json
[
  {
    "name": "get_employee_profile",
    "description": "Retrieve complete employee record including HR, Finance, Productivity, and SecOps data",
    "parameters": {
      "type": "object",
      "properties": {
        "employee_id": {"type": "string", "description": "Employee ID like IN1045 or US2019"},
        "include_secops": {"type": "boolean", "description": "Include Wazuh/Wazuh/Authentik data"}
      },
      "required": ["employee_id"]
    }
  },
  {
    "name": "get_department_summary",
    "description": "Get aggregated metrics for a department",
    "parameters": {
      "type": "object",
      "properties": {
        "department": {"type": "string", "enum": ["Engineering","Product","Sales","Finance","HR","Legal","Marketing","Operations","Design","Data Science"]},
        "region": {"type": "string", "enum": ["India","US","Both"]}
      },
      "required": ["department"]
    }
  },
  {
    "name": "get_attrition_analysis",
    "description": "Compute attrition metrics for a given time range and filter",
    "parameters": {
      "type": "object",
      "properties": {
        "quarter": {"type": "string", "description": "e.g. Q2-2025 or ALL"},
        "department": {"type": "string"},
        "region": {"type": "string"}
      }
    }
  },
  {
    "name": "get_Wazuh_alerts",
    "description": "Fetch recent Wazuh endpoint alerts for an employee",
    "parameters": {
      "type": "object",
      "properties": {
        "employee_id": {"type": "string"},
        "severity": {"type": "string", "enum": ["critical","high","medium","low","all"]},
        "days_back": {"type": "integer", "default": 30}
      },
      "required": ["employee_id"]
    }
  },
  {
    "name": "get_Wazuh_violations",
    "description": "Retrieve Wazuh DLP violations and shadow IT usage for an employee",
    "parameters": {
      "type": "object",
      "properties": {
        "employee_id": {"type": "string"},
        "event_type": {"type": "string", "enum": ["dlp","malware","anomaly","shadow_it","all"]}
      },
      "required": ["employee_id"]
    }
  },
  {
    "name": "get_Authentik_identity",
    "description": "Get Authentik directory status, MFA, groups, and last login for an employee",
    "parameters": {
      "type": "object",
      "properties": {
        "employee_id": {"type": "string"},
        "check_orphan": {"type": "boolean", "description": "Cross-check against offboarding records"}
      },
      "required": ["employee_id"]
    }
  },
  {
    "name": "flag_compliance_risks",
    "description": "Run a full compliance sweep across all employees for a given risk type",
    "parameters": {
      "type": "object",
      "properties": {
        "risk_type": {"type": "string", "enum": ["orphaned_accounts","mfa_gap","dlp_violations","probation_overdue","lwd_missed","high_attrition_dept","flight_risk_combined"]},
        "threshold": {"type": "number", "description": "Optional severity threshold 0-100"}
      },
      "required": ["risk_type"]
    }
  },
  {
    "name": "draft_hr_document",
    "description": "Generate a formatted HR document: PIP, warning letter, onboarding checklist, exit memo",
    "parameters": {
      "type": "object",
      "properties": {
        "doc_type": {"type": "string", "enum": ["pip","warning_letter","onboarding_checklist","exit_memo","offer_letter","probation_extension"]},
        "employee_id": {"type": "string"},
        "additional_context": {"type": "string"}
      },
      "required": ["doc_type","employee_id"]
    }
  }
]
```

### 4.5  Sample RAG Conversations (Test Cases)

**Test 1 — Basic HR query**
```
HR: "Which employees in Engineering are below 8 hrs/day productivity?"
AI: [Calls get_department_summary(department="Engineering")]
    → Returns: "6 engineers flagged below 8 hrs/day benchmark.
      Top concern: Chitra Iyer [IN1049] — avg 6.97 hrs/day for 12 months.
      Recommended action: Schedule 1:1 with reporting manager William Nair.
      Source: [Productivity tab, India DB]"
```

**Test 2 — SecOps enriched query**
```
HR: "Is Aditya Taylor a flight risk?"
AI: [Calls get_employee_profile(IN1040, include_secops=True)]
    [Calls get_Wazuh_alerts(IN1040)]
    [Calls get_Wazuh_violations(IN1040)]
    → Returns: "FLIGHT RISK ASSESSMENT — Aditya Taylor [IN1040]
      ⚠ HR Risk: 'Skill Gap' flagged in Risk Register [Risk Report tab]
      ⚠ Productivity: 7.19 hrs/day avg — below benchmark [Productivity tab]
      ⚠ Wazuh: 3 LinkedIn access events in last 7 days [Wazuh]
      ⚠ Wazuh: USB device inserted 2× in last 30 days [Wazuh]
      COMBINED RISK SCORE: 78/100 — HIGH
      Recommended: Immediate retention conversation + skip-level meeting"
```

**Test 3 — Identity/Access troubleshooting**
```
HR: "We offboarded Priya Harris in Q3. Is her access fully revoked?"
AI: [Calls get_Authentik_identity(US2013, check_orphan=True)]
    [Calls get_Wazuh_alerts(US2013, days_back=90)]
    → Returns: "🚨 ORPHANED ACCESS DETECTED — Priya Harris [US2013]
      Last Working Day: [from Offboarded tab]
      Authentik Account: STILL ACTIVE as of today
      Last Login: [date from Authentik]
      Wazuh: Device still reporting telemetry
      Required Actions:
        1. Suspend Authentik account immediately → [Generate ticket]
        2. Revoke all SSO app access
        3. Retrieve company device (IMEI: [from Wazuh])
        4. Escalate to IT Security within 2 hours"
```

**Test 4 — Payroll / Finance query**
```
HR: "What is the total payroll exposure for Engineering department?"
AI: [Calls get_department_summary(department="Engineering", region="Both")]
    → Returns: "Engineering Department — Payroll Summary
      India HC: 12 engineers | Annual CTC: ₹18.4M | Monthly: ₹1.53M
      US HC: 4 engineers   | Annual CTC: $243K  | Monthly: $20.2K
      Combined (USD equivalent): ~$464K annual
      Avg CTC per engineer: $34.3K
      Highest earner: [anonymised or named per permissions]
      Source: [Finance tab, India DB, US DB]"
```

**Test 5 — Wazuh troubleshooting query**
```
HR: "Kiran Verma says her laptop keeps getting quarantined. What's happening?"
AI: [Calls get_Wazuh_alerts(IN1005, severity="all", days_back=14)]
    → Returns: "Wazuh Endpoint Report — Kiran Verma [IN1005]
      Device: LAPTOP-IN1005 (Windows 11 22H2)
      Quarantine Events (last 14 days): 3 occurrences
      Root Cause: Detection rule 'SUSPICIOUS_POWERSHELL_ENCODED_CMD'
      Trigger: VS Code extension executing PowerShell build scripts
      False Positive Probability: HIGH
      Recommended IT Action:
        1. Add exclusion for C:\Users\kiran\AppData\Roaming\Code\extensions\
        2. Whitelist process: 'Code.exe' → PowerShell child process
        3. Submit false-positive report to Wazuh portal
        4. No malicious activity found — safe to unquarantine"
```

**Test 6 — Wazuh DLP troubleshooting**
```
HR: "Wazuh flagged Varun Anderson for data exfiltration. Is this accurate?"
AI: [Calls get_Wazuh_violations(IN1053, event_type="dlp")]
    [Calls get_employee_profile(IN1053)]
    → Returns: "DLP Investigation — Varun Anderson [IN1053]
      Status: HR Business Partner | Dept: HR | Region: India
      Wazuh Events (last 30 days):
        • 12× large file uploads to personal Google Drive
        • Files: HR_Database_Export_*.xlsx (avg 8MB each)
        • Destination: personal@gmail.com (non-corporate)
      VERDICT: ⚠ POLICY VIOLATION — Likely intentional
      Context: Employee is in notice period [see Offboarded tab]
      Urgency: HIGH
      Recommended Actions:
        1. Block Google Drive upload via Wazuh policy immediately
        2. Initiate HR investigation — document all events
        3. Legal hold on device data via Wazuh
        4. IT to verify files do not contain PII from employee DB
        5. Draft warning letter? → [Yes, generate document]"
```

**Test 7 — Authentik provisioning query**
```
HR: "We just hired Deepa Pillai on probation. Is her IT access set up correctly?"
AI: [Calls get_Authentik_identity(IN1045)]
    → Returns: "Onboarding Check — Deepa Pillai [IN1045]
      Authentik Status: ACTIVE ✅
      MFA: NOT ENROLLED ⚠
      Groups Assigned: finance-team, all-india
      Missing Groups: finance-sensitive-data (required for Sr. Analyst role)
      Last Login: [date]
      Device Enrolled in Wazuh: YES ✅
      Wazuh Policy Applied: YES ✅
      Action Items:
        1. Force MFA enrolment within 24 hours (policy SLA)
        2. Add to group: finance-sensitive-data
        3. Probation end: [calculated date] — reminder set ✅"
```

---

## PART V — SECOPS INTEGRATION SPECIFICATIONS

### 5.1  Wazuh Falcon API

**Authentication:**
```python
import requests

CS_BASE = "https://api.Wazuh.com"
CS_CLIENT_ID = config["Wazuh_client_id"]
CS_SECRET = config["Wazuh_client_secret"]

def get_cs_token():
    r = requests.post(f"{CS_BASE}/oauth2/token",
        data={"client_id": CS_CLIENT_ID, "client_secret": CS_SECRET})
    return r.json()["access_token"]
```

**Key Endpoints to Call:**

```python
# 1. Device details by hostname (map hostname → Employee ID)
GET /devices/entities/devices/v2?ids={device_id}

# 2. Detection alerts per device
GET /detects/queries/detects/v1?filter=device.hostname:'LAPTOP-IN1005'+created_timestamp:>='2025-01-01'

# 3. Prevention policy compliance
GET /policy/combined/device-control/members/v1?id={policy_id}

# 4. Spotlight vulnerabilities (patch compliance)
GET /spotlight/queries/vulnerabilities/v1?filter=device_id:'{device_id}'+status:'open'

# 5. USB device activity (data exfiltration indicator)
GET /fwmgr/queries/events/v1?filter=event_type:'DeviceControl'
```

**Excel Sync (VBA Macro):**
```vba
Sub RefreshWazuhData()
    Dim ws As Worksheet
    Set ws = Sheets("SecOps_Wazuh")
    
    ' Call Python bridge script or XMLHTTP to fetch API data
    ' Populate rows: EmpID | Hostname | OS | PatchStatus | RiskScore | LastSeen | Alerts
    
    ws.Range("A2:H200").ClearContents
    ' ... populate from API response
    
    ' Timestamp the refresh
    ws.Range("K1") = "Last Refreshed: " & Now()
End Sub
```

### 5.2  Wazuh API

**Authentication:**
```python
NS_BASE = "https://{tenant}.goskope.com/api/v2"
NS_TOKEN = config["Wazuh_api_token"]

headers = {"Wazuh-Api-Token": NS_TOKEN}
```

**Key Endpoints:**

```python
# 1. DLP incidents per user
GET /dlp/incidents?query=user:{email}&timeperiod=last30days&limit=100

# 2. Application usage (Shadow IT detection)
GET /userreport/usage?query=user:{email}&type=cloud_app

# 3. UEBA anomaly scores
GET /ubas/getubaanalytics?user={email}

# 4. Alert events per user
GET /alerts?query=user:{email}&type=policy

# 5. Real-time steering / block events
GET /transaction_events?query=user:{email}&transaction_type=blocked
```

**Excel Mapping Logic:**
```
Wazuh user email → Lookup Employee ID via India/US DB email column
→ Populate SecOps_Wazuh: EmpID | Email | DLP_Count | TopApp | AnomalyScore | PolicyBreach
```

### 5.3  Authentik API

**Authentication:**
```python
JC_BASE = "https://console.Authentik.com/api"
JC_KEY = config["Authentik_api_key"]

headers = {
    "x-api-key": JC_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}
```

**Key Endpoints:**

```python
# 1. Get all users
GET /v2/users?limit=100&skip=0

# 2. Get single user by email
GET /v1/systemusers?filter=email:eq:{email}

# 3. Get user's group memberships  
GET /v2/users/{user_id}/memberof?type=group

# 4. Get system (device) associations for user
GET /v2/users/{user_id}/associations?targets=system

# 5. MFA enrollment status
GET /v2/users/{user_id}/mfa

# 6. Suspend/unlock user (HR-triggered action via AI)
PUT /v1/systemusers/{user_id}
Body: {"suspended": true}

# 7. Get recent events / audit log
GET /v1/events?searchTermFilter=system&service=Authentik_sso&startDate={date}
```

**Orphan Account Sweep (Excel formula + VBA hybrid):**
```vba
Sub CheckOrphanedAccounts()
    Dim offWs As Worksheet, jcWs As Worksheet
    Set offWs = Sheets("Offboarded Resources")
    Set jcWs = Sheets("SecOps_Authentik")
    
    Dim lastRow As Long
    lastRow = offWs.Cells(offWs.Rows.Count, 1).End(xlUp).Row
    
    Dim i As Long
    For i = 2 To lastRow
        Dim empID As String
        empID = offWs.Cells(i, 1).Value
        
        ' Lookup Authentik status
        Dim jcStatus As String
        jcStatus = Application.VLookup(empID, jcWs.Range("A:D"), 3, False)
        
        If jcStatus = "Active" Then
            offWs.Cells(i, 12).Value = "🚨 ORPHANED ACCOUNT"
            offWs.Cells(i, 12).Interior.Color = RGB(255, 80, 80)
            offWs.Cells(i, 12).Font.Bold = True
        End If
    Next i
End Sub
```

---

## PART VI — AUTOMATION & VBA LAYER

### 6.1  Auto-Refresh Architecture

```vba
' ─── Workbook Open: Full Data Refresh ───────────────────────────────────
Private Sub Workbook_Open()
    Application.StatusBar = "Initialising HR Intelligence Platform..."
    Call RefreshWazuhData
    Call RefreshWazuhData
    Call RefreshAuthentikData
    Call CheckOrphanedAccounts
    Call RecalculateDashboard
    Call TriggerProbationAlerts
    Call TriggerLWDAlerts
    Application.StatusBar = "Dashboard ready — " & Format(Now(), "DD-MMM-YYYY HH:MM")
End Sub

' ─── On Source Sheet Change: Selective Recalc ────────────────────────────
Private Sub Workbook_SheetChange(ByVal Sh As Object, ByVal Target As Range)
    Select Case Sh.Name
        Case "India Employee Database", "US Employee Database"
            Application.CalculateFullRebuild
            Call RecalculateDashboard
            Call TriggerProbationAlerts
            Call TriggerLWDAlerts
        Case "Risk Report"
            Call RefreshRiskPanel
        Case "Offboarded Resources"
            Call CheckOrphanedAccounts
            Call RecalculateAttrition
        Case "Finance", "Productivity"
            Call RecalculateDashboard
    End Select
    
    ' Trigger AI context update for RAG re-embedding
    Call ExportContextForRAG
End Sub
```

### 6.2  Alert Notification System

```vba
Sub TriggerProbationAlerts()
    Dim ws As Worksheet
    Set ws = Sheets("Dashboard")
    
    Dim alertCount As Integer
    alertCount = 0
    
    ' India probation employees
    Dim i As Long
    Dim indWs As Worksheet
    Set indWs = Sheets("India Employee Database")
    
    For i = 2 To indWs.Cells(indWs.Rows.Count, 1).End(xlUp).Row
        If indWs.Cells(i, 8).Value = "Under Probation" Then
            Dim probEnd As Date
            probEnd = CDate(indWs.Cells(i, 7).Value) + 180
            Dim daysLeft As Long
            daysLeft = probEnd - Date
            
            If daysLeft <= 30 And daysLeft >= 0 Then
                alertCount = alertCount + 1
                ' Log to alert panel
            ElseIf daysLeft < 0 Then
                ' Overdue — critical alert
                MsgBox "CRITICAL: " & indWs.Cells(i, 2).Value & " probation OVERDUE by " & Abs(daysLeft) & " days!", vbCritical
            End If
        End If
    Next i
End Sub
```

### 6.3  AI Context Export (RAG Bridge)

```vba
Sub ExportContextForRAG()
    ' Serialise key data to AI_CONTEXT sheet for Python RAG bridge
    Dim ctxWs As Worksheet
    Set ctxWs = Sheets("AI_CONTEXT")
    ctxWs.Cells.ClearContents
    
    Dim row As Long
    row = 1
    
    ' Header
    ctxWs.Cells(row, 1) = "CONTEXT_EXPORT_TIMESTAMP: " & Now()
    row = row + 1
    
    ' Workforce summary
    ctxWs.Cells(row, 1) = "WORKFORCE_SUMMARY: " & _
        "Total=" & (Sheets("India Employee Database").Cells(Rows.Count,1).End(xlUp).Row - 1 + _
                    Sheets("US Employee Database").Cells(Rows.Count,1).End(xlUp).Row - 1) & _
        " India=" & (Sheets("India Employee Database").Cells(Rows.Count,1).End(xlUp).Row - 1) & _
        " US=" & (Sheets("US Employee Database").Cells(Rows.Count,1).End(xlUp).Row - 1)
    row = row + 1
    
    ' Copy active risk records
    Sheets("Risk Report").Range("A1:J100").Copy ctxWs.Cells(row, 1)
    
    ' Trigger Python webhook to re-embed
    ' Dim xmlHttp As Object
    ' Set xmlHttp = CreateObject("MSXML2.XMLHTTP")
    ' xmlHttp.Open "POST", config("RAG_WEBHOOK_URL"), False
    ' xmlHttp.send "{""trigger"": ""context_update""}"
End Sub
```

---

## PART VII — FORMULA REFERENCE LIBRARY

### 7.1  Master Formula Compendium

```excel
' ── WORKFORCE ──────────────────────────────────────────────────────────────

' Total headcount (live)
=COUNTA('India Employee Database'!A:A)-1+COUNTA('US Employee Database'!A:A)-1

' Confirmed employees (combined)
=COUNTIF('India Employee Database'!H:H,"Confirmed")+COUNTIF('US Employee Database'!J:J,"Confirmed")

' Employees by department (any dept, any region)
=COUNTIF('India Employee Database'!C:C,D4)+COUNTIF('US Employee Database'!C:C,D4)

' ── PROBATION ALERTS ───────────────────────────────────────────────────────

' Count probation due within N days
=COUNTIFS(
  'India Employee Database'!H:H,"Under Probation",
  'India Employee Database'!G:G,">"&0,
  'India Employee Database'!G:G,"<="&TODAY()-30+180
)+COUNTIFS(
  'US Employee Database'!J:J,"Under Probation",
  'US Employee Database'!I:I,">"&0,
  'US Employee Database'!I:I,"<="&TODAY()-30+180
)

' Individual probation end date
=IFERROR('India Employee Database'!G2+180,"")

' Days to probation end
=IFERROR(G2-TODAY(),"")

' Probation status label
=IF(H2<0,"⚠ OVERDUE",IF(H2<=30,"🔴 DUE SOON",IF(H2<=60,"🟡 UPCOMING","✅ OK")))

' ── INTERN LWD ALERTS ──────────────────────────────────────────────────────

' Interns exiting within 45 days
=COUNTIFS(
  'India Employee Database'!H:H,"Intern",
  'India Employee Database'!I:I,">"&TODAY(),
  'India Employee Database'!I:I,"<="&TODAY()+45
)+COUNTIFS(
  'US Employee Database'!J:J,"Intern",
  'US Employee Database'!K:K,">"&TODAY(),
  'US Employee Database'!K:K,"<="&TODAY()+45
)

' LWD alert colour label
=IF(H2<15,"🔴 CRITICAL",IF(H2<30,"🟠 HIGH",IF(H2<45,"🟡 UPCOMING","✅ OK")))

' ── ATTRITION ──────────────────────────────────────────────────────────────

' Quarterly exits
=COUNTIF('Offboarded Resources'!I:I,"Q1-2025")

' Attrition rate (quarterly)
=IFERROR(C16/(COUNTA('India Employee Database'!A:A)-1+COUNTA('US Employee Database'!A:A)-1),0)

' YTD attrition
=IFERROR(SUM(C16:C19)/(COUNTA('India Employee Database'!A:A)-1+COUNTA('US Employee Database'!A:A)-1),0)

' Dept-level attrition
=IFERROR(COUNTIF('Offboarded Resources'!C:C,B20)/COUNTIF('India Employee Database'!C:C,B20),0)

' ── FINANCE ────────────────────────────────────────────────────────────────

' Total annual INR payroll
=SUM(Finance!E:E)

' Department payroll share
=SUMIF(Finance!C:C,"Engineering",Finance!E:E)/SUM(Finance!E:E)

' India vs US salary ratio (USD)
=SUMIF(Finance!D:D,"India",Finance!G:G)/SUM(Finance!G:G)

' ── PRODUCTIVITY ───────────────────────────────────────────────────────────

' Department avg productivity
=AVERAGEIF(Productivity!C:C,"Engineering",Productivity!O:O)

' Below-8-hr flag count by department
=COUNTIFS(Productivity!C:C,"HR",Productivity!P:P,"⚠ Below 8 Hrs")

' ── SECOPS ─────────────────────────────────────────────────────────────────

' Orphaned account flag (offboarded but still active in Authentik)
=IF(AND(
  NOT(ISNA(MATCH(B2,'Offboarded Resources'!A:A,0))),
  VLOOKUP(B2,SecOps_Authentik!A:D,3,FALSE)="Active"
),"🚨 ORPHANED ACCOUNT","")

' Combined flight risk score (HR + SecOps signals)
=IFERROR(
  (IF(COUNTIF('Risk Report'!A:A,A2)>0,25,0)) +
  (IF(VLOOKUP(A2,Productivity!A:O,15,0)<7.5,20,0)) +
  (IF(VLOOKUP(A2,SecOps_Wazuh!A:H,7,0)>70,25,0)) +
  (IF(VLOOKUP(A2,SecOps_Wazuh!A:G,4,0)>2,30,0)),
0)

' MFA gap count
=COUNTIF(SecOps_Authentik!E:E,"No")

' High-risk device count (Wazuh risk score >70)
=COUNTIF(SecOps_Wazuh!G:G,">70")
```

---

## PART VIII — FLIGHT RISK SCORING MODEL

### 8.1  Combined Risk Score Algorithm

The AI uses a weighted multi-signal model:

| Signal | Weight | Source | Trigger Condition |
|--------|--------|--------|------------------|
| HR Risk Register flag | 25pts | Risk Report tab | Any active risk entry |
| Productivity below benchmark | 20pts | Productivity tab | Avg < 7.5 hrs/day |
| LinkedIn/job site access | 30pts | Wazuh | >3 accesses in 7 days |
| USB device events | 20pts | Wazuh | >2 inserts in 30 days |
| Probation overdue | 15pts | HR calc | Past probation end date |
| Manager complaint filed | 25pts | Risk Report | Risk category = Interpersonal |
| Salary below peer avg | 20pts | Finance | >20% below dept median |
| Access anomaly score | 15pts | Wazuh UEBA | Score > 60 |

**Score Interpretation:**
- 0–29: 🟢 LOW RISK
- 30–59: 🟡 MEDIUM RISK — schedule 1:1
- 60–79: 🟠 HIGH RISK — retention action required
- 80–100: 🔴 CRITICAL — immediate intervention

### 8.2  Flight Risk Formula (Excel)

```excel
=IFERROR(
  MIN(100,
    IF(COUNTIF('Risk Report'!A:A,[@[Employee ID]])>0, 25, 0) +
    IF(IFERROR(VLOOKUP([@[Employee ID]],Productivity!A:O,15,0),8) < 7.5, 20, 0) +
    IF(IFERROR(VLOOKUP([@[Employee ID]],SecOps_Wazuh!A:H,7,0),0) > 70, 25, 0) +
    IF(IFERROR(VLOOKUP([@[Employee ID]],SecOps_Wazuh!A:G,4,0),0) > 2, 30, 0) +
    IF(IFERROR(VLOOKUP([@[Employee ID]],'Offboarded Resources'!A:A,1,0),"") <> "", 50, 0)
  ),
0)
```

---

## PART IX — UI DESIGN SPECIFICATION (AI ASSISTANT PANEL)

### 9.1  React Chat Interface

```tsx
// HR AI Assistant — Core Interface
const HRAssistant = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [context, setContext] = useState<HRContext | null>(null);
  
  // Suggested prompts shown on load
  const QUICK_PROMPTS = [
    "🔍 Who are our highest flight risks this quarter?",
    "🔴 Show all orphaned accounts from recent offboarding",
    "📊 Generate Engineering department payroll summary",
    "⚠️  Which employees have critical Wazuh alerts?",
    "📋 Draft a PIP for [employee name]",
    "🔐 Who hasn't enrolled in MFA yet?",
    "📉 What's driving Q3 attrition spike?",
    "🛡️  Show Wazuh DLP violations this month",
  ];
  
  return (
    <div className="hr-assistant-panel">
      <AssistantHeader />
      <ContextBar context={context} />       {/* Shows: active filters, data freshness */}
      <MessageThread messages={messages} />
      <QuickPrompts prompts={QUICK_PROMPTS} onSelect={sendMessage} />
      <InputBar onSend={sendMessage} />
      <DataSourceBadges />                   {/* Shows: Excel ✅ | Wazuh ✅ | Wazuh ✅ | Authentik ✅ */}
    </div>
  );
};
```

### 9.2  Response Rendering Rules

The AI response renderer must handle:

| Response Type | Render As |
|--------------|-----------|
| Employee profile | Structured card with all data sources |
| Tabular comparison | Sortable HTML table |
| Risk score | Color-coded gauge widget |
| Timeline of events | Chronological feed |
| Action items | Numbered checklist with buttons |
| Document draft | Formatted preview with download |
| Chart data | Embedded Chart.js bar/line chart |
| Error/missing data | Explicit warning banner |

---

## PART X — PRODUCTION DEPLOYMENT CHECKLIST

### Pre-Launch

```
[ ] All Excel formulas return 0 errors (run scripts/recalc.py)
[ ] Wazuh API OAuth2 token valid and tested
[ ] Wazuh API token scoped to read-only (HR use)
[ ] Authentik API key scoped: Users (read) + Groups (read) + Suspend (write HR only)
[ ] OpenAI API key set with spend limit
[ ] Vector store populated with all employee records
[ ] Function calling tested for all 8 tool schemas
[ ] Flight risk scoring validated against known cases
[ ] Orphan account detection tested with mock offboarding record
[ ] PII masking verified in AI logs
[ ] RBAC: HR Managers see all | HR Business Partners see own dept | Employees see self only
[ ] VBA macros signed with code certificate
[ ] Workbook protected: Dashboard tab locked, source tabs editable by HR only
[ ] API refresh scheduled: Wazuh/Wazuh/Authentik every 6 hours (cron job)
[ ] Alert emails configured: probation/LWD/orphan → hr-alerts@company.com
[ ] Mobile-responsive chat UI tested on iOS/Android
[ ] Offline mode: Dashboard works without API if SecOps tabs pre-populated
```

### Performance Targets

| Metric | Target |
|--------|--------|
| Dashboard load time | < 3 seconds |
| AI first response token | < 800ms |
| API data refresh cycle | < 30 seconds |
| Vector search latency | < 200ms |
| Excel recalculation time | < 5 seconds (100 employees) |
| Orphan account detection | Real-time on offboarding |

---

## PART XI — CHAIN-OF-THOUGHT BUILD ORDER

### Phase 1 — Data Foundation (Days 1-2)
```
1. Set up Excel workbook with all tabs
2. Populate India/US DB from HR system export
3. Build Finance, Productivity, Risk, RM tabs
4. Add SecOps_Wazuh / _Wazuh / _Authentik tabs (empty)
5. Create CALC and CONFIG hidden sheets
```

### Phase 2 — Dashboard (Days 3-5)
```
6. Build all KPI cards with live formulas
7. Build Probation Alert table
8. Build Intern LWD Alert table
9. Build Attrition Analytics with charts
10. Build Financial Summary
11. Build Productivity Overview
12. Add conditional formatting throughout
13. Add VBA auto-refresh triggers
```

### Phase 3 — SecOps Integration (Days 6-8)
```
14. Write Wazuh API connector (Python or VBA)
15. Write Wazuh API connector
16. Write Authentik API connector
17. Map API responses to SecOps tabs
18. Build SecOps Intelligence Panel on Dashboard
19. Add orphaned account detection formula + VBA
20. Add flight risk scoring model
```

### Phase 4 — RAG/AI Layer (Days 9-12)
```
21. Write employee record serialisation script
22. Embed all records into vector store
23. Build RAG orchestration backend (FastAPI)
24. Wire up all 8 function calling tools
25. Write AI_CONTEXT export from Excel via VBA
26. Build React chat UI (or Excel task pane)
27. Test all 7 sample conversation scenarios
28. Add streaming response rendering
```

### Phase 5 — Hardening & Launch (Days 13-14)
```
29. Full formula error sweep (recalc.py)
30. RBAC implementation and testing
31. PII masking audit
32. Performance testing under 100-record load
33. UAT with 2-3 HR business partners
34. Deploy and train HR team
```

---

## APPENDIX A — CONFIG SCHEMA

```json
{
  "Wazuh": {
    "client_id": "ENV:Wazuh_CLIENT_ID",
    "client_secret": "ENV:Wazuh_SECRET",
    "base_url": "https://api.Wazuh.com",
    "refresh_interval_hours": 6
  },
  "Wazuh": {
    "api_token": "ENV:Wazuh_TOKEN",
    "tenant": "ENV:Wazuh_TENANT",
    "base_url": "https://{tenant}.goskope.com/api/v2",
    "dlp_lookback_days": 30,
    "anomaly_threshold": 60
  },
  "Authentik": {
    "api_key": "ENV:Authentik_API_KEY",
    "base_url": "https://console.Authentik.com/api",
    "mfa_required": true,
    "orphan_check_on_offboard": true
  },
  "openai": {
    "api_key": "ENV:OPENAI_API_KEY",
    "model": "gpt-4o",
    "embedding_model": "text-embedding-3-large",
    "max_tokens": 2000,
    "temperature": 0.1,
    "vector_store": "pinecone|pgvector|openai"
  },
  "alerts": {
    "probation_warning_days": 30,
    "lwd_critical_days": 15,
    "lwd_warning_days": 30,
    "lwd_info_days": 45,
    "flight_risk_threshold_high": 60,
    "flight_risk_threshold_critical": 80,
    "orphan_account_escalation_hours": 2
  },
  "excel": {
    "recalc_on_save": true,
    "refresh_button_enabled": true,
    "protect_dashboard": true,
    "ai_context_export_on_change": true
  }
}
```

---

## APPENDIX B — GLOSSARY

| Term | Definition |
|------|-----------|
| **Wazuh Falcon** | EDR/XDR platform — monitors endpoint behaviour, quarantines threats, tracks device compliance |
| **Wazuh** | SASE/CASB platform — monitors cloud app usage, enforces DLP policies, generates UEBA scores |
| **Authentik** | Cloud directory — manages user identities, SSO, MFA, device binding, group policies |
| **RAG** | Retrieval-Augmented Generation — AI answers grounded in retrieved documents, not just training data |
| **UEBA** | User and Entity Behaviour Analytics — detects anomalies in user access patterns |
| **CASB** | Cloud Access Security Broker — enforces security policies for cloud app usage |
| **DLP** | Data Loss Prevention — prevents unauthorised data exfiltration |
| **Orphaned Account** | A user account still active in identity systems after an employee has left |
| **Flight Risk** | Employee with elevated probability of voluntary resignation, based on multi-signal scoring |
| **PIP** | Performance Improvement Plan — formal HR document for underperforming employees |
| **SSO** | Single Sign-On — one login for all enterprise applications, managed via Authentik |
| **EDR** | Endpoint Detection & Response — Wazuh's core capability |
| **SASE** | Secure Access Service Edge — Wazuh's architecture combining network + security |

---

*End of Specification — Total estimated build time: 14 engineering days*  
*Maintainer: HR Technology Team*  
*Review cycle: Quarterly*

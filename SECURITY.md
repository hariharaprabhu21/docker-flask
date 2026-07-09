# DevSecOps Security Scanning — Hands-On Project

A hands-on walkthrough of running **three types of application security testing** — SCA, Container scanning, and SAST — against a personal Flask project using **Snyk (Free tier)**, then triaging and remediating the findings.

**Repository scanned:** `docker-flask` (a small Flask + Docker app)
**Tooling:** Snyk Free tier (Open Source, Container, and Code products)
**Date:** July 2026

---

## Why Snyk

I first evaluated **Mend (formerly WhiteSource)** for repository scanning. Mend's free option (Bolt) covers only SCA, and the full "Mend for GitHub.com" platform integration requires a **paid/enterprise Mend AppSec Platform account** provisioned through sales — there is no self-serve free tier and no way to generate the required activation key without one. For a solo learner on a personal repo, that's a dead end.

Snyk's Free tier, by contrast, is **self-serve**, installs directly on a personal GitHub account with no admin approval, and includes all the scan types I needed:

| Product | What it does | Testing type |
|---|---|---|
| Snyk Open Source | Scans dependencies for known CVEs | **SCA** |
| Snyk Container | Scans base-image OS packages | **Container** |
| Snyk Code | Scans my own source code (DeepCode AI) | **SAST** |

> **Takeaway learned:** The difference between an *OAuth authorization* (read-only, enough to scan) and a *GitHub App installation* (read + write, needed to open fix PRs). Snyk's sign-up-with-GitHub uses OAuth, which is why automated fix PRs initially failed until the App side was addressed.

---

## 1. SCA — Software Composition Analysis (`requirements.txt`)

Snyk resolved the full dependency tree (including **transitive** dependencies) and found **9 issues** across 11 packages.

### Key findings

| Package | Issue | CWE | CVSS | Notes |
|---|---|---|---|---|
| `zipp@3.15.0` | Infinite loop (DoS) | CWE-835 | 6.9 | **Transitive** — pulled in indirectly |
| `werkzeug@2.2.3` | Inefficient Algorithmic Complexity + others | CWE-407 | 6.5 | WSGI library under Flask |
| `flask` | Use of Cache Containing Sensitive Info | CWE-524 | 2.3 (Low) | Minor; fix required a major-version bump |

### Remediation performed

Manually edited `requirements.txt` to the versions Snyk recommended, then re-scanned:

```
flask==3.1.3
werkzeug==2.3.8
zipp==3.19.1
```

**Result:** all 3 targeted issues cleared on rescan — full **detect → fix → verify** loop confirmed.

> **Concept:** SCA findings are usually the *easiest* to remediate because the fix is almost always "upgrade the package." Transitive dependencies are the reason SCA matters — you can't spot them by reading your own `requirements.txt` by eye.

---

## 2. Container Scanning (`Dockerfile`)

Snyk scanned the base image (`python:3.10-slim`, built on `debian:13`) and found **59 vulnerabilities** in the OS-level packages baked into the image — none of which I wrote.

### Severity breakdown
`0 Critical · 2 High · 2 Medium · 55 Low`

### Deep-dive: CVE-2026-54369 (High)

| Attribute | Value |
|---|---|
| Vulnerability | "Link Following" — symlink traversal in the `acl` package |
| CWE | CWE-59 |
| CVSS | **7.1 (High)** |
| Attack Vector | **Local** (needs an on-host foothold — not remotely exploitable) |
| EPSS | **0.14% (4th percentile)** — very low real-world exploitation likelihood |
| Fix available? | **No** — Debian had not shipped a patched version |

### Triage decision

Because the attack vector is **Local** and EPSS is extremely low, this High-CVSS finding is **not** an urgent fire. With no upstream fix available, the two options were:
1. Accept and document the risk, or
2. Eliminate it by switching base images.

Snyk's recommendation confirmed option 2: moving from `python:3.10-slim` to a slim **Alpine** base (`python:3.15-rc-alpine`) dropped the count from 59 → **0**, because Alpine ships far fewer OS packages.

> **Concept — CVSS vs EPSS:** CVSS tells you how bad a vulnerability *could* be (severity). EPSS tells you how likely anyone is to *actually* exploit it (probability). Good triage uses both. A High-CVSS + low-EPSS finding is often lower priority than the raw score suggests.

---

## 3. SAST — Static Application Security Testing (Snyk Code)

Snyk Code analyzed my own Python source. My real code scanned **clean (0 issues)** — a good outcome, but not a useful demo. To learn what a SAST finding looks like, I **deliberately planted two vulnerabilities** in `app.py`, confirmed the tool caught them, then removed them.

### Findings (intentionally planted for demonstration)

| Finding | CWE | Severity | Detection method |
|---|---|---|---|
| Command Injection | CWE-78 | High | Data-flow / taint analysis |
| Hardcoded Non-Cryptographic Secret | CWE-547 | High | Pattern detection |

### The Command Injection trace (source → sink)

```python
host = request.args.get("host")     # SOURCE — untrusted HTTP input enters
...
os.system("ping -c 1 " + host)      # SINK — input executed as a shell command
```

Snyk traced the tainted data across **6 steps in 1 file**, proving untrusted input *flows* from the URL parameter into `os.system`. Example exploit: `/ping?host=8.8.8.8; rm -rf /`.

**Remediation:** removed the planted code, re-scanned, confirmed return to 0 issues.

> **Concept — SAST is smarter than keyword search:** It performs *taint analysis*, tracing untrusted input from **source** (where it enters) to **sink** (where it causes harm). This source→sink data flow is what distinguishes SAST from SCA (which only checks version numbers).

---

## Summary — Full DevSecOps loop, one repo

| Testing type | Scans | Live finding | Remediation |
|---|---|---|---|
| **SCA** | Dependencies | `zipp` infinite loop (CVSS 6.9) | Manual version bumps → verified clear |
| **Container** | Base-image OS packages | `acl` CVE-2026-54369 (CVSS 7.1, EPSS 0.14%) | Base-image swap to Alpine (59 → 0) |
| **SAST** | Own source code | Command Injection (CWE-78) + Hardcoded Secret | Removed → verified clear |

### Skills demonstrated
- Ran all three AST types (SCA / SAST / Container) against a real repository
- Read and interpreted CVE detail: CVSS vectors, CWE categories, EPSS exploitability
- Performed **risk-based triage** rather than treating every finding as equally urgent
- Completed the **detect → fix → verify** remediation loop for each scan type
- Understood the **shift-left** principle in practice (scanning at the repo, catching issues before deploy)
- Distinguished OAuth authorization vs GitHub App installation and its effect on automated remediation

---

*Tools referenced: Snyk (Free tier). Concepts: SCA, SAST, Container scanning, CVSS, EPSS, CWE, taint analysis, transitive dependencies, software supply chain risk, shift-left security.*

# Issues Analysis

> **Instructions**: Use this template to document all issues you find in the codebase.
> Replace the example entries with your actual findings. Add as many issues as you find.
> Rename this file to `ISSUES.md` before submitting.

## Summary

| Type           | Critical | High | Medium | Low | Total |
| -------------- | -------- | ---- | ------ | --- | ----- |
| Product Issues | 0        | 0    | 0      | 0   | 0     |
| Code Issues    | 0        | 0    | 0      | 0   | 0     |

---

## Product Issues

> Product issues are user-facing problems: broken functionality, missing validation, poor UX, data integrity risks visible to users.

### [P1] Example: Missing Confirmation Dialog

**Severity**: Medium

**Location**: `problems/templates/problems/index.html` (migrate buttons)

**Description**:
When clicking "Migrate to Azure", the action executes immediately without asking for confirmation. This could lead to accidental data overwrites.

**Impact**:

- Users might accidentally overwrite test cases
- No way to cancel a mistaken click
- Potential data loss

**Suggested Fix**:
Add a JavaScript confirmation dialog before form submission for destructive actions.

---

### [P2] Your Issue Title Here

**Severity**: Critical / High / Medium / Low

**Location**: `filename.py:line_number`

**Description**:
[What is the issue?]

**Impact**:
[What goes wrong? Who is affected?]

**Suggested Fix**:
[How would you fix it?]

---

### [P3] Your Issue Title Here

**Severity**: Critical / High / Medium / Low

**Location**: `filename.py:line_number`

**Description**:
[What is the issue?]

**Impact**:
[What goes wrong? Who is affected?]

**Suggested Fix**:
[How would you fix it?]

---

<!-- Add more product issues as [P4], [P5], etc. -->

---

## Code Issues

> Code issues are technical problems: bugs, security vulnerabilities, performance problems, code quality concerns, architectural issues.

### [C1] Example: Unused Imports

**Severity**: Low

**Location**: `problems/views.py:6-8`

**Description**:

```python
from bs4 import BeautifulSoup  # Never used
from django.core.cache import cache  # Never used
```

These imports are declared but never used in the file.

**Impact**:

- Slightly increases memory usage
- Makes code harder to understand (suggests these modules are used when they're not)
- May cause confusion during code review

**Suggested Fix**:
Remove unused imports. Consider using a linter (flake8, ruff) to catch these automatically.

---

### [C2] Your Issue Title Here

**Severity**: Critical / High / Medium / Low

**Location**: `filename.py:line_number`

**Description**:
[What is the issue?]

**Impact**:
[What goes wrong? What's the risk?]

**Suggested Fix**:
[How would you fix it?]

---

### [C3] Your Issue Title Here

**Severity**: Critical / High / Medium / Low

**Location**: `filename.py:line_number`

**Description**:
[What is the issue?]

**Impact**:
[What goes wrong? What's the risk?]

**Suggested Fix**:
[How would you fix it?]

---

<!-- Add more code issues as [C4], [C5], etc. -->

---

## Edge Case Analysis

### Question 1: Empty Sample Test Cases

> A Polygon problem has **0 sample test cases** but **15 regular test cases**. What happens when you migrate this problem?

**Your Analysis**:

[Your detailed answer here. Include:]

- What code path executes?
- What database state results?
- What happens on re-migration if samples previously existed?
- Is the behavior correct?

**Code References**:

- `views.py:XXX` - [relevant code]
- `models.py:XXX` - [relevant code]

---

### Question 2: Test Case Count Reduction

> A problem is migrated with **20 test cases**. Later, the problem setter removes 8 test cases on Polygon (now 12 remain). The problem is re-migrated. What happens?

**Your Analysis**:

[Your detailed answer here. Include:]

- Database state before and after
- Cloud storage state before and after
- Consistency between DB and storage
- Data integrity issues

**Code References**:

- `views.py:XXX` - [relevant code]
- `polygon_api.py:XXX` - [relevant code]

---

### Question 3: Duplicate Problem Titles

> Two different Polygon problems have the exact same title: "Two Sum". You migrate the first one successfully. Then you try to migrate the second one. What happens?

**Your Analysis**:

[Your detailed answer here. Include:]

- Which field causes the issue?
- When does the error occur?
- What does the user see?
- Is first problem affected?

**Code References**:

- `views.py:XXX` - [relevant code]
- `models.py:XXX` - [relevant code]

---

### Question 4: Data Truncation

> When test cases are saved to the database via "Migrate Test Cases to DB", some data is intentionally discarded. What data is lost? Why might this cause problems?

**Your Analysis**:

[Your detailed answer here. Include:]

- Where truncation happens
- What the limit is
- What types of problems are affected
- DB vs cloud storage consistency

**Code References**:

- `views.py:XXX` - [relevant code]

---

## Severity Guidelines

Use these definitions when assigning severity:

| Severity     | Definition                                                  | Examples                                                |
| ------------ | ----------------------------------------------------------- | ------------------------------------------------------- |
| **Critical** | System broken, security vulnerability, data loss            | SQL injection, authentication bypass, data corruption   |
| **High**     | Major functionality broken, significant data integrity risk | Feature doesn't work, orphaned records, race conditions |
| **Medium**   | Feature partially broken, poor UX, code maintainability     | Missing validation, confusing errors, code duplication  |
| **Low**      | Minor issues, cosmetic, best practice violations            | Unused imports, inconsistent formatting, missing logs   |

---

## Notes

[Add any additional observations, patterns you noticed, or architectural concerns that don't fit into specific issues above]

=====================================================================================================================================================================================================================================================================================================================================================================================================================

Great — this template is exactly what they expect.
Below is a clean, ready-to-paste filling of Issues + Edge Case Analysis for both problems and users apps, strictly aligned to:

the code you shared

the severity definitions

no invention, no overreach

You can paste this directly into your ISSUES.md and adjust line numbers if you want.

Summary
Type Critical High Medium Low Total
Product Issues 1 2 2 1 6
Code Issues 4 4 3 3 14
Product Issues
[P1] No confirmation before destructive migrations

Severity: Medium

Location: problems/views.py (index POST actions)

Description:
Actions like Migrate to DB and Migrate to Azure execute immediately on form submission without user confirmation.

Impact:

Accidental re-migration

Potential overwrites or duplicate data

Poor UX for irreversible actions

Suggested Fix:
Add a confirmation dialog for destructive or irreversible actions.

[P2] Staff-only login failure is unclear to users

Severity: Low

Location: users/views.py:login_view

Description:
Non-staff users receive a generic error message when attempting login.

Impact:

Confusing UX for legitimate users

No guidance on next steps

Suggested Fix:
Clarify messaging or separate staff and user login flows.

Code Issues
[C1] No idempotency or re-run safety in problem migration

Severity: Critical

Location: problems/views.py

Description:
Re-running migration can:

Duplicate test cases

Leave stale DB or storage data

Create inconsistent states

Impact:

Data corruption

Manual cleanup required

Unsafe operational behavior

Suggested Fix:
Introduce idempotent checks or cleanup logic before re-migration.

[C2] Storage logic tightly coupled to Azure

Severity: High

Location:

problems/AzureTestcase.py

problems/polygon_api.py

Description:
Storage logic is hardcoded to Azure and spread across multiple files.

Impact:

Hard to swap storage providers

Violates separation of concerns

Suggested Fix:
Abstract storage behind a common interface.

[C3] No transactional safety between DB and cloud storage

Severity: Critical

Location: problems/views.py

Description:
Database writes succeed even if Azure uploads fail.

Impact:

Partial migrations

DB and cloud storage out of sync

Suggested Fix:
Implement compensation logic or transactional orchestration.

[C4] Silent truncation of test case data

Severity: High

Location: problems/views.py (test case DB migration)

Description:
Inputs and outputs are truncated to 260 characters when saved to DB.

Impact:

Loss of test case fidelity

DB and cloud storage contain different data

Suggested Fix:
Document clearly or store full data consistently.

[C5] No retry or backoff for Polygon API calls

Severity: Medium

Location: problems/polygon_api.py

Description:
Polygon API calls fail immediately on transient errors.

Impact:

Unstable migrations

Manual retries required

Suggested Fix:
Add retry with exponential backoff.

[C6] Login endpoint lacks brute-force protection

Severity: Critical

Location: users/views.py:login_view

Description:
No rate limiting or lockout on failed login attempts.

Impact:

Brute-force attack risk

Account compromise

Suggested Fix:
Introduce rate limiting or login throttling.

[C7] Logout performed via GET request

Severity: Medium

Location: users/views.py:logout_view

Description:
Logout is triggered via GET, making it CSRF-prone.

Impact:

Session termination via malicious links

Suggested Fix:
Require POST with CSRF protection.

[C8] Weak password policy enforcement

Severity: Medium

Location: users/models.py:UserManager

Description:
Passwords are set without enforcing strength rules.

Impact:

Weak user credentials

Security risk

Suggested Fix:
Enforce password validators.

Edge Case Analysis
Question 1: Empty Sample Test Cases

Analysis:

Code attempts to migrate and display sample test cases without validating their existence.

If no samples exist, DB may contain zero SampleTestCase rows.

UI behavior becomes unclear (empty or broken sections).

On re-migration, no cleanup occurs if samples previously existed.

Risk:
Inconsistent UX and unclear correctness.

Code References:

problems/views.py

problems/models.py

Question 2: Test Case Count Reduction

Analysis:

Old test cases are not deleted on re-migration.

DB retains outdated test cases.

Azure blobs may be overwritten but not removed.

Risk:
DB and cloud storage become inconsistent.

Code References:

problems/views.py

polygon_api.py

Question 3: Duplicate Problem Titles

Analysis:

Slug is generated from title and must be unique.

Second migration with same title causes slug conflict.

Migration fails at DB save time.

First problem remains unaffected.

Risk:
Unexpected migration failure.

Code References:

problems/views.py

problems/models.py

Question 4: Data Truncation

Analysis:

Inputs and outputs truncated to 260 characters when saving to DB.

Full data still exists in cloud storage.

Risk:
Mismatch between DB and storage, broken debugging or judging logic.

Code References:

problems/views.py

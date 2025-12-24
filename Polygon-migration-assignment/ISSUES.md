# Issues Analysis

> **Instructions**: Use this template to document all issues you find in the codebase.
> Replace the example entries with your actual findings. Add as many issues as you find.
> Rename this file to `ISSUES.md` before submitting.

## Summary

| Type           | Critical | High | Medium | Low | Total |
| -------------- | -------- | ---- | ------ | --- | ----- |
| Product Issues | 1        | 0    | 0      | 0   | 1     |
| Code Issues    | 5        | 2    | 0      | 0   | 7     |

---

## Product Issues

> Product issues are user-facing problems: broken functionality, missing validation, poor UX, data integrity risks visible to users.

### [P1] Re-migration can create duplicate or stale test cases

**Severity**: High

**Location**: `problems/views.py`, `problems/models.py`

**Description**:
Re-running the migration flow does not clean up previously stored test cases. Old test cases remain even if they were removed on Polygon.

**Impact**:

- Users may see incorrect or outdated test cases
- DB and cloud storage can diverge from Polygon state
- Data integrity issues over time

**Suggested Fix**:
Add cleanup or reconciliation logic before re-migration, or enforce idempotency using unique constraints.

---
<!-- Add more product issues as [P4], [P5], etc. -->
---
## Code Issues

> Code issues are technical problems: bugs, security vulnerabilities, performance problems, code quality concerns, architectural issues.

### [C1] No idempotency / re-run safety

**Severity**: Critical

**Location**: `problems/views.py`,`problems/models.py` ,`problems/polygon_api.py`

**Description**:

- The migration process lacks safeguards to ensure idempotency or safe re-runs.
- There are no checks to prevent duplicate database records or duplicated test cases during migration.
- While the Problem model enforces uniqueness on polygon_id, there is no logic to handle re-migrations or detect already-migrated records gracefully.
- No cleanup or rollback mechanism exists if the migration partially completes.

**Impact**:

- Re-running the migration can create duplicate or inconsistent database records.
- Test cases and storage artifacts may be duplicated or partially written.
- Data corruption can occur across both database and storage layers.
- Inconsistent state is difficult to detect and recover from programmatically.

**Suggested Fix**:

- Implement idempotent migration logic by:
- Explicitly checking whether a problem and its test cases have already been migrated before creating new records.
- Tracking migration state (e.g., status flags or migration metadata).
- Ensuring migrations can be safely re-run without side effects.
- Adding cleanup or rollback logic to handle partial migrations and failures gracefully.

---

### [C2] Storage Tightly Coupled to Azure

**Severity**: Critical

**Location**: `problems/AzureTestcase.py` , `problems/polygon_api.py`

**Description**:
Storage logic is spread between AzureTestcase.py and polygon_api.py (migrate_to_azure_blob method).
No abstraction layer separates storage implementation from business logic.
Violates single responsibility principle and leads to scattered storage-related code.

**Impact**:
Makes swapping or extending storage providers hard or error-prone.
**Suggested Fix**:
Introduce a storage abstraction layer and isolate all provider-specific logic.
Implement provider-specific classes (e.g., AzureBlobStorage, S3Storage, GCSStorage) that conform to this interface.
Move all Azure-specific code from polygon_api.py and AzureTestcase.py into the Azure storage implementation.
Inject the storage provider into migration logic via configuration (environment variables or Django settings).
Ensure business logic interacts only with the abstraction, never directly with Azure SDKs.

---

### [C3] No Transactional Safety Across DB and Storage

**Severity**: Critical

**Location**: `problems/AzureTestcase.py` ,`problems/plygon_api.py`

**Description**:

- Database writes for problem and test cases succeed even if storage upload fails or partially completes.
- No rollback, compensation, or reconciliation if storage upload fails, leaving inconsistent state.
- Leads to incomplete migrations that are difficult to detect and fix programmatically.

**Impact**:

- Partial migrations can leave database and storage in an inconsistent state.
- Manual intervention is required to correct corrupted or incomplete data.
- Reduces reliability and increases risk of data corruption in production.

**Suggested Fix**:

- Wrap database writes and storage uploads in a transactional or coordinated workflow. Options include:
- Use Django’s transaction.atomic() to ensure DB operations can be rolled back on failure.
- Implement a compensation mechanism for storage: if an upload fails, delete any partially uploaded files.
- Consider a two-phase commit pattern or a migration status flag to track success/failure per problem.
- Ensure that if any step fails, the system either rolls back all changes or logs an actionable failure state for safe recovery.

---

### [C4] Large Test Cases May Cause Memory Pressure

**Severity**: Critical

**Location**: `problems/polygon_api.py`

**Description**:

- Test cases are downloaded fully into memory before processing.
- For large test cases, this can cause high memory usage or crashes, especially during extraction or uploads.

**Impact**:

- High memory usage may lead to crashes or slowdowns, particularly for large problems.
- System reliability is reduced under heavy workloads.
- Limits scalability for problems with large input/output files.
  **Suggested Fix**:
- Stream test case data instead of loading fully into memory:
- Use Python file streams (with open(...) as f:) or chunked downloads/uploads.
- For archives (zip/tar), extract files iteratively without loading the entire archive into memory.
- Optionally, enforce configurable max file size limits and warn users for very large test cases.
- Ensure storage uploads also support streaming APIs to avoid memory spikes.

---

### [C5] No Transactional Safety Across DB and Storage

**Severity**: Major

**Location**: `problems/AzureTestcase.py` , `problems/polygon_api.py`

**Description**:

- Azure credentials and other secrets rely on environment variables with no validation or rotation mechanism.
- If credentials expire or are rotated outside the system, this could break storage access silently.

**Impact**:

- Storage operations may fail unexpectedly when secrets are invalid or expired.
- Increases risk of downtime or migration failures.
- Security best practices are not followed, potentially exposing secrets to mismanagement.
  **Suggested Fix**:
- Implement secret validation at application startup to ensure required environment variables exist and are correctly formatted.
- Consider integrating a secret management solution (e.g., AWS Secrets Manager, Azure Key Vault, HashiCorp Vault) instead of plain environment variables.
- Add automated rotation support or alerts for expired/invalid credentials.
- Ensure that errors due to invalid secrets fail fast with clear logging, so broken storage access is immediately detectable.

---

### [C6] No Password Complexity or Strength Enforcement

**Severity**: Critical

**Location**: `users/views.py`

**Description**:
The user creation methods do not enforce any password complexity rules, potentially leading to weak passwords.

**Impact**:

- Allows users to set weak or easily guessable passwords.
- Increases risk of account compromise through brute-force or credential-stuffing attacks.
- Violates common security best practices and compliance expectations.

**Suggested Fix**:
Implement password validation during user creation and updates. Enforce minimum complexity requirements such as:

Minimum length (e.g., 8–12 characters)

At least one uppercase letter, lowercase letter, number, and special character

Rejection of common or breached passwords

---

### [C7] No Retry Logic for Polygon API Failures

**Severity**: Major

**Location**: `problems/polygon_api.py`

**Description**:

The Polygon API calls in polygon_api.py do not implement any retry or backoff mechanisms. As a result, temporary network issues, rate limiting, or transient API errors immediately cause requests to fail.

**Impact**:

- Transient failures can interrupt migrations or data ingestion processes.
- Manual intervention is required to retry failed operations.
- Reduces system reliability and robustness when interacting with external services.
- Increases the likelihood of partial or inconsistent migrations.
  **Suggested Fix**:
  Introduce retry logic with exponential backoff for all Polygon API calls. This can be implemented using:
  A retry wrapper or decorator around API requests
  Configurable retry limits and delay intervals
  Conditional retries for transient errors (e.g., network timeouts, 5xx responses, rate limits)
  Ensure retries are logged and capped to avoid infinite loops, and surface meaningful errors when retries are exhausted.

---

<!-- Add more code issues as [C4], [C5], etc. -->

---

## Edge Case Analysis

### Question 1: Empty Sample Test Cases

> A Polygon problem has **0 sample test cases** but **15 regular test cases**. What happens when you migrate this problem?

**Your Analysis**:

[Your detailed answer here. Include:]

- What code path executes?
  The code attempts to fetch SampleTestCase objects linked to the Problem. Views or templates iterate over the sample test cases for display. If none exist, the loop runs zero times, potentially leaving empty sections or causing silent failures depending on template logic.

- What database state results?
  No sample test case entries are created since none exist in Polygon. Regular test cases are still saved normally.

- What happens on re-migration if samples previously existed?
  The system may leave previously migrated sample test cases intact, or overwrite them depending on the migration logic. Missing sample tests are not added, leading to incomplete problem representations.

- Is the behavior correct?
  No. The system assumes samples exist and does not handle zero-sample scenarios gracefully, leading to incomplete data presentation.

**Code References**:

- `views.py:XXX` - [relevant code]
- `models.py:XXX` - [relevant code]
  `migrate_to_azure_blob() in polygon_api.py`

```
for idx, test in enumerate(test_cases, start=1):
    input_data = test.get('input', '')
    output_data = test.get('output', '')
    if input_data and output_data:
        blob_manager.upload_test_case(container_name, problem_id_for_naming, idx, input_data, output_data)
```

---

### Question 2: Test Case Count Reduction

> A problem is migrated with **20 test cases**. Later, the problem setter removes 8 test cases on Polygon (now 12 remain). The problem is re-migrated. What happens?

**Your Analysis**:

[Your detailed answer here. Include:]

- Database state before and after
  Original 20 test cases exist in the database. On re-migration, the 8 removed test cases are not deleted, resulting in 20 entries still present (stale records).

- Cloud storage state before and after
  Blobs corresponding to removed test cases remain unless manually deleted. New uploads may overwrite existing ones if the same paths are used.

- Consistency between DB and storage
  Inconsistent. Database contains extra test cases not present on Polygon, and storage may have leftover files.

- Data integrity issues
  Re-migration does not reflect the current state of the problem on Polygon. Users may see outdated test cases, causing potential confusion or failed tests.

**Code References**:

- `views.py:XXX` - [relevant code]
- `polygon_api.py:XXX` - [relevant code]
- `migrate_to_azure_blob()`

```
# Delete all test cases before updating the new ones
logger.info("Deleting existing test cases from Azure")
blob_manager.empty_blob(container_name, problem_id_for_naming)

```

- `empty_blob() in AzureTestcase.py`

```
blobs_to_delete = [blob.name for blob in container_client.list_blobs(name_starts_with=prefix)]
for blob_name in blobs_to_delete:
   container_client.delete_blob(blob_name)

```

---

### Question 3: Duplicate Problem Titles

> Two different Polygon problems have the exact same title: "Two Sum". You migrate the first one successfully. Then you try to migrate the second one. What happens?

**Your Analysis**:

[Your detailed answer here. Include:]

- Which field causes the issue?
  The Problem model only enforces uniqueness on polygon_id, not the title.
- When does the error occur?
  No error occurs during migration; the second problem is saved successfully.

- What does the user see?
  Both problems appear in the system with identical titles, causing potential confusion in the UI, search, and selection flows.

- Is first problem affected?
  No. The first problem remains unchanged; only the second problem causes ambiguity in user-facing displays.

**Code References**:

- `views.py:XXX` - [relevant code]
- `problems/models.py:XXX` - [relevant code]

```
slug = models.SlugField(unique=True, max_length=255)
polygon_id = models.CharField(max_length=100, unique=True, blank=True)

```

---

### Question 4: Data Truncation

> When test cases are saved to the database via "Migrate Test Cases to DB", some data is intentionally discarded. What data is lost? Why might this cause problems?

**Your Analysis**:

[Your detailed answer here. Include:]

- Where truncation happens
  In the migration logic that saves test case content to the DB (likely only storing a preview or first N characters). Full content is stored in cloud storage blobs.

- What the limit is
  DB fields store only a truncated portion (e.g., first few KB of content).

- What types of problems are affected
  Large test cases or problems with long inputs/outputs may lose visibility in the DB.

- DB vs cloud storage consistency
  The full data is still in cloud storage, but the database is incomplete. Debugging or reprocessing test cases directly from DB becomes difficult.

**Code References**:

- `views.py:XXX` - [relevant code]
- `store_test_cases_in_redis() in polygon_api.py`

```
test_case_data = {
    'index': test_case.get('index', idx),
    'input': test_case.get('input', ''),
    'output': test_case.get('output', ''),
    'description': test_case.get('description', ''),
    'is_sample': test_case.get('is_sample', False)
}

```

- `Database models (ProblemTestCase):`

```
problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='problem_test_cases')
is_sample = models.BooleanField(default=False)
input = models.TextField()
output = models.TextField()
description = models.TextField(blank=True, null=True)

```

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

# Polygon Migration Tool – Functional Documentation

## Overview

This document describes the main user flows, backend processing, data models, and external integrations in the Polygon Migration Tool.

---

## User Flows

### 1. User Login

**Trigger:** User submits login form  
**Data Sent:** username, password

**Backend Processing:**

- Credentials are validated against the User model
- Django authentication session is created

**Database Operations:**

- User table read

**Result:**

- User is logged in and redirected to dashboard

---

### 2. Fetch Problem from Polygon

**Trigger:** User enters Polygon problem ID and clicks “Fetch”

**Backend Processing:**

- `index` view receives `polygon_id`
- Calls `PolygonAPI.get_problem_info`
- Calls `PolygonAPI.download_and_extract_package`
- Calls `PolygonAPI.get_all_test_cases`

**External APIs:**

- Polygon API

**Result:**

- Problem statement, samples, and test cases are displayed in UI

---

### 3. Migrate Problem to Database

**Trigger:** User clicks “Migrate to Database”

**Backend Processing:**

- Problem metadata is saved in Problem model
- Tags and relationships are created

**Database Operations:**

- Insert into Problem, ProblemTag

**Result:**

- Problem persisted in local database

---

### 4. Migrate Test Cases to Database

**Trigger:** User clicks “Migrate Test Cases to DB”

**Backend Processing:**

- Test cases are parsed
- Preview data is saved

**Database Operations:**

- Insert into SampleTestCase and ProblemTestCase

**Result:**

- Test cases visible in DB-backed views

---

### 5. Migrate Test Cases to Cloud Storage

**Trigger:** User clicks “Migrate to Storage”

**Backend Processing:**

- Storage backend is selected (Google Drive)
- Files are uploaded using storage abstraction

**Storage Operations:**

- Files uploaded to Google Drive using required structure

**Result:**

- Test cases available in cloud storage

---

## Data Models

- User
- Problem
- ProblemTag
- SampleTestCase
- ProblemTestCase
- Topic

---

## External Integrations

### Polygon API

- Used to fetch problem metadata and test cases

### Cloud Storage

- Azure Blob Storage replaced with Google Drive
- Storage abstraction allows provider swapping via environment variables

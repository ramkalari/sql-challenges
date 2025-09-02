# DuckDB Support

This branch adds DuckDB support alongside the existing SQLite support for SQL challenges.

## Features Added

### Backend Changes

1. **New DuckDB Container (`backend/duckdb_container.py`)**
   - `DuckDBContainer`: Manages isolated DuckDB database files for SQL challenges
   - `DuckDBChallengeManager`: Manages DuckDB challenge execution and validation
   - Similar interface to the existing SQLite container but uses DuckDB Python API

2. **Enhanced Challenge Submission**
   - `ChallengeSubmitRequest` now includes `database_type` field (defaults to "sqlite")
   - Backend automatically routes to appropriate database engine based on selection
   - Supports both "sqlite" and "duckdb" database types

3. **Updated Dependencies**
   - Added `duckdb==1.1.3` to `requirements.txt`

### Frontend Changes

1. **Database Engine Selection UI**
   - Added dropdown selector in challenges page to choose between SQLite and DuckDB
   - Includes helpful description of the differences between the engines
   - User selection is sent with query submission

2. **State Management**
   - Added `databaseType` state variable with "sqlite" as default
   - Frontend sends selected database type to backend with each query

## Usage

### For Users

1. Navigate to the challenges page
2. Select a challenge
3. Choose your preferred database engine:
   - **SQLite**: Traditional relational database (default)
   - **DuckDB**: Analytical database optimized for OLAP workloads
4. Write your SQL query
5. Submit and compare results

### For Developers

The same SQL challenges work with both database engines, but users may notice:
- Different SQL dialect support between SQLite and DuckDB
- Different performance characteristics
- Different function availability

## API Changes

### POST /challenges/{challenge_id}/submit

**Request Body:**
```json
{
  "user_query": "SELECT * FROM table_name",
  "database_type": "sqlite" // or "duckdb"
}
```

The `database_type` field is optional and defaults to "sqlite" for backward compatibility.

## Implementation Details

- Both database engines use the same challenge validation logic
- Temporary database files are created and cleaned up automatically
- DuckDB uses file-based databases (similar to SQLite) for challenge isolation
- Results are normalized to strings for consistent comparison

## Benefits

1. **Educational**: Users can learn differences between OLTP (SQLite) and OLAP (DuckDB) databases
2. **Performance**: DuckDB may perform better on analytical queries
3. **SQL Dialects**: Users can practice with different SQL flavors
4. **Modern Analytics**: Exposure to modern analytical database systems 
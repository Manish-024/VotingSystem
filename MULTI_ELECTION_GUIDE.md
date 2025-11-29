# Multi-Election Feature Guide

## Overview
The Blockchain Voting System now supports running multiple elections simultaneously with a shared voter pool. This allows voters to participate in different elections using the same credentials, while each election maintains its own candidates and blockchain.

## Key Features

### 1. **Multiple Concurrent Elections**
- Run multiple elections at the same time
- Each election has its own independent blockchain
- Separate candidate pools for each election
- Independent voting status tracking per election

### 2. **Shared Voter Pool**
- Voters are registered once and can vote in multiple elections
- Same voter ID and private key work across all elections
- Each voter maintains separate voting status per election
- Voters can vote in election A and election B independently

### 3. **Election Selector**
- Visual dropdown interface on all pages (Admin, Voter, Results)
- Shows election name, status (Active/Inactive), and statistics
- Easy switching between elections
- Real-time updates when switching

## How It Works

### Architecture

```
Global State:
├── elections {}          # Dictionary of all elections
│   ├── election_1 → VotingSystem instance
│   ├── election_2 → VotingSystem instance
│   └── ...
├── current_election_id   # Currently active election ID
└── shared_voters {}      # Voter pool shared across all elections
    ├── V001 → Voter object (with private_key)
    ├── V002 → Voter object
    └── ...
```

### Data Flow

1. **Creating an Election**: 
   - Generates unique election ID: `election_{count}_{timestamp}`
   - Creates new VotingSystem instance
   - Stores in `elections` dictionary
   - Sets as `current_election_id`

2. **Registering Voters**:
   - Checks if voter exists in `shared_voters`
   - If exists: Reuses existing voter with same credentials
   - If new: Creates voter and adds to shared pool
   - Adds voter reference to current election

3. **Registering Candidates**:
   - Candidates are election-specific
   - Each election has its own candidate pool
   - Candidate IDs are unique within each election

4. **Casting Votes**:
   - Voter authenticates with private key
   - Vote is added to the current election's blockchain
   - Voting status updated only for current election
   - Same voter can vote in other elections

## Usage Guide

### For Administrators

#### 1. Create Multiple Elections

**Option A: Via UI**
1. Go to Admin Portal (`/admin`)
2. Fill in "Create New Election" form
3. Enter election name and difficulty
4. Click "Create Election"
5. Repeat for additional elections

**Option B: Via Sample Data**
1. Click "Create Sample Election Data" button
2. This creates one election with 5 candidates and 20 voters
3. Click again to create additional sample elections

#### 2. Switch Between Elections

1. Use the **Election Selector** dropdown at the top of any page
2. Select the election you want to manage
3. Page will reload showing selected election's data
4. All operations (register candidate, start/end, mine) apply to selected election

#### 3. Manage Voters Across Elections

**Adding Same Voters to Multiple Elections:**
```python
# Voters are automatically shared
# When you register V001 in Election 1, 
# you can register the same V001 in Election 2
# They will use the same private key
```

**Example Workflow:**
1. Create Election 1: "Student Council"
2. Register 20 voters (V001-V020)
3. Register 5 candidates for Student Council
4. Create Election 2: "Department Head"
5. Register same voters (V001-V020) - they'll use existing credentials
6. Register 3 different candidates for Department Head
7. Start both elections
8. Voters can now vote in both using same credentials

### For Voters

#### 1. View Available Elections

1. Go to Voter Portal (`/voter`)
2. Use **Election Selector** dropdown to see all elections
3. Each option shows:
   - Election name
   - Status: 🟢 Active or 🔴 Closed

#### 2. Vote in Multiple Elections

1. Select an election from dropdown
2. Enter your Voter ID and Private Key
3. Check your status: "Check Voter Status" button
4. Select candidate and cast vote
5. Switch to another election using dropdown
6. Vote again (if election is active)

**Important Notes:**
- Same credentials work across all elections
- Voting status is tracked separately per election
- Cannot vote twice in the same election
- Can vote in different elections without restrictions

### For Results Viewing

1. Go to Results page (`/results`)
2. Use **Election Selector** to choose election
3. View results specific to that election:
   - Vote counts
   - Percentages
   - Charts
   - Blockchain verification

## API Endpoints

### New Endpoints

#### List All Elections
```http
GET /api/list-elections
```
**Response:**
```json
{
  "success": true,
  "elections": [
    {
      "id": "election_1_1732855234",
      "name": "Student Council Election 2025",
      "is_active": true,
      "candidates": 5,
      "voters": 20,
      "votes": 15
    }
  ],
  "current_election_id": "election_1_1732855234"
}
```

#### Switch Election
```http
POST /api/switch-election
Content-Type: application/json

{
  "election_id": "election_2_1732855567"
}
```
**Response:**
```json
{
  "success": true,
  "message": "Switched to election: Department Head Election 2025"
}
```

### Modified Endpoints

All existing endpoints now operate on the `current_election_id`:
- `/api/register-candidate` - Adds to current election
- `/api/cast-vote` - Votes in current election
- `/api/start-election` - Starts current election
- `/api/end-election` - Ends current election
- `/api/mine-votes` - Mines votes for current election
- `/api/stats` - Returns stats for current election

## Use Cases

### Example 1: University Elections

**Scenario:** University runs multiple concurrent elections

```
Election 1: Student Council (5 candidates, 1000 students)
Election 2: Graduate Representative (3 candidates, 200 students)
Election 3: Faculty Board (4 candidates, 150 faculty members)
```

**Solution:**
- Register all 1350 people as voters once
- Create 3 separate elections
- For Election 1: Add all students
- For Election 2: Add grad students only (subset)
- For Election 3: Add faculty only (subset)
- Each group votes in their respective elections

### Example 2: Organization with Multiple Positions

**Scenario:** Company elects multiple positions simultaneously

```
Election 1: CEO (4 candidates, 500 employees)
Election 2: CTO (3 candidates, 500 employees)
Election 3: CFO (2 candidates, 500 employees)
```

**Solution:**
- Register 500 employees once (shared voter pool)
- Add all employees to all 3 elections
- Employees vote for each position independently
- Results tracked separately per position

### Example 3: Testing and Production Elections

**Scenario:** Test election setup before deploying production

```
Election 1: Test Election (sample data)
Election 2: Production Election (real voters)
```

**Solution:**
- Create test election with sample data
- Test all functionality
- Create production election when ready
- Switch between them for comparison

## Technical Details

### Voter Credentials
- Private keys are generated once per voter
- Stored in `shared_voters` dictionary
- Reused across all elections
- Format: 64-character hexadecimal string

### Blockchain Independence
- Each election has its own blockchain
- Separate genesis blocks
- Independent mining difficulty
- No cross-election dependencies

### Election IDs
- Format: `election_{sequence}_{unix_timestamp}`
- Example: `election_1_1732855234`
- Guaranteed unique
- Sortable chronologically

### Memory Considerations
- All elections stored in memory
- Data lost on server restart
- For production: Add database persistence
- Consider archiving completed elections

## Best Practices

### 1. **Election Naming**
```
✅ Good: "2025 Student Council Election"
✅ Good: "Computer Science Department Head - Spring 2025"
❌ Bad: "Election 1"
❌ Bad: "Test"
```

### 2. **Voter Management**
```
✅ Register voters in first election
✅ Reuse same voter IDs in subsequent elections
✅ Keep voter credentials file safe
❌ Don't create duplicate voter IDs with different data
```

### 3. **Election Lifecycle**
```
1. Create Election
2. Register Candidates
3. Add Voters (existing or new)
4. Start Election
5. Voters Cast Votes
6. Mine Votes Periodically
7. End Election
8. View Results
```

### 4. **Switching Elections**
```
✅ Use dropdown selector in UI
✅ Wait for page reload after switching
✅ Verify current election in stats display
❌ Don't switch while mining is in progress
```

## Troubleshooting

### Problem: Voter can't vote in second election

**Solution:**
1. Check if voter was added to second election
2. Verify using same Voter ID and Private Key
3. Ensure second election is Active
4. Check if already voted (separate status per election)

### Problem: Election selector shows "No elections"

**Solution:**
1. Create at least one election first
2. Refresh the page
3. Check browser console for JavaScript errors
4. Verify server is running

### Problem: Wrong election data showing

**Solution:**
1. Check which election is selected in dropdown
2. Use dropdown to switch to correct election
3. Wait for page to fully reload
4. Verify current election ID in browser console:
   ```javascript
   // In browser console
   fetch('/api/list-elections')
     .then(r => r.json())
     .then(d => console.log(d.current_election_id))
   ```

### Problem: Voter credentials not working

**Solution:**
1. Verify voter exists in shared_voters
2. Check if voter was added to specific election
3. Confirm private key is exactly 64 hex characters
4. Try "Check Voter Status" button first

## Future Enhancements

Potential improvements for multi-election system:

1. **Database Persistence**
   - Save elections to database
   - Restore on server restart
   - Archive completed elections

2. **Voter Groups**
   - Create voter groups/categories
   - Assign groups to elections
   - Bulk voter management

3. **Election Templates**
   - Save election configurations
   - Reuse for similar elections
   - Quick setup from templates

4. **Advanced Analytics**
   - Cross-election voting patterns
   - Voter participation rates
   - Comparative results analysis

5. **Access Control**
   - Election-specific admin roles
   - Voter eligibility rules
   - Candidate approval workflow

6. **Export/Import**
   - Export election data
   - Import voters from CSV
   - Backup/restore functionality

## Security Considerations

1. **Private Key Management**
   - Private keys are sensitive
   - Store voter credentials file securely
   - Never share private keys publicly
   - Consider encryption at rest

2. **Election Integrity**
   - Each blockchain is independent
   - Verify blockchain after mining
   - Regular integrity checks
   - Audit logs (future enhancement)

3. **Voter Authentication**
   - Require private key for all votes
   - Check voting status before accepting vote
   - Prevent double voting per election
   - Log all voting attempts

4. **Admin Access**
   - Protect admin endpoints
   - Add authentication (future enhancement)
   - Audit admin actions
   - Limit election modifications after start

## Conclusion

The multi-election feature provides flexibility for organizations running multiple voting processes. It maintains the security and transparency of blockchain-based voting while allowing efficient management of concurrent elections with shared voter pools.

For questions or issues, check the main README.md or create an issue in the repository.

# 🎲 Sample Data Guide

This guide explains how to populate your blockchain voting system with sample data for testing.

## Method 1: Using the Web Interface (Easiest!)

1. **Start the web server** (if not already running):
   ```bash
   source venv/bin/activate
   python app.py
   ```

2. **Open the Admin Portal**: http://127.0.0.1:5000/admin

3. **Click the "🎲 Create Sample Election Data" button**
   - This will automatically create:
     - ✅ 1 Election: "University Student Council Election 2025"
     - ✅ 5 Candidates from different parties
     - ✅ 20 Voters with unique credentials

4. **Save the voter credentials** that appear in the popup
   - You can download them as a text file
   - You'll need these to test voting!

## Method 2: Using the Python Script

Run the sample data generator:

```bash
source venv/bin/activate
python create_sample_data.py
```

Then choose:
- **Option 1**: Create election with candidates and voters only
- **Option 2**: Create election with some sample votes already cast

The script will save voter credentials to `sample_voter_credentials.txt`

## Sample Election Details

### 🏛️ Election
**Name**: University Student Council Election 2025  
**Difficulty**: 2 (Balanced mining speed)

### 👥 Candidates

| ID | Name | Party | Focus |
|----|------|-------|-------|
| C001 | Sarah Johnson | Progressive Student Alliance | Mental health, sustainability, housing |
| C002 | Michael Chen | Academic Excellence Party | Study resources, research, careers |
| C003 | Aisha Patel | Diversity & Inclusion Coalition | Equal opportunities, cultural events |
| C004 | James Rodriguez | Sports & Wellness Movement | Athletic facilities, wellness |
| C005 | Emily Thompson | Independent | Non-partisan, transparent governance |

### 🗳️ Voters (Sample)

First 3 voters (check `sample_voter_credentials.txt` for all 20):

- **V001** - Alice Williams (alice.williams@university.edu)
- **V002** - Bob Martinez (bob.martinez@university.edu)
- **V003** - Charlie Brown (charlie.brown@university.edu)

## Testing the Voting System

### Step-by-Step Testing:

1. **Go to Admin Portal** and create sample data (if not done)

2. **Start the Election**:
   - Click "▶️ Start Election" in the Admin Portal

3. **Cast Votes** as different voters:
   - Go to Voter Portal: http://127.0.0.1:5000/voter
   - Use credentials from the saved file
   - Example:
     - Voter ID: `V001`
     - Private Key: `[from credentials file]`
     - Select a candidate and vote

4. **Mine the Votes** (Admin Portal):
   - Click "⛏️ Mine Pending Votes"
   - Watch the blockchain mining process!

5. **View Results**:
   - Go to: http://127.0.0.1:5000/results
   - See vote distribution charts
   - Verify blockchain integrity

## Quick Test Scenario

Here's a quick test you can run:

```bash
# 1. Create sample data
python create_sample_data.py
# Choose option 2 (with sample votes)

# 2. Open web interface
# Admin: http://127.0.0.1:5000/admin
# Voter: http://127.0.0.1:5000/voter
# Results: http://127.0.0.1:5000/results
```

This creates an election with 12 votes already cast and mined!

## Sample Voter Credentials Format

```
Voter ID: V001
Name: Alice Williams
Private Key: [64-character hexadecimal string]
```

**⚠️ Important**: Keep voter credentials secure! In a real election, these would be distributed securely to eligible voters.

## Troubleshooting

### "No election created" message
- Make sure you clicked the "Create Sample Election Data" button
- Or run `python create_sample_data.py` first

### "Voter not registered" error
- Double-check the Voter ID (case-sensitive: V001, V002, etc.)
- Make sure you're using the correct credentials from the file

### "Invalid private key" error
- Copy the entire private key (it's a long hexadecimal string)
- Make sure there are no extra spaces

### "Voter has already voted" error
- Each voter can only vote once
- Try a different voter ID

## Advanced: Custom Sample Data

Want to create your own sample data? Edit `create_sample_data.py`:

```python
# Add more candidates
("C006", "Your Name", "Your Party", "Your description")

# Add more voters
("V021", "Voter Name", "email@example.com")
```

## Need Help?

Check the main README.md for more information or contact the administrator.

---

**Happy Testing!** 🎉🗳️⛓️

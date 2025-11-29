# Blockchain-Based Voting System

A secure, transparent, and tamper-proof voting system built using blockchain technology. This system ensures election integrity through cryptographic hashing and proof-of-work consensus mechanism.

## Features

### 🔐 Security Features
- **Blockchain Technology**: All votes are stored in an immutable blockchain
- **Cryptographic Hashing**: SHA-256 hashing for data integrity
- **Proof of Work**: Mining algorithm to secure blocks
- **Private Key Authentication**: Each voter receives a unique private key
- **Tamper Detection**: Built-in blockchain validation

### 🗳️ Voting Features
- **Voter Registration**: Secure voter registration with unique IDs
- **Candidate Registration**: Register multiple candidates with party affiliations
- **Real-time Voting**: Cast votes during active election periods
- **Vote Mining**: Batch process votes into blockchain blocks
- **Results Calculation**: Automated vote counting from blockchain
- **Election Management**: Start/stop elections with timestamp tracking

### 📊 Administrative Features
- **Election Statistics**: View voter turnout, candidate counts, and more
- **Blockchain Verification**: Validate blockchain integrity at any time
- **Results Display**: Formatted election results with percentages
- **Data Export**: Export complete election data and blockchain

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download the project:
```bash
cd /Users/I527873/Documents/BITS/VotingSystem
```

2. (Optional) Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Application (Recommended)

1. Start the web server:
```bash
python app.py
```

2. Open your browser and navigate to:
   - **Home**: http://127.0.0.1:5000
   - **Admin Portal**: http://127.0.0.1:5000/admin
   - **Voter Portal**: http://127.0.0.1:5000/voter
   - **Results**: http://127.0.0.1:5000/results

### Running the CLI Application

Start the command-line voting system:
```bash
python main.py
```

### Quick Start Guide

#### For Administrators:

1. **Create an Election**
   - Select "Administrator Portal"
   - Choose "Create New Election"
   - Enter election name and difficulty level (1-4)

2. **Register Candidates**
   - Select "Register Candidate"
   - Enter candidate ID, name, party, and description

3. **Register Voters**
   - Select "Register Voter"
   - Enter voter ID, name, and email
   - **Important**: Save the generated private key!

4. **Start Election**
   - Select "Start Election" when ready

5. **Mine Votes**
   - Periodically select "Mine Pending Votes" to add votes to blockchain

6. **End Election**
   - Select "End Election" when voting period is over
   - View results and verify blockchain integrity

#### For Voters:

1. **View Candidates**
   - Select "Voter Portal"
   - Choose "View Candidates" to see all options

2. **Cast Vote**
   - Select "Cast Vote"
   - Enter your voter ID and private key
   - Select your preferred candidate

3. **Check Status**
   - Select "Check Voting Status" to verify if you've voted

### Running the Demo

To see the system in action with sample data:
```bash
python demo.py
```

## Screenshots & Features

### Web Interface Features:

#### 🏠 Home Page
- Modern landing page with feature highlights
- Clear navigation to Admin and Voter portals
- Information about blockchain security benefits

#### 🔐 Admin Portal
- Create and manage elections
- Register voters and candidates
- Start/stop elections
- Mine pending votes into blockchain
- Verify blockchain integrity
- Real-time statistics dashboard

#### 🗳️ Voter Portal
- View all registered candidates
- Cast secure votes using private key
- Check voting status
- User-friendly interface

#### 📊 Results Page
- Visual vote distribution charts
- Detailed results table with percentages
- Winner announcement
- Blockchain verification

## Project Structure

```
VotingSystem/
├── blockchain.py              # Core blockchain implementation
├── voting_system.py           # Voting system logic
├── app.py                     # Flask web application
├── main.py                    # CLI application interface
├── demo.py                    # Demonstration script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── index.html            # Home page
│   ├── admin.html            # Admin portal
│   ├── voter.html            # Voter portal
│   └── results.html          # Results page
└── static/                    # Static assets
    ├── css/
    │   └── style.css         # Stylesheet
    └── js/
        ├── main.js           # Common JavaScript
        ├── admin.js          # Admin functionality
        └── voter.js          # Voter functionality
```

## Architecture

### Components

1. **Blockchain (`blockchain.py`)**
   - `Transaction`: Represents a vote
   - `Block`: Contains multiple transactions with hash
   - `Blockchain`: Manages the chain of blocks

2. **Voting System (`voting_system.py`)**
   - `Voter`: Represents a registered voter
   - `Candidate`: Represents an election candidate
   - `VotingSystem`: Main system orchestrator

3. **Application (`main.py`)**
   - `VotingApp`: CLI interface for users

### How It Works

1. **Vote Casting**: When a voter casts a vote, a transaction is created
2. **Pending Pool**: Votes are stored in a pending transaction pool
3. **Mining**: Admin mines pending votes into a new block using PoW
4. **Blockchain**: Mined block is added to the immutable blockchain
5. **Validation**: System can verify blockchain integrity at any time
6. **Results**: Final results are calculated from all blockchain transactions

## Security Considerations

### Implemented Security Features:
- ✅ Immutable blockchain ledger
- ✅ Cryptographic hashing (SHA-256)
- ✅ Proof of Work consensus
- ✅ Private key authentication
- ✅ Double-voting prevention
- ✅ Blockchain integrity verification

### Production Recommendations:
- 🔸 Implement digital signatures (RSA/ECDSA)
- 🔸 Add network distribution (P2P network)
- 🔸 Implement secure key management (HSM)
- 🔸 Add voter identity verification
- 🔸 Implement encrypted storage
- 🔸 Add audit logging
- 🔸 Implement rate limiting
- 🔸 Add two-factor authentication

## Technical Details

### Blockchain Parameters
- **Hashing Algorithm**: SHA-256
- **Consensus Mechanism**: Proof of Work
- **Default Difficulty**: 2 (configurable 1-4)
- **Block Structure**: Index, Transactions, Previous Hash, Timestamp, Nonce, Hash

### Mining Process
The mining difficulty determines how many leading zeros the block hash must have:
- Difficulty 1: Faster mining, less secure (development)
- Difficulty 2: Balanced (default)
- Difficulty 3-4: Slower mining, more secure (production)

## Example Usage

```python
from voting_system import VotingSystem

# Create election
election = VotingSystem("Presidential Election 2025", difficulty=2)

# Register candidates
election.register_candidate("C001", "Alice Johnson", "Progressive Party")
election.register_candidate("C002", "Bob Smith", "Conservative Party")

# Register voters
voter1 = election.register_voter("V001", "John Doe", "john@example.com")
voter2 = election.register_voter("V002", "Jane Smith", "jane@example.com")

# Start election
election.start_election()

# Cast votes
election.cast_vote("V001", "C001", voter1.private_key)
election.cast_vote("V002", "C002", voter2.private_key)

# Mine votes
election.mine_votes()

# End election and view results
election.end_election()
election.display_results()

# Verify integrity
election.verify_blockchain_integrity()
```

## Testing

Run the demo script to test all functionality:
```bash
python demo.py
```

This will:
- Create a sample election
- Register candidates and voters
- Simulate voting
- Mine votes into blockchain
- Display results
- Verify blockchain integrity

## Limitations

This is an educational implementation demonstrating blockchain concepts. For production use, consider:

- Network distribution (currently single-node)
- Advanced cryptography (digital signatures)
- Database persistence
- Scalability optimization
- Legal compliance requirements
- Accessibility features
- Multi-language support

## Contributing

This is an educational project. Feel free to:
- Add new features
- Improve security
- Enhance user interface
- Add tests
- Improve documentation

## License

This project is provided as-is for educational purposes.

## Author

Created as a demonstration of blockchain technology applied to voting systems.

## Acknowledgments

- Blockchain concepts inspired by Bitcoin and Ethereum
- Cryptography using Python's hashlib library
- Educational implementation for learning purposes

---

**⚠️ Disclaimer**: This is an educational implementation and should not be used for real elections without significant security enhancements, legal compliance verification, and professional security auditing.

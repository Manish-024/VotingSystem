"""
Voting System implementation using blockchain technology.
Includes Voter, Candidate, and VotingSystem classes.
"""

import hashlib
import secrets
from typing import List, Dict, Optional
from datetime import datetime
from blockchain import Blockchain, Transaction


class Voter:
    """Represents a voter in the system."""
    
    def __init__(self, voter_id: str, name: str, email: str):
        self.voter_id = voter_id
        self.name = name
        self.email = email
        self.has_voted = False
        self.private_key = self._generate_private_key()
    
    def _generate_private_key(self) -> str:
        """Generate a unique private key for the voter."""
        return hashlib.sha256(
            f"{self.voter_id}{self.name}{secrets.token_hex(16)}".encode()
        ).hexdigest()
    
    def to_dict(self) -> Dict:
        """Convert voter to dictionary (without private key)."""
        return {
            'voter_id': self.voter_id,
            'name': self.name,
            'email': self.email,
            'has_voted': self.has_voted
        }
    
    def __repr__(self):
        return f"Voter(id={self.voter_id}, name={self.name}, voted={self.has_voted})"


class Candidate:
    """Represents a candidate in the election."""
    
    def __init__(self, candidate_id: str, name: str, party: str, description: str = ""):
        self.candidate_id = candidate_id
        self.name = name
        self.party = party
        self.description = description
    
    def to_dict(self) -> Dict:
        """Convert candidate to dictionary."""
        return {
            'candidate_id': self.candidate_id,
            'name': self.name,
            'party': self.party,
            'description': self.description
        }
    
    def __repr__(self):
        return f"Candidate(id={self.candidate_id}, name={self.name}, party={self.party})"


class VotingSystem:
    """Main voting system that manages elections using blockchain."""
    
    def __init__(self, election_name: str, difficulty: int = 2):
        self.election_name = election_name
        self.blockchain = Blockchain(difficulty=difficulty)
        self.voters: Dict[str, Voter] = {}
        self.candidates: Dict[str, Candidate] = {}
        self.is_active = False
        self.start_time = None
        self.end_time = None
    
    def register_voter(self, voter_id: str, name: str, email: str) -> Optional[Voter]:
        """Register a new voter."""
        if voter_id in self.voters:
            print(f"Voter {voter_id} already registered.")
            return None
        
        voter = Voter(voter_id, name, email)
        self.voters[voter_id] = voter
        print(f"Voter registered: {voter.name} (ID: {voter_id})")
        return voter
    
    def register_candidate(self, candidate_id: str, name: str, party: str, 
                          description: str = "") -> Optional[Candidate]:
        """Register a new candidate."""
        if candidate_id in self.candidates:
            print(f"Candidate {candidate_id} already registered.")
            return None
        
        candidate = Candidate(candidate_id, name, party, description)
        self.candidates[candidate_id] = candidate
        print(f"Candidate registered: {candidate.name} ({party})")
        return candidate
    
    def start_election(self):
        """Start the election."""
        if self.is_active:
            print("Election is already active.")
            return
        
        if not self.candidates:
            print("Cannot start election: No candidates registered.")
            return
        
        self.is_active = True
        self.start_time = datetime.now()
        print(f"Election '{self.election_name}' started at {self.start_time}")
    
    def end_election(self):
        """End the election and mine remaining votes."""
        if not self.is_active:
            print("Election is not active.")
            return
        
        self.is_active = False
        self.end_time = datetime.now()
        
        # Mine any pending transactions
        if self.blockchain.pending_transactions:
            print("Mining final votes...")
            self.blockchain.mine_pending_transactions()
        
        print(f"Election '{self.election_name}' ended at {self.end_time}")
    
    def cast_vote(self, voter_id: str, candidate_id: str, private_key: str) -> bool:
        """Cast a vote for a candidate."""
        # Check if election is active
        if not self.is_active:
            print("Error: Election is not active.")
            return False
        
        # Check if voter exists
        if voter_id not in self.voters:
            print("Error: Voter not registered.")
            return False
        
        voter = self.voters[voter_id]
        
        # Verify private key
        if voter.private_key != private_key:
            print("Error: Invalid private key.")
            return False
        
        # Check if voter has already voted
        if voter.has_voted:
            print("Error: Voter has already cast their vote.")
            return False
        
        # Check if candidate exists
        if candidate_id not in self.candidates:
            print("Error: Candidate not found.")
            return False
        
        # Create and add transaction
        transaction = Transaction(voter_id, candidate_id)
        self.blockchain.add_transaction(transaction)
        voter.has_voted = True
        
        print(f"Vote cast successfully by {voter.name} for {self.candidates[candidate_id].name}")
        return True
    
    def mine_votes(self):
        """Mine pending votes into the blockchain."""
        if not self.blockchain.pending_transactions:
            print("No votes to mine.")
            return
        
        print(f"Mining {len(self.blockchain.pending_transactions)} votes...")
        self.blockchain.mine_pending_transactions()
        print("Votes successfully added to blockchain.")
    
    def get_results(self) -> Dict[str, int]:
        """Calculate and return election results."""
        results = {candidate_id: 0 for candidate_id in self.candidates}
        
        # Count votes from blockchain
        all_transactions = self.blockchain.get_all_transactions()
        for transaction in all_transactions:
            if transaction.candidate_id in results:
                results[transaction.candidate_id] += 1
        
        return results
    
    def display_results(self):
        """Display election results in a formatted way."""
        print(f"\n{'='*60}")
        print(f"Election Results: {self.election_name}")
        print(f"{'='*60}")
        
        results = self.get_results()
        total_votes = sum(results.values())
        
        # Sort by vote count (descending)
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        
        print(f"\nTotal Votes Cast: {total_votes}")
        print(f"Total Registered Voters: {len(self.voters)}")
        print(f"Voter Turnout: {(total_votes/len(self.voters)*100) if self.voters else 0:.2f}%\n")
        
        print(f"{'Rank':<6} {'Candidate':<25} {'Party':<20} {'Votes':<10} {'Percentage':<10}")
        print("-" * 71)
        
        for rank, (candidate_id, votes) in enumerate(sorted_results, 1):
            candidate = self.candidates[candidate_id]
            percentage = (votes / total_votes * 100) if total_votes > 0 else 0
            print(f"{rank:<6} {candidate.name:<25} {candidate.party:<20} {votes:<10} {percentage:.2f}%")
        
        print(f"{'='*60}\n")
    
    def verify_blockchain_integrity(self) -> bool:
        """Verify the integrity of the blockchain."""
        is_valid = self.blockchain.is_chain_valid()
        if is_valid:
            print("✓ Blockchain integrity verified: All votes are secure and tamper-proof.")
        else:
            print("✗ Blockchain integrity check FAILED: Potential tampering detected!")
        return is_valid
    
    def get_voter_count(self) -> int:
        """Get the total number of registered voters."""
        return len(self.voters)
    
    def get_candidate_count(self) -> int:
        """Get the total number of registered candidates."""
        return len(self.candidates)
    
    def get_votes_cast(self) -> int:
        """Get the total number of votes cast."""
        return len(self.blockchain.get_all_transactions())
    
    def export_election_data(self) -> Dict:
        """Export all election data."""
        return {
            'election_name': self.election_name,
            'is_active': self.is_active,
            'start_time': str(self.start_time) if self.start_time else None,
            'end_time': str(self.end_time) if self.end_time else None,
            'voters': [voter.to_dict() for voter in self.voters.values()],
            'candidates': [candidate.to_dict() for candidate in self.candidates.values()],
            'results': self.get_results(),
            'blockchain': self.blockchain.export_chain()
        }
    
    def __repr__(self):
        return (f"VotingSystem(election={self.election_name}, "
                f"voters={len(self.voters)}, candidates={len(self.candidates)}, "
                f"active={self.is_active})")

"""
Blockchain implementation for the voting system.
Each block contains votes as transactions with cryptographic hashing for security.
"""

import hashlib
import json
from time import time
from typing import List, Dict, Any


class Transaction:
    """Represents a vote transaction in the blockchain."""
    
    def __init__(self, voter_id: str, candidate_id: str, timestamp: float = None):
        self.voter_id = voter_id
        self.candidate_id = candidate_id
        self.timestamp = timestamp or time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary."""
        return {
            'voter_id': self.voter_id,
            'candidate_id': self.candidate_id,
            'timestamp': self.timestamp
        }
    
    def __repr__(self):
        return f"Transaction(voter_id={self.voter_id}, candidate_id={self.candidate_id})"


class Block:
    """Represents a block in the blockchain."""
    
    def __init__(self, index: int, transactions: List[Transaction], 
                 previous_hash: str, timestamp: float = None, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time()
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate the hash of the block using SHA-256."""
        block_string = json.dumps({
            'index': self.index,
            'transactions': [t.to_dict() for t in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2):
        """Mine the block using Proof of Work algorithm."""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary."""
        return {
            'index': self.index,
            'transactions': [t.to_dict() for t in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'hash': self.hash
        }
    
    def __repr__(self):
        return f"Block(index={self.index}, hash={self.hash[:10]}..., transactions={len(self.transactions)})"


class Blockchain:
    """Manages the blockchain for the voting system."""
    
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = 0  # No reward for voting system
        
        # Create genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain."""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Add a transaction to pending transactions."""
        if not transaction.voter_id or not transaction.candidate_id:
            return False
        
        self.pending_transactions.append(transaction)
        return True
    
    def mine_pending_transactions(self):
        """Mine pending transactions into a new block."""
        if not self.pending_transactions:
            print("No transactions to mine.")
            return
        
        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )
        block.mine_block(self.difficulty)
        
        self.chain.append(block)
        self.pending_transactions = []
    
    def is_chain_valid(self) -> bool:
        """Validate the integrity of the blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if hash is correct
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash at block {i}")
                return False
        
        return True
    
    def get_all_transactions(self) -> List[Transaction]:
        """Get all transactions from the blockchain."""
        all_transactions = []
        for block in self.chain[1:]:  # Skip genesis block
            all_transactions.extend(block.transactions)
        return all_transactions
    
    def export_chain(self) -> List[Dict[str, Any]]:
        """Export the blockchain to a list of dictionaries."""
        return [block.to_dict() for block in self.chain]
    
    def __repr__(self):
        return f"Blockchain(blocks={len(self.chain)}, valid={self.is_chain_valid()})"

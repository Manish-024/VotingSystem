"""
Demonstration script for the Blockchain-based Voting System.
This script showcases all features of the system with sample data.
"""

from voting_system import VotingSystem
import time


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo():
    """Run a complete demonstration of the voting system."""
    
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  BLOCKCHAIN-BASED VOTING SYSTEM - DEMONSTRATION".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Step 1: Create Election
    print_section("STEP 1: Creating Election")
    election = VotingSystem("Presidential Election 2025", difficulty=2)
    print("✓ Election created successfully!")
    print(f"  Election Name: {election.election_name}")
    print(f"  Mining Difficulty: {election.blockchain.difficulty}")
    
    # Step 2: Register Candidates
    print_section("STEP 2: Registering Candidates")
    candidates_data = [
        ("C001", "Alice Johnson", "Progressive Party", "Focus on education and healthcare"),
        ("C002", "Bob Smith", "Conservative Party", "Strong economy and national security"),
        ("C003", "Carol Martinez", "Green Party", "Environmental protection and sustainability"),
        ("C004", "David Chen", "Independent", "Unity and bipartisan cooperation")
    ]
    
    for candidate_id, name, party, description in candidates_data:
        election.register_candidate(candidate_id, name, party, description)
    
    print(f"\n✓ Total candidates registered: {election.get_candidate_count()}")
    
    # Step 3: Register Voters
    print_section("STEP 3: Registering Voters")
    voters_data = [
        ("V001", "John Doe", "john.doe@email.com"),
        ("V002", "Jane Smith", "jane.smith@email.com"),
        ("V003", "Michael Brown", "michael.brown@email.com"),
        ("V004", "Emily Davis", "emily.davis@email.com"),
        ("V005", "Robert Wilson", "robert.wilson@email.com"),
        ("V006", "Sarah Johnson", "sarah.johnson@email.com"),
        ("V007", "James Lee", "james.lee@email.com"),
        ("V008", "Lisa Anderson", "lisa.anderson@email.com"),
        ("V009", "William Taylor", "william.taylor@email.com"),
        ("V010", "Maria Garcia", "maria.garcia@email.com")
    ]
    
    voter_objects = {}
    for voter_id, name, email in voters_data:
        voter = election.register_voter(voter_id, name, email)
        if voter:
            voter_objects[voter_id] = voter
    
    print(f"\n✓ Total voters registered: {election.get_voter_count()}")
    print("✓ Each voter has been assigned a unique private key")
    
    # Step 4: Start Election
    print_section("STEP 4: Starting Election")
    election.start_election()
    print(f"✓ Election is now ACTIVE")
    print(f"✓ Started at: {election.start_time}")
    
    # Step 5: Cast Votes
    print_section("STEP 5: Casting Votes")
    print("Voters are now casting their votes...\n")
    
    # Simulate voting with different preferences
    vote_distribution = {
        "V001": "C001",  # Alice
        "V002": "C001",  # Alice
        "V003": "C002",  # Bob
        "V004": "C001",  # Alice
        "V005": "C003",  # Carol
        "V006": "C002",  # Bob
        "V007": "C001",  # Alice
        "V008": "C004",  # David
        "V009": "C002",  # Bob
        "V010": "C001",  # Alice
    }
    
    for voter_id, candidate_id in vote_distribution.items():
        voter = voter_objects[voter_id]
        success = election.cast_vote(voter_id, candidate_id, voter.private_key)
        if success:
            time.sleep(0.1)  # Small delay for demonstration
    
    print(f"\n✓ Total votes cast: {len(vote_distribution)}")
    print(f"✓ Pending votes (not yet mined): {len(election.blockchain.pending_transactions)}")
    
    # Step 6: Mine Votes (Part 1)
    print_section("STEP 6: Mining Votes into Blockchain")
    print("Mining votes in batches...\n")
    
    # Mine all pending votes
    election.mine_votes()
    
    print(f"\n✓ All votes have been added to the blockchain")
    print(f"✓ Total blocks in chain: {len(election.blockchain.chain)}")
    
    # Step 7: Verify Blockchain Integrity
    print_section("STEP 7: Verifying Blockchain Integrity")
    election.verify_blockchain_integrity()
    
    # Step 8: View Statistics
    print_section("STEP 8: Election Statistics")
    print(f"Election Name: {election.election_name}")
    print(f"Status: {'Active' if election.is_active else 'Inactive'}")
    print(f"Registered Voters: {election.get_voter_count()}")
    print(f"Votes Cast: {election.get_votes_cast()}")
    print(f"Voter Turnout: {(election.get_votes_cast()/election.get_voter_count()*100):.2f}%")
    print(f"Registered Candidates: {election.get_candidate_count()}")
    print(f"Blockchain Blocks: {len(election.blockchain.chain)}")
    print(f"Blockchain Valid: {election.blockchain.is_chain_valid()}")
    
    # Step 9: End Election
    print_section("STEP 9: Ending Election")
    election.end_election()
    print(f"✓ Election ended at: {election.end_time}")
    
    # Step 10: Display Results
    print_section("STEP 10: Final Election Results")
    election.display_results()
    
    # Step 11: Show Winner
    print_section("ELECTION WINNER")
    results = election.get_results()
    winner_id = max(results, key=results.get)
    winner = election.candidates[winner_id]
    winner_votes = results[winner_id]
    total_votes = sum(results.values())
    percentage = (winner_votes / total_votes * 100) if total_votes > 0 else 0
    
    print(f"🏆 WINNER: {winner.name}")
    print(f"   Party: {winner.party}")
    print(f"   Votes: {winner_votes} ({percentage:.2f}%)")
    print()
    
    # Step 12: Demonstrate Security
    print_section("STEP 11: Demonstrating Security Features")
    
    print("1. Testing Double Voting Prevention:")
    print("   Attempting to vote again with voter V001...")
    voter1 = voter_objects["V001"]
    
    # Try to vote again (should fail)
    election.is_active = True  # Temporarily reactivate
    success = election.cast_vote("V001", "C002", voter1.private_key)
    if not success:
        print("   ✓ Double voting prevented successfully!")
    election.is_active = False
    
    print("\n2. Testing Invalid Private Key:")
    print("   Attempting to vote with wrong private key...")
    election.is_active = True
    success = election.cast_vote("V002", "C001", "wrong_private_key")
    if not success:
        print("   ✓ Invalid private key rejected successfully!")
    election.is_active = False
    
    print("\n3. Blockchain Integrity Check:")
    print("   Verifying all blocks are properly chained...")
    if election.verify_blockchain_integrity():
        print("   ✓ Blockchain integrity confirmed!")
    
    print("\n4. Immutability Demonstration:")
    print("   Blockchain is immutable - any tampering would be detected")
    print("   Each block contains the hash of the previous block")
    print("   Changing any vote would change all subsequent hashes")
    
    # Final Summary
    print_section("DEMONSTRATION COMPLETE")
    print("Key Features Demonstrated:")
    print("  ✓ Secure voter registration with private keys")
    print("  ✓ Candidate registration and management")
    print("  ✓ Tamper-proof vote recording")
    print("  ✓ Blockchain mining with Proof of Work")
    print("  ✓ Double voting prevention")
    print("  ✓ Private key authentication")
    print("  ✓ Blockchain integrity verification")
    print("  ✓ Transparent vote counting")
    print("  ✓ Immutable audit trail")
    print()
    print("The voting system successfully:")
    print(f"  • Registered {election.get_voter_count()} voters")
    print(f"  • Registered {election.get_candidate_count()} candidates")
    print(f"  • Recorded {election.get_votes_cast()} votes")
    print(f"  • Created {len(election.blockchain.chain)} blockchain blocks")
    print(f"  • Maintained 100% blockchain integrity")
    print()
    print("=" * 70)
    
    return election


def interactive_demo():
    """Run an interactive demonstration."""
    print("\nWould you like to:")
    print("1. Run automated demonstration")
    print("2. Exit")
    
    try:
        choice = input("\nEnter choice (1-2): ").strip()
        if choice == "1":
            demo()
        else:
            print("Exiting...")
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")


if __name__ == "__main__":
    interactive_demo()

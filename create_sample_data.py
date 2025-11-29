"""
Sample Data Generator for Blockchain Voting System
This script creates sample elections, candidates, and voters for testing.
"""

from voting_system import VotingSystem


def create_sample_election():
    """Create a sample election with candidates and voters."""
    
    print("\n" + "="*70)
    print("  CREATING SAMPLE ELECTION DATA")
    print("="*70 + "\n")
    
    # Create election
    print("📋 Creating election...")
    election = VotingSystem("University Student Council Election 2025", difficulty=2)
    print(f"✓ Election created: {election.election_name}\n")
    
    # Register Candidates
    print("👥 Registering candidates...")
    candidates_data = [
        {
            "id": "C001",
            "name": "Sarah Johnson",
            "party": "Progressive Student Alliance",
            "description": "Focusing on mental health support, campus sustainability, and affordable housing"
        },
        {
            "id": "C002",
            "name": "Michael Chen",
            "party": "Academic Excellence Party",
            "description": "Prioritizing study resources, research funding, and career development programs"
        },
        {
            "id": "C003",
            "name": "Aisha Patel",
            "party": "Diversity & Inclusion Coalition",
            "description": "Championing equal opportunities, cultural events, and international student support"
        },
        {
            "id": "C004",
            "name": "James Rodriguez",
            "party": "Sports & Wellness Movement",
            "description": "Enhancing athletic facilities, wellness programs, and student recreation"
        },
        {
            "id": "C005",
            "name": "Emily Thompson",
            "party": "Independent",
            "description": "Non-partisan approach to student advocacy and transparent governance"
        }
    ]
    
    for candidate in candidates_data:
        election.register_candidate(
            candidate["id"],
            candidate["name"],
            candidate["party"],
            candidate["description"]
        )
    
    print(f"\n✓ Registered {len(candidates_data)} candidates\n")
    
    # Register Voters
    print("🗳️  Registering voters...")
    voters_data = [
        {"id": "V001", "name": "Alice Williams", "email": "alice.williams@university.edu"},
        {"id": "V002", "name": "Bob Martinez", "email": "bob.martinez@university.edu"},
        {"id": "V003", "name": "Charlie Brown", "email": "charlie.brown@university.edu"},
        {"id": "V004", "name": "Diana Prince", "email": "diana.prince@university.edu"},
        {"id": "V005", "name": "Ethan Hunt", "email": "ethan.hunt@university.edu"},
        {"id": "V006", "name": "Fiona Chen", "email": "fiona.chen@university.edu"},
        {"id": "V007", "name": "George Kumar", "email": "george.kumar@university.edu"},
        {"id": "V008", "name": "Hannah Lee", "email": "hannah.lee@university.edu"},
        {"id": "V009", "name": "Ian Smith", "email": "ian.smith@university.edu"},
        {"id": "V010", "name": "Julia Anderson", "email": "julia.anderson@university.edu"},
        {"id": "V011", "name": "Kevin Nguyen", "email": "kevin.nguyen@university.edu"},
        {"id": "V012", "name": "Laura Garcia", "email": "laura.garcia@university.edu"},
        {"id": "V013", "name": "Marcus Johnson", "email": "marcus.johnson@university.edu"},
        {"id": "V014", "name": "Nina Patel", "email": "nina.patel@university.edu"},
        {"id": "V015", "name": "Oliver Davis", "email": "oliver.davis@university.edu"},
        {"id": "V016", "name": "Priya Sharma", "email": "priya.sharma@university.edu"},
        {"id": "V017", "name": "Quinn Wilson", "email": "quinn.wilson@university.edu"},
        {"id": "V018", "name": "Rachel Kim", "email": "rachel.kim@university.edu"},
        {"id": "V019", "name": "Samuel Lee", "email": "samuel.lee@university.edu"},
        {"id": "V020", "name": "Tina Zhang", "email": "tina.zhang@university.edu"}
    ]
    
    voter_credentials = []
    for voter_data in voters_data:
        voter = election.register_voter(
            voter_data["id"],
            voter_data["name"],
            voter_data["email"]
        )
        if voter:
            voter_credentials.append({
                "id": voter.voter_id,
                "name": voter.name,
                "private_key": voter.private_key
            })
    
    print(f"\n✓ Registered {len(voter_credentials)} voters\n")
    
    # Save voter credentials to file
    print("💾 Saving voter credentials...")
    with open('sample_voter_credentials.txt', 'w') as f:
        f.write("="*70 + "\n")
        f.write("  VOTER CREDENTIALS - KEEP THIS SECURE!\n")
        f.write("="*70 + "\n\n")
        f.write(f"Election: {election.election_name}\n\n")
        f.write("Use these credentials to test voting:\n\n")
        
        for cred in voter_credentials:
            f.write(f"Voter ID: {cred['id']}\n")
            f.write(f"Name: {cred['name']}\n")
            f.write(f"Private Key: {cred['private_key']}\n")
            f.write("-"*70 + "\n\n")
    
    print("✓ Credentials saved to: sample_voter_credentials.txt\n")
    
    # Display sample credentials
    print("="*70)
    print("  SAMPLE VOTER CREDENTIALS (First 3 voters)")
    print("="*70 + "\n")
    
    for cred in voter_credentials[:3]:
        print(f"🔑 Voter ID: {cred['id']}")
        print(f"   Name: {cred['name']}")
        print(f"   Private Key: {cred['private_key']}")
        print()
    
    print("📄 Full list saved in: sample_voter_credentials.txt\n")
    
    # Summary
    print("="*70)
    print("  SUMMARY")
    print("="*70)
    print(f"\n✓ Election Created: {election.election_name}")
    print(f"✓ Candidates: {election.get_candidate_count()}")
    print(f"✓ Registered Voters: {election.get_voter_count()}")
    print(f"✓ Status: {'Active' if election.is_active else 'Ready to Start'}")
    print(f"\n⚠️  Next Steps:")
    print(f"   1. Go to Admin Portal to START the election")
    print(f"   2. Use voter credentials to cast votes")
    print(f"   3. Mine votes in Admin Portal")
    print(f"   4. View results when done!")
    print("\n" + "="*70 + "\n")
    
    return election, voter_credentials


def create_sample_with_votes():
    """Create a sample election and cast some votes."""
    
    print("\n" + "="*70)
    print("  CREATING SAMPLE ELECTION WITH PRE-CAST VOTES")
    print("="*70 + "\n")
    
    # Create election with candidates and voters
    election, voter_credentials = create_sample_election()
    
    # Start the election
    print("\n🚀 Starting election...")
    election.start_election()
    
    # Cast some sample votes
    print("\n🗳️  Casting sample votes...\n")
    
    vote_distribution = [
        ("V001", "C001"),  # Alice votes for Sarah
        ("V002", "C001"),  # Bob votes for Sarah
        ("V003", "C002"),  # Charlie votes for Michael
        ("V004", "C001"),  # Diana votes for Sarah
        ("V005", "C003"),  # Ethan votes for Aisha
        ("V006", "C002"),  # Fiona votes for Michael
        ("V007", "C001"),  # George votes for Sarah
        ("V008", "C004"),  # Hannah votes for James
        ("V009", "C002"),  # Ian votes for Michael
        ("V010", "C001"),  # Julia votes for Sarah
        ("V011", "C005"),  # Kevin votes for Emily
        ("V012", "C003"),  # Laura votes for Aisha
    ]
    
    votes_cast = 0
    for voter_id, candidate_id in vote_distribution:
        # Find the voter's private key
        private_key = None
        for cred in voter_credentials:
            if cred["id"] == voter_id:
                private_key = cred["private_key"]
                break
        
        if private_key:
            success = election.cast_vote(voter_id, candidate_id, private_key)
            if success:
                votes_cast += 1
    
    print(f"\n✓ Cast {votes_cast} votes")
    
    # Mine the votes
    print("\n⛏️  Mining votes into blockchain...\n")
    election.mine_votes()
    
    # Display results
    print("\n📊 Current Results:\n")
    election.display_results()
    
    # Verify blockchain
    print("\n🔒 Verifying blockchain integrity...\n")
    election.verify_blockchain_integrity()
    
    print("\n" + "="*70)
    print("  SAMPLE DATA WITH VOTES CREATED SUCCESSFULLY!")
    print("="*70)
    print(f"\n✓ Election is ACTIVE")
    print(f"✓ {votes_cast} votes have been cast and mined")
    print(f"✓ {len(voter_credentials) - votes_cast} voters haven't voted yet")
    print(f"✓ You can still cast more votes with remaining voter credentials")
    print(f"\n📄 All credentials saved in: sample_voter_credentials.txt")
    print("\n" + "="*70 + "\n")
    
    return election, voter_credentials


if __name__ == "__main__":
    import sys
    
    print("\n🗳️  SAMPLE DATA GENERATOR FOR BLOCKCHAIN VOTING SYSTEM\n")
    print("Choose an option:")
    print("1. Create election with candidates and voters only")
    print("2. Create election with sample votes already cast")
    print("0. Exit\n")
    
    try:
        choice = input("Enter your choice (0-2): ").strip()
        
        if choice == "1":
            create_sample_election()
        elif choice == "2":
            create_sample_with_votes()
        elif choice == "0":
            print("Exiting...")
        else:
            print("Invalid choice. Please run again and select 1 or 2.")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n\nError: {e}")

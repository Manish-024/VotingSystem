"""
Main application interface for the Blockchain-based Voting System.
Provides a command-line interface for both administrators and voters.
"""

import sys
from voting_system import VotingSystem


class VotingApp:
    """Command-line application for the voting system."""
    
    def __init__(self):
        self.system = None
    
    def clear_screen(self):
        """Clear the console screen."""
        print("\n" * 2)
    
    def display_menu(self, title: str, options: list):
        """Display a menu with options."""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        print(f"  0. Back/Exit")
        print(f"{'='*60}")
    
    def get_choice(self, max_option: int) -> int:
        """Get user's menu choice."""
        while True:
            try:
                choice = int(input("\nEnter your choice: "))
                if 0 <= choice <= max_option:
                    return choice
                print(f"Please enter a number between 0 and {max_option}")
            except ValueError:
                print("Please enter a valid number")
    
    def admin_menu(self):
        """Administrator menu."""
        while True:
            options = [
                "Create New Election",
                "Register Voter",
                "Register Candidate",
                "Start Election",
                "End Election",
                "Mine Pending Votes",
                "View Election Results",
                "Verify Blockchain Integrity",
                "View Election Statistics"
            ]
            
            self.display_menu("ADMINISTRATOR MENU", options)
            choice = self.get_choice(len(options))
            
            if choice == 0:
                break
            elif choice == 1:
                self.create_election()
            elif choice == 2:
                self.register_voter()
            elif choice == 3:
                self.register_candidate()
            elif choice == 4:
                self.start_election()
            elif choice == 5:
                self.end_election()
            elif choice == 6:
                self.mine_votes()
            elif choice == 7:
                self.view_results()
            elif choice == 8:
                self.verify_integrity()
            elif choice == 9:
                self.view_statistics()
    
    def voter_menu(self):
        """Voter menu."""
        while True:
            options = [
                "View Candidates",
                "Cast Vote",
                "Check Voting Status"
            ]
            
            self.display_menu("VOTER MENU", options)
            choice = self.get_choice(len(options))
            
            if choice == 0:
                break
            elif choice == 1:
                self.view_candidates()
            elif choice == 2:
                self.cast_vote()
            elif choice == 3:
                self.check_voting_status()
    
    def create_election(self):
        """Create a new election."""
        print("\n--- Create New Election ---")
        election_name = input("Enter election name: ").strip()
        
        if not election_name:
            print("Error: Election name cannot be empty.")
            return
        
        try:
            difficulty = int(input("Enter mining difficulty (1-4, default 2): ") or "2")
            if difficulty < 1 or difficulty > 4:
                difficulty = 2
        except ValueError:
            difficulty = 2
        
        self.system = VotingSystem(election_name, difficulty)
        print(f"\n✓ Election '{election_name}' created successfully!")
    
    def register_voter(self):
        """Register a new voter."""
        if not self.system:
            print("\nError: Please create an election first.")
            return
        
        print("\n--- Register Voter ---")
        voter_id = input("Enter voter ID: ").strip()
        name = input("Enter voter name: ").strip()
        email = input("Enter voter email: ").strip()
        
        if not all([voter_id, name, email]):
            print("Error: All fields are required.")
            return
        
        voter = self.system.register_voter(voter_id, name, email)
        if voter:
            print(f"\n✓ Voter registered successfully!")
            print(f"Private Key: {voter.private_key}")
            print("\n⚠️  IMPORTANT: Save this private key! It's needed to vote.")
    
    def register_candidate(self):
        """Register a new candidate."""
        if not self.system:
            print("\nError: Please create an election first.")
            return
        
        print("\n--- Register Candidate ---")
        candidate_id = input("Enter candidate ID: ").strip()
        name = input("Enter candidate name: ").strip()
        party = input("Enter party name: ").strip()
        description = input("Enter description (optional): ").strip()
        
        if not all([candidate_id, name, party]):
            print("Error: ID, name, and party are required.")
            return
        
        candidate = self.system.register_candidate(candidate_id, name, party, description)
        if candidate:
            print(f"\n✓ Candidate registered successfully!")
    
    def start_election(self):
        """Start the election."""
        if not self.system:
            print("\nError: Please create an election first.")
            return
        
        self.system.start_election()
    
    def end_election(self):
        """End the election."""
        if not self.system:
            print("\nError: Please create an election first.")
            return
        
        self.system.end_election()
    
    def mine_votes(self):
        """Mine pending votes."""
        if not self.system:
            print("\nError: Please create an election first.")
            return
        
        self.system.mine_votes()
    
    def view_candidates(self):
        """View all registered candidates."""
        if not self.system:
            print("\nError: Please create an election first.")
            return
        
        if not self.system.candidates:
            print("\nNo candidates registered yet.")
            return
        
        print(f"\n{'='*60}")
        print("REGISTERED CANDIDATES")
        print(f"{'='*60}")
        
        for candidate in self.system.candidates.values():
            print(f"\nID: {candidate.candidate_id}")
            print(f"Name: {candidate.name}")
            print(f"Party: {candidate.party}")
            if candidate.description:
                print(f"Description: {candidate.description}")
            print("-" * 60)
    
    def cast_vote(self):
        """Cast a vote."""
        if not self.system:
            print("\nError: Please create an election first.")
            return
        
        if not self.system.is_active:
            print("\nError: Election is not currently active.")
            return
        
        print("\n--- Cast Vote ---")
        voter_id = input("Enter your voter ID: ").strip()
        private_key = input("Enter your private key: ").strip()
        
        # Show candidates
        self.view_candidates()
        
        candidate_id = input("\nEnter candidate ID to vote for: ").strip()
        
        if self.system.cast_vote(voter_id, candidate_id, private_key):
            print("\n✓ Your vote has been recorded!")
            print("Your vote will be added to the blockchain when mined.")
    
    def check_voting_status(self):
        """Check if a voter has voted."""
        if not self.system:
            print("\nError: Please create an election first.")
            return
        
        voter_id = input("\nEnter your voter ID: ").strip()
        
        if voter_id in self.system.voters:
            voter = self.system.voters[voter_id]
            print(f"\nVoter: {voter.name}")
            print(f"Email: {voter.email}")
            print(f"Voting Status: {'✓ Voted' if voter.has_voted else '✗ Not voted yet'}")
        else:
            print("\nVoter not found.")
    
    def view_results(self):
        """View election results."""
        if not self.system:
            print("\nError: Please create an election first.")
            return
        
        self.system.display_results()
    
    def verify_integrity(self):
        """Verify blockchain integrity."""
        if not self.system:
            print("\nError: Please create an election first.")
            return
        
        print("\n--- Blockchain Integrity Check ---")
        self.system.verify_blockchain_integrity()
    
    def view_statistics(self):
        """View election statistics."""
        if not self.system:
            print("\nError: Please create an election first.")
            return
        
        print(f"\n{'='*60}")
        print("ELECTION STATISTICS")
        print(f"{'='*60}")
        print(f"Election Name: {self.system.election_name}")
        print(f"Status: {'Active' if self.system.is_active else 'Inactive'}")
        print(f"Registered Voters: {self.system.get_voter_count()}")
        print(f"Registered Candidates: {self.system.get_candidate_count()}")
        print(f"Votes Cast: {self.system.get_votes_cast()}")
        print(f"Pending Votes: {len(self.system.blockchain.pending_transactions)}")
        print(f"Blockchain Blocks: {len(self.system.blockchain.chain)}")
        print(f"{'='*60}")
    
    def main_menu(self):
        """Main menu."""
        print("\n")
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 58 + "║")
        print("║" + "    BLOCKCHAIN-BASED VOTING SYSTEM".center(58) + "║")
        print("║" + " " * 58 + "║")
        print("╚" + "═" * 58 + "╝")
        
        while True:
            options = [
                "Administrator Portal",
                "Voter Portal"
            ]
            
            self.display_menu("MAIN MENU", options)
            choice = self.get_choice(len(options))
            
            if choice == 0:
                print("\nThank you for using the Blockchain Voting System!")
                sys.exit(0)
            elif choice == 1:
                self.admin_menu()
            elif choice == 2:
                self.voter_menu()
    
    def run(self):
        """Run the application."""
        try:
            self.main_menu()
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    app = VotingApp()
    app.run()


if __name__ == "__main__":
    main()

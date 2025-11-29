"""
Web application for the Blockchain-based Voting System.
Provides a modern web UI using Flask.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from voting_system import VotingSystem
import secrets
import os
import time

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Disable caching for development
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(response):
    """Add headers to prevent caching"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# Global storage for multiple elections
elections = {}  # {election_id: VotingSystem}
current_election_id = None
shared_voters = {}  # {voter_id: Voter} - shared across elections


@app.route('/')
def index():
    """Home page."""
    election_list = [{'id': eid, 'name': e.election_name, 'is_active': e.is_active} 
                     for eid, e in elections.items()]
    return render_template('index.html', elections=election_list, 
                         current_election_id=current_election_id)


@app.route('/admin')
def admin():
    """Admin dashboard."""
    global current_election_id
    voting_system = elections.get(current_election_id) if current_election_id else None
    
    stats = None
    if voting_system:
        stats = {
            'election_name': voting_system.election_name,
            'is_active': voting_system.is_active,
            'voter_count': voting_system.get_voter_count(),
            'candidate_count': voting_system.get_candidate_count(),
            'votes_cast': voting_system.get_votes_cast(),
            'pending_votes': len(voting_system.blockchain.pending_transactions),
            'blockchain_blocks': len(voting_system.blockchain.chain),
            'blockchain_valid': voting_system.blockchain.is_chain_valid()
        }
    
    election_list = [{'id': eid, 'name': e.election_name, 'is_active': e.is_active} 
                     for eid, e in elections.items()]
    
    return render_template('admin.html', stats=stats, system_exists=voting_system is not None,
                         elections=election_list, current_election_id=current_election_id,
                         shared_voter_count=len(shared_voters))


@app.route('/voter')
def voter():
    """Voter portal."""
    global current_election_id
    voting_system = elections.get(current_election_id) if current_election_id else None
    
    if not voting_system:
        election_list = [{'id': eid, 'name': e.election_name, 'is_active': e.is_active} 
                        for eid, e in elections.items()]
        return render_template('voter.html', system_exists=False, elections=election_list)
    
    candidates = [c.to_dict() for c in voting_system.candidates.values()]
    election_list = [{'id': eid, 'name': e.election_name, 'is_active': e.is_active} 
                     for eid, e in elections.items()]
    
    return render_template('voter.html', 
                         system_exists=True,
                         election_name=voting_system.election_name,
                         election_id=current_election_id,
                         is_active=voting_system.is_active,
                         candidates=candidates,
                         elections=election_list,
                         current_election_id=current_election_id)


@app.route('/results')
def results():
    """View election results."""
    global current_election_id
    voting_system = elections.get(current_election_id) if current_election_id else None
    
    election_list = [{'id': eid, 'name': e.election_name, 'is_active': e.is_active} 
                     for eid, e in elections.items()]
    
    if not voting_system:
        return render_template('results.html', system_exists=False, elections=election_list)
    
    results_data = voting_system.get_results()
    candidates_info = []
    total_votes = sum(results_data.values())
    
    for candidate_id, votes in sorted(results_data.items(), key=lambda x: x[1], reverse=True):
        candidate = voting_system.candidates[candidate_id]
        percentage = (votes / total_votes * 100) if total_votes > 0 else 0
        candidates_info.append({
            'id': candidate_id,
            'name': candidate.name,
            'party': candidate.party,
            'votes': votes,
            'percentage': round(percentage, 2)
        })
    
    stats = {
        'election_name': voting_system.election_name,
        'election_id': current_election_id,
        'total_votes': total_votes,
        'total_voters': voting_system.get_voter_count(),
        'turnout': round((total_votes / voting_system.get_voter_count() * 100) if voting_system.get_voter_count() > 0 else 0, 2)
    }
    
    return render_template('results.html', 
                         system_exists=True,
                         stats=stats,
                         candidates=candidates_info,
                         elections=election_list,
                         current_election_id=current_election_id)


# API Routes
@app.route('/api/create-election', methods=['POST'])
def api_create_election():
    """API: Create new election."""
    global current_election_id
    data = request.json
    election_name = data.get('election_name')
    difficulty = int(data.get('difficulty', 2))
    
    if not election_name:
        return jsonify({'success': False, 'message': 'Election name is required'})
    
    # Create unique election ID
    election_id = f"election_{len(elections) + 1}_{secrets.token_hex(4)}"
    
    # Create new election
    new_election = VotingSystem(election_name, difficulty)
    
    # Copy shared voters to new election
    for voter_id, voter in shared_voters.items():
        new_election.voters[voter_id] = voter
    
    elections[election_id] = new_election
    current_election_id = election_id
    
    return jsonify({
        'success': True, 
        'message': f'Election "{election_name}" created successfully',
        'election_id': election_id
    })


@app.route('/api/switch-election', methods=['POST'])
def api_switch_election():
    """API: Switch to a different election."""
    global current_election_id
    data = request.json
    election_id = data.get('election_id')
    
    if not election_id or election_id not in elections:
        return jsonify({'success': False, 'message': 'Invalid election ID'})
    
    current_election_id = election_id
    return jsonify({
        'success': True, 
        'message': f'Switched to {elections[election_id].election_name}'
    })


@app.route('/api/register-voter', methods=['POST'])
def api_register_voter():
    """API: Register a new voter (shared across all elections)."""
    data = request.json
    voter_id = data.get('voter_id')
    name = data.get('name')
    email = data.get('email')
    
    if not all([voter_id, name, email]):
        return jsonify({'success': False, 'message': 'All fields are required'})
    
    # Check if voter already exists in shared voters
    if voter_id in shared_voters:
        return jsonify({'success': False, 'message': 'Voter ID already exists'})
    
    # Create voter using any election (or create temporary one)
    from voting_system import Voter
    voter = Voter(voter_id, name, email)
    
    # Add to shared voters
    shared_voters[voter_id] = voter
    
    # Add to all existing elections
    for election in elections.values():
        election.voters[voter_id] = voter
    
    return jsonify({
        'success': True, 
        'message': f'Voter {name} registered successfully for all elections',
        'private_key': voter.private_key
    })


@app.route('/api/register-candidate', methods=['POST'])
def api_register_candidate():
    """API: Register a new candidate."""
    global current_election_id
    voting_system = elections.get(current_election_id) if current_election_id else None
    
    if not voting_system:
        return jsonify({'success': False, 'message': 'Please create or select an election first'})
    
    data = request.json
    candidate_id = data.get('candidate_id')
    name = data.get('name')
    party = data.get('party')
    description = data.get('description', '')
    
    if not all([candidate_id, name, party]):
        return jsonify({'success': False, 'message': 'ID, name, and party are required'})
    
    candidate = voting_system.register_candidate(candidate_id, name, party, description)
    if candidate:
        return jsonify({'success': True, 'message': f'Candidate {name} registered successfully'})
    else:
        return jsonify({'success': False, 'message': 'Candidate ID already exists'})


@app.route('/api/list-elections', methods=['GET'])
def api_list_elections():
    """API: List all elections."""
    election_list = []
    for eid, vs in elections.items():
        election_list.append({
            'id': eid,
            'name': vs.election_name,
            'is_active': vs.is_active,
            'candidates': len(vs.candidates),
            'voters': len(vs.voters),
            'votes': vs.get_votes_cast()
        })
    return jsonify({
        'success': True,
        'elections': election_list,
        'current_election_id': current_election_id
    })


@app.route('/api/start-election', methods=['POST'])
def api_start_election():
    """API: Start the election."""
    global current_election_id
    if not current_election_id or current_election_id not in elections:
        return jsonify({'success': False, 'message': 'Please create an election first'})
    
    voting_system = elections[current_election_id]
    if voting_system.is_active:
        return jsonify({'success': False, 'message': 'Election is already active'})
    
    if not voting_system.candidates:
        return jsonify({'success': False, 'message': 'Cannot start election: No candidates registered'})
    
    voting_system.start_election()
    return jsonify({'success': True, 'message': 'Election started successfully'})


@app.route('/api/end-election', methods=['POST'])
def api_end_election():
    """API: End the election."""
    global current_election_id
    if not current_election_id or current_election_id not in elections:
        return jsonify({'success': False, 'message': 'Please create an election first'})
    
    voting_system = elections[current_election_id]
    if not voting_system.is_active:
        return jsonify({'success': False, 'message': 'Election is not active'})
    
    voting_system.end_election()
    return jsonify({'success': True, 'message': 'Election ended successfully'})


@app.route('/api/mine-votes', methods=['POST'])
def api_mine_votes():
    """API: Mine pending votes."""
    global current_election_id
    if not current_election_id or current_election_id not in elections:
        return jsonify({'success': False, 'message': 'Please create an election first'})
    
    voting_system = elections[current_election_id]
    pending_count = len(voting_system.blockchain.pending_transactions)
    if pending_count == 0:
        return jsonify({'success': False, 'message': 'No votes to mine'})
    
    voting_system.mine_votes()
    
    # Get the newly mined block details
    latest_block = voting_system.blockchain.get_latest_block()
    
    return jsonify({
        'success': True, 
        'message': f'{pending_count} votes mined successfully',
        'block_hash': latest_block.hash,
        'block_index': latest_block.index,
        'block_nonce': latest_block.nonce,
        'transaction_count': len(latest_block.transactions)
    })


@app.route('/api/cast-vote', methods=['POST'])
def api_cast_vote():
    """API: Cast a vote."""
    global current_election_id
    if not current_election_id or current_election_id not in elections:
        return jsonify({'success': False, 'message': 'Please create an election first'})
    
    voting_system = elections[current_election_id]
    data = request.json
    voter_id = data.get('voter_id')
    candidate_id = data.get('candidate_id')
    private_key = data.get('private_key')
    
    if not all([voter_id, candidate_id, private_key]):
        return jsonify({'success': False, 'message': 'All fields are required'})
    
    success = voting_system.cast_vote(voter_id, candidate_id, private_key)
    if success:
        # Get the transaction that was just added
        pending_txs = voting_system.blockchain.pending_transactions
        if pending_txs:
            latest_tx = pending_txs[-1]
            # Calculate a hash for this transaction
            import hashlib
            import json as json_module
            tx_data = json_module.dumps(latest_tx.to_dict(), sort_keys=True)
            tx_hash = hashlib.sha256(tx_data.encode()).hexdigest()
            
            return jsonify({
                'success': True, 
                'message': 'Vote cast successfully!',
                'transaction_hash': tx_hash,
                'transaction_id': f"TX-{latest_tx.timestamp}",
                'pending_count': len(pending_txs)
            })
        return jsonify({'success': True, 'message': 'Vote cast successfully!'})
    else:
        return jsonify({'success': False, 'message': 'Vote casting failed. Check your credentials.'})


@app.route('/api/check-status', methods=['POST'])
def api_check_status():
    """API: Check voter status."""
    global current_election_id
    if not current_election_id or current_election_id not in elections:
        return jsonify({'success': False, 'message': 'Please create an election first'})
    
    voting_system = elections[current_election_id]
    data = request.json
    voter_id = data.get('voter_id')
    
    if voter_id not in voting_system.voters:
        return jsonify({'success': False, 'message': 'Voter not found'})
    
    voter = voting_system.voters[voter_id]
    return jsonify({
        'success': True,
        'voter': {
            'name': voter.name,
            'email': voter.email,
            'has_voted': voter.has_voted
        }
    })


@app.route('/api/verify-blockchain', methods=['GET'])
def api_verify_blockchain():
    """API: Verify blockchain integrity."""
    global current_election_id
    if not current_election_id or current_election_id not in elections:
        return jsonify({'success': False, 'message': 'Please create an election first'})
    
    voting_system = elections[current_election_id]
    is_valid = voting_system.blockchain.is_chain_valid()
    return jsonify({
        'success': True,
        'is_valid': is_valid,
        'message': 'Blockchain is valid ✓' if is_valid else 'Blockchain integrity check FAILED ✗'
    })


@app.route('/api/blockchain-data', methods=['GET'])
def api_blockchain_data():
    """API: Get detailed blockchain data with all hashes."""
    global current_election_id
    if not current_election_id or current_election_id not in elections:
        return jsonify({'success': False, 'message': 'Please create an election first'})
    
    voting_system = elections[current_election_id]
    blockchain = voting_system.blockchain
    
    # Get all blocks with hash information
    blocks_data = []
    for block in blockchain.chain:
        blocks_data.append({
            'index': block.index,
            'hash': block.hash,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'nonce': block.nonce,
            'transaction_count': len(block.transactions),
            'transactions': [t.to_dict() for t in block.transactions]
        })
    
    # Get pending transactions
    pending_data = [t.to_dict() for t in blockchain.pending_transactions]
    
    return jsonify({
        'success': True,
        'blocks': blocks_data,
        'pending_transactions': pending_data,
        'total_blocks': len(blockchain.chain),
        'difficulty': blockchain.difficulty,
        'is_valid': blockchain.is_chain_valid()
    })


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """API: Get election statistics."""
    global current_election_id
    if not current_election_id or current_election_id not in elections:
        return jsonify({'success': False, 'message': 'No election created'})
    
    voting_system = elections[current_election_id]
    return jsonify({
        'success': True,
        'stats': {
            'election_name': voting_system.election_name,
            'is_active': voting_system.is_active,
            'voter_count': voting_system.get_voter_count(),
            'candidate_count': voting_system.get_candidate_count(),
            'votes_cast': voting_system.get_votes_cast(),
            'pending_votes': len(voting_system.blockchain.pending_transactions),
            'blockchain_blocks': len(voting_system.blockchain.chain),
            'blockchain_valid': voting_system.blockchain.is_chain_valid()
        }
    })


@app.route('/api/create-sample-data', methods=['POST'])
def api_create_sample_data():
    """API: Create sample election data."""
    global current_election_id, shared_voters
    
    # Determine which election to create based on count
    election_count = len(elections) + 1
    election_id = f"election_{election_count}_{int(time.time())}"
    
    # Different election types with different candidates
    election_templates = [
        {
            "name": "University Student Council Election 2025",
            "candidates": [
                ("C001", "Sarah Johnson", "Progressive Student Alliance", 
                 "Focusing on mental health support, campus sustainability, and affordable housing"),
                ("C002", "Michael Chen", "Academic Excellence Party", 
                 "Prioritizing study resources, research funding, and career development programs"),
                ("C003", "Aisha Patel", "Diversity & Inclusion Coalition", 
                 "Championing equal opportunities, cultural events, and international student support"),
                ("C004", "James Rodriguez", "Sports & Wellness Movement", 
                 "Enhancing athletic facilities, wellness programs, and student recreation"),
                ("C005", "Emily Thompson", "Independent", 
                 "Non-partisan approach to student advocacy and transparent governance")
            ]
        },
        {
            "name": "Computer Science Department Head Election 2025",
            "candidates": [
                ("D001", "Dr. Alan Turing", "Innovation & Research Party", 
                 "Advancing AI and quantum computing research, securing research grants"),
                ("D002", "Dr. Grace Hopper", "Software Engineering Alliance", 
                 "Modernizing curriculum with industry partnerships and internship programs"),
                ("D003", "Dr. Donald Knuth", "Academic Excellence Society", 
                 "Strengthening theoretical foundations and promoting academic publishing"),
            ]
        },
        {
            "name": "Campus President Election 2025",
            "candidates": [
                ("P001", "Jennifer Martinez", "Unity Coalition", 
                 "Building bridges between departments and fostering campus-wide collaboration"),
                ("P002", "David Thompson", "Reform Party", 
                 "Restructuring administration for efficiency and transparency"),
                ("P003", "Sophia Lee", "Progressive Movement", 
                 "Championing environmental sustainability and social justice initiatives"),
                ("P004", "Robert Kim", "Traditional Values Party", 
                 "Preserving academic traditions while embracing necessary innovation"),
            ]
        },
        {
            "name": "Graduate Student Representative Election 2025",
            "candidates": [
                ("G001", "Maya Patel", "Graduate Advocacy Group", 
                 "Fighting for better stipends, healthcare, and work-life balance"),
                ("G002", "Alex Johnson", "Research Excellence Party", 
                 "Improving research facilities and securing conference funding"),
                ("G003", "Chris Anderson", "Independent Graduate Voice", 
                 "Non-partisan representation focusing on student welfare"),
            ]
        },
        {
            "name": "Faculty Senate Chair Election 2025",
            "candidates": [
                ("F001", "Prof. Elizabeth Warren", "Faculty First Coalition", 
                 "Advocating for faculty rights, tenure protection, and academic freedom"),
                ("F002", "Prof. James Foster", "Collaborative Leadership Party", 
                 "Promoting interdisciplinary research and administrative cooperation"),
                ("F003", "Prof. Maria Garcia", "Innovation in Education Group", 
                 "Transforming teaching methods with technology and pedagogy research"),
            ]
        }
    ]
    
    # Select template (cycle through them, or use first for first election)
    template_index = (election_count - 1) % len(election_templates)
    template = election_templates[template_index]
    
    # Create election with template data
    voting_system = VotingSystem(template["name"], difficulty=2)
    elections[election_id] = voting_system
    current_election_id = election_id
    
    # Register Candidates from template
    candidates_data = template["candidates"]
    
    for cid, name, party, desc in candidates_data:
        voting_system.register_candidate(cid, name, party, desc)
    
    # Register Voters (shared pool)
    voters_data = [
        ("V001", "Alice Williams", "alice.williams@university.edu"),
        ("V002", "Bob Martinez", "bob.martinez@university.edu"),
        ("V003", "Charlie Brown", "charlie.brown@university.edu"),
        ("V004", "Diana Prince", "diana.prince@university.edu"),
        ("V005", "Ethan Hunt", "ethan.hunt@university.edu"),
        ("V006", "Fiona Chen", "fiona.chen@university.edu"),
        ("V007", "George Kumar", "george.kumar@university.edu"),
        ("V008", "Hannah Lee", "hannah.lee@university.edu"),
        ("V009", "Ian Smith", "ian.smith@university.edu"),
        ("V010", "Julia Anderson", "julia.anderson@university.edu"),
        ("V011", "Kevin Nguyen", "kevin.nguyen@university.edu"),
        ("V012", "Laura Garcia", "laura.garcia@university.edu"),
        ("V013", "Marcus Johnson", "marcus.johnson@university.edu"),
        ("V014", "Nina Patel", "nina.patel@university.edu"),
        ("V015", "Oliver Davis", "oliver.davis@university.edu"),
        ("V016", "Priya Sharma", "priya.sharma@university.edu"),
        ("V017", "Quinn Wilson", "quinn.wilson@university.edu"),
        ("V018", "Rachel Kim", "rachel.kim@university.edu"),
        ("V019", "Samuel Lee", "samuel.lee@university.edu"),
        ("V020", "Tina Zhang", "tina.zhang@university.edu")
    ]
    
    voter_credentials = []
    for vid, name, email in voters_data:
        # Check if voter already exists in shared pool
        if vid in shared_voters:
            voter = shared_voters[vid]
            # Add existing voter to this election
            voting_system.voters[vid] = voter
        else:
            # Create new voter and add to shared pool
            voter = voting_system.register_voter(vid, name, email)
            if voter:
                shared_voters[vid] = voter
        
        if voter:
            voter_credentials.append({
                'voter_id': vid,
                'name': name,
                'private_key': voter.private_key
            })
    
    return jsonify({
        'success': True,
        'message': f'Sample election created with {len(candidates_data)} candidates and {len(voters_data)} voters',
        'election_id': election_id,
        'voter_credentials': voter_credentials
    })


if __name__ == '__main__':
    print("\n" + "="*70)
    print("  BLOCKCHAIN VOTING SYSTEM - Web Interface")
    print("="*70)
    
    # Get port from environment variable (for Render/Railway/Heroku) or default to 5001 (avoiding macOS AirPlay on 5000)
    port = int(os.environ.get('PORT', 5001))
    # Use 0.0.0.0 for cloud deployment, 127.0.0.1 for local
    host = os.environ.get('HOST', '0.0.0.0' if os.environ.get('PORT') else '127.0.0.1')
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"\n  🌐 Starting server at http://{host}:{port}")
    print("  📊 Admin Portal: http://{host}:{port}/admin".replace('{host}', host).replace('{port}', str(port)))
    print("  🗳️  Voter Portal: http://{host}:{port}/voter".replace('{host}', host).replace('{port}', str(port)))
    print("  📈 Results: http://{host}:{port}/results".replace('{host}', host).replace('{port}', str(port)))
    print("\n  Press CTRL+C to stop the server\n")
    print("="*70 + "\n")
    
    app.run(debug=debug, host=host, port=port)

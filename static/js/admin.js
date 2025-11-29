// Admin Portal JavaScript

// Load latest block hash
async function loadLatestBlockHash() {
    try {
        const result = await apiRequest('/api/blockchain-data', 'GET');
        if (result.success && result.blocks.length > 0) {
            const latestBlock = result.blocks[result.blocks.length - 1];
            document.getElementById('latestHashValue').textContent = latestBlock.hash;
            document.getElementById('latestBlockIndex').textContent = latestBlock.index;
            document.getElementById('latestBlockNonce').textContent = latestBlock.nonce;
            document.getElementById('latestBlockTxCount').textContent = latestBlock.transaction_count;
        }
    } catch (error) {
        console.error('Failed to load latest block hash:', error);
    }
}

// Load elections on page load
async function loadElections() {
    try {
        const result = await apiRequest('/api/list-elections', 'GET');
        if (result.success) {
            const select = document.getElementById('electionSelect');
            select.innerHTML = '';
            
            if (result.elections.length === 0) {
                select.innerHTML = '<option value="">No elections created</option>';
            } else {
                result.elections.forEach(election => {
                    const option = document.createElement('option');
                    option.value = election.id;
                    option.textContent = `${election.name} (${election.candidates} candidates, ${election.votes} votes)`;
                    if (election.id === result.current_election_id) {
                        option.selected = true;
                    }
                    select.appendChild(option);
                });
            }
        }
        
        // Load latest block hash after loading elections
        loadLatestBlockHash();
    } catch (error) {
        console.error('Failed to load elections:', error);
    }
}

// Switch election - Setup event listener
document.addEventListener('DOMContentLoaded', () => {
    const electionSelect = document.getElementById('electionSelect');
    if (electionSelect) {
        electionSelect.addEventListener('change', async () => {
            const electionId = electionSelect.value;
            if (electionId) {
                try {
                    const result = await apiRequest('/api/switch-election', 'POST', {
                        election_id: electionId
                    });
                    if (result.success) {
                        showNotification('Switched to election: ' + electionId, 'success');
                        // Reload page to update all stats and data
                        setTimeout(() => location.reload(), 500);
                    }
                } catch (error) {
                    showNotification('Failed to switch election', 'error');
                }
            }
        });
    }
    
    // Load elections when page loads
    loadElections();
});

// Create Election
document.getElementById('createElectionForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const electionName = document.getElementById('electionName').value;
    const difficulty = document.getElementById('difficulty').value;
    
    try {
        const result = await apiRequest('/api/create-election', 'POST', {
            election_name: electionName,
            difficulty: parseInt(difficulty)
        });
        
        if (result.success) {
            showNotification(result.message, 'success');
            clearForm('createElectionForm');
            await loadElections();
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        showNotification('Failed to create election', 'error');
    }
});

// Register Voter
document.getElementById('registerVoterForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const voterId = document.getElementById('voterId').value;
    const name = document.getElementById('voterName').value;
    const email = document.getElementById('voterEmail').value;
    
    try {
        const result = await apiRequest('/api/register-voter', 'POST', {
            voter_id: voterId,
            name: name,
            email: email
        });
        
        if (result.success) {
            showNotification(result.message, 'success');
            clearForm('registerVoterForm');
            
            // Display private key
            const privateKeyDisplay = document.getElementById('privateKeyDisplay');
            const privateKeyValue = document.getElementById('privateKeyValue');
            privateKeyValue.textContent = result.private_key;
            privateKeyDisplay.style.display = 'block';
            
            // Add click to copy
            privateKeyValue.style.cursor = 'pointer';
            privateKeyValue.title = 'Click to copy';
            privateKeyValue.onclick = () => copyToClipboard(result.private_key);
            
            // Don't reload - private key is already displayed
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        showNotification('Failed to register voter', 'error');
    }
});

// Register Candidate
document.getElementById('registerCandidateForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const candidateId = document.getElementById('candidateId').value;
    const name = document.getElementById('candidateName').value;
    const party = document.getElementById('candidateParty').value;
    const description = document.getElementById('candidateDescription').value;
    
    try {
        const result = await apiRequest('/api/register-candidate', 'POST', {
            candidate_id: candidateId,
            name: name,
            party: party,
            description: description
        });
        
        if (result.success) {
            showNotification(result.message, 'success');
            clearForm('registerCandidateForm');
            // Don't reload - candidate is registered
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        showNotification('Failed to register candidate', 'error');
    }
});

// Start Election
document.getElementById('startElectionBtn')?.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to start the election?')) return;
    
    try {
        const result = await apiRequest('/api/start-election', 'POST');
        
        if (result.success) {
            showNotification(result.message, 'success');
            // Don't reload - election started
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        showNotification('Failed to start election', 'error');
    }
});

// End Election
document.getElementById('endElectionBtn')?.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to end the election? This action cannot be undone.')) return;
    
    try {
        const result = await apiRequest('/api/end-election', 'POST');
        
        if (result.success) {
            showNotification(result.message, 'success');
            // Don't reload - election ended
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        showNotification('Failed to end election', 'error');
    }
});

// Mine Votes
document.getElementById('mineVotesBtn')?.addEventListener('click', async () => {
    const btn = document.getElementById('mineVotesBtn');
    btn.disabled = true;
    btn.textContent = 'Mining...';
    
    try {
        const result = await apiRequest('/api/mine-votes', 'POST');
        
        if (result.success) {
            // Show modal with block hash information
            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.85);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                padding: 2rem;
            `;
            
            const content = document.createElement('div');
            content.style.cssText = `
                background: white;
                padding: 2.5rem;
                border-radius: 1rem;
                max-width: 650px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            `;
            
            content.innerHTML = `
                <div style="text-align: center; margin-bottom: 1.5rem;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">⛏️</div>
                    <h2 style="color: var(--success); margin-bottom: 0.5rem;">Block Mined Successfully!</h2>
                    <p style="color: var(--text-muted); font-size: 0.95rem;">${result.message}</p>
                </div>
                
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; color: white;">
                    <div style="margin-bottom: 1rem;">
                        <div style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 0.5rem;">Block Hash:</div>
                        <code style="
                            display: block;
                            background: rgba(0,0,0,0.2);
                            padding: 0.75rem;
                            border-radius: 6px;
                            font-size: 0.8rem;
                            word-break: break-all;
                            font-family: monospace;
                            font-weight: 600;
                            cursor: pointer;
                        " onclick="copyToClipboard('${result.block_hash}')" title="Click to copy">${result.block_hash}</code>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; font-size: 0.9rem;">
                        <div>
                            <div style="opacity: 0.8; font-size: 0.85rem;">Block Index:</div>
                            <div style="font-weight: 600; font-size: 1.2rem;">#${result.block_index}</div>
                        </div>
                        <div>
                            <div style="opacity: 0.8; font-size: 0.85rem;">Nonce:</div>
                            <div style="font-weight: 600; font-size: 1.2rem;">${result.block_nonce}</div>
                        </div>
                        <div>
                            <div style="opacity: 0.8; font-size: 0.85rem;">Votes:</div>
                            <div style="font-weight: 600; font-size: 1.2rem;">${result.transaction_count}</div>
                        </div>
                    </div>
                </div>
                
                <div style="background: #d1fae5; border-left: 4px solid #10b981; padding: 1rem; border-radius: 4px; margin-bottom: 1.5rem; font-size: 0.9rem; color: #065f46;">
                    <strong>✓ Success:</strong> The votes have been permanently added to the blockchain and cannot be altered.
                </div>
                
                <div style="display: flex; gap: 1rem;">
                    <button onclick="copyToClipboard('${result.block_hash}')" class="btn btn-secondary" style="flex: 1;">
                        📋 Copy Hash
                    </button>
                    <button onclick="this.parentElement.parentElement.parentElement.remove(); loadLatestBlockHash();" class="btn btn-primary" style="flex: 1;">
                        ✓ Close
                    </button>
                </div>
            `;
            
            modal.appendChild(content);
            document.body.appendChild(modal);
            
            showNotification(result.message, 'success');
            btn.disabled = false;
            btn.textContent = '⛏️ Mine Pending Votes';
        } else {
            showNotification(result.message, 'error');
            btn.disabled = false;
            btn.textContent = '⛏️ Mine Pending Votes';
        }
    } catch (error) {
        showNotification('Failed to mine votes', 'error');
        btn.disabled = false;
        btn.textContent = '⛏️ Mine Pending Votes';
    }
});

// Verify Blockchain
document.getElementById('verifyBlockchainBtn')?.addEventListener('click', async () => {
    const btn = document.getElementById('verifyBlockchainBtn');
    btn.disabled = true;
    btn.textContent = 'Verifying...';
    
    try {
        const result = await apiRequest('/api/verify-blockchain', 'GET');
        
        if (result.success) {
            if (result.is_valid) {
                showNotification(result.message, 'success');
            } else {
                showNotification(result.message, 'error');
            }
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        showNotification('Failed to verify blockchain', 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = '✓ Verify Blockchain';
    }
});

// Create or Replace Sample Data - Common function
async function createSampleDataAction(btnId, isReplace = false) {
    const confirmMsg = isReplace 
        ? 'This will REPLACE the current election with sample data. All current data will be lost. Continue?' 
        : 'This will create a sample election with 5 candidates and 20 voters. Continue?';
    
    if (!confirm(confirmMsg)) return;
    
    const btn = document.getElementById(btnId);
    btn.disabled = true;
    btn.textContent = 'Creating Sample Data...';
    
    try {
        const result = await apiRequest('/api/create-sample-data', 'POST');
        
        if (result.success) {
            showNotification(result.message, 'success');
            
            // Display voter credentials
            if (result.voter_credentials && result.voter_credentials.length > 0) {
                // Create a modal/popup with credentials
                const modal = document.createElement('div');
                modal.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0,0,0,0.8);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10000;
                    padding: 2rem;
                `;
                
                const content = document.createElement('div');
                content.style.cssText = `
                    background: white;
                    padding: 2rem;
                    border-radius: 1rem;
                    max-width: 800px;
                    max-height: 80vh;
                    overflow-y: auto;
                `;
                
                let html = `
                    <h2 style="color: var(--primary); margin-bottom: 1rem;">
                        🎉 Sample Data Created Successfully!
                    </h2>
                    <div class="alert alert-warning">
                        <strong>⚠️ Save These Voter Credentials!</strong><br>
                        You'll need these to test voting. Copy them now.
                    </div>
                    <div style="max-height: 400px; overflow-y: auto; margin: 1rem 0;">
                        <table style="width: 100%; border-collapse: collapse;">
                            <thead>
                                <tr style="background: var(--primary); color: white;">
                                    <th style="padding: 0.75rem; text-align: left;">Voter ID</th>
                                    <th style="padding: 0.75rem; text-align: left;">Name</th>
                                    <th style="padding: 0.75rem; text-align: left;">Private Key</th>
                                </tr>
                            </thead>
                            <tbody>
                `;
                
                result.voter_credentials.forEach((cred, index) => {
                    html += `
                        <tr style="border-bottom: 1px solid var(--border); ${index % 2 === 0 ? 'background: var(--light);' : ''}">
                            <td style="padding: 0.75rem; font-weight: 600;">${cred.voter_id}</td>
                            <td style="padding: 0.75rem;">${cred.name}</td>
                            <td style="padding: 0.75rem;">
                                <code style="font-size: 0.75rem; word-break: break-all; cursor: pointer;" 
                                      onclick="copyToClipboard('${cred.private_key}')" 
                                      title="Click to copy">
                                    ${cred.private_key}
                                </code>
                            </td>
                        </tr>
                    `;
                });
                
                html += `
                            </tbody>
                        </table>
                    </div>
                    <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 1rem;">
                        <button onclick="downloadCredentials()" class="btn btn-secondary">
                            📥 Download as Text File
                        </button>
                        <button onclick="this.parentElement.parentElement.parentElement.remove(); loadElections();" 
                                class="btn btn-primary">
                            ✓ Close and Continue
                        </button>
                    </div>
                `;
                
                content.innerHTML = html;
                modal.appendChild(content);
                document.body.appendChild(modal);
                
                // Store credentials for download
                window.sampleCredentials = result.voter_credentials;
            } else {
                loadElections();
            }
        } else {
            showNotification(result.message, 'error');
            btn.disabled = false;
            btn.textContent = isReplace ? '🔄 Replace with Sample Election Data' : '🎲 Create Sample Election Data';
        }
    } catch (error) {
        showNotification('Failed to create sample data', 'error');
        btn.disabled = false;
        btn.textContent = isReplace ? '🔄 Replace with Sample Election Data' : '🎲 Create Sample Election Data';
    }
}

// Attach event listeners for both buttons
document.getElementById('createSampleDataBtn')?.addEventListener('click', () => {
    createSampleDataAction('createSampleDataBtn', false);
});

document.getElementById('replaceSampleDataBtn')?.addEventListener('click', () => {
    createSampleDataAction('replaceSampleDataBtn', true);
});

// Download credentials function
window.downloadCredentials = function() {
    if (!window.sampleCredentials) return;
    
    let text = "="*70 + "\n";
    text += "  VOTER CREDENTIALS - KEEP THIS SECURE!\n";
    text += "="*70 + "\n\n";
    text += "Election: University Student Council Election 2025\n\n";
    text += "Use these credentials to test voting:\n\n";
    
    window.sampleCredentials.forEach(cred => {
        text += `Voter ID: ${cred.voter_id}\n`;
        text += `Name: ${cred.name}\n`;
        text += `Private Key: ${cred.private_key}\n`;
        text += "-".repeat(70) + "\n\n";
    });
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'voter_credentials.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    showNotification('Credentials downloaded!', 'success');
};

// Auto-refresh stats every 30 seconds
if (window.location.pathname === '/admin') {
    setInterval(async () => {
        try {
            const result = await apiRequest('/api/stats', 'GET');
            if (result.success) {
                // Update stats without full page reload
                updateStatsDisplay(result.stats);
            }
        } catch (error) {
            console.error('Failed to fetch stats:', error);
        }
    }, 30000);
}

function updateStatsDisplay(stats) {
    // Update stat cards if they exist
    const statCards = document.querySelectorAll('.stat-card');
    if (statCards.length >= 6) {
        statCards[0].querySelector('.stat-value').textContent = stats.voter_count;
        statCards[1].querySelector('.stat-value').textContent = stats.candidate_count;
        statCards[2].querySelector('.stat-value').textContent = stats.votes_cast;
        statCards[3].querySelector('.stat-value').textContent = stats.pending_votes;
        statCards[4].querySelector('.stat-value').textContent = stats.blockchain_blocks;
        statCards[5].querySelector('.stat-value').textContent = stats.blockchain_valid ? '✓' : '✗';
    }
}

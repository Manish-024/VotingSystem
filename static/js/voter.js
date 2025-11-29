// Voter Portal JavaScript

// Load elections on page load
async function loadElections() {
    try {
        const result = await apiRequest('/api/list-elections', 'GET');
        if (result.success) {
            const select = document.getElementById('electionSelect');
            select.innerHTML = '';
            
            if (result.elections.length === 0) {
                select.innerHTML = '<option value="">No elections available</option>';
            } else {
                result.elections.forEach(election => {
                    const option = document.createElement('option');
                    option.value = election.id;
                    const status = election.is_active ? '🟢 Active' : '🔴 Closed';
                    option.textContent = `${election.name} - ${status}`;
                    if (election.id === result.current_election_id) {
                        option.selected = true;
                    }
                    select.appendChild(option);
                });
            }
        }
    } catch (error) {
        console.error('Failed to load elections:', error);
    }
}

// Switch election
document.getElementById('electionSelect')?.addEventListener('change', async (e) => {
    const electionId = e.target.value;
    if (!electionId) return;
    
    try {
        const result = await apiRequest('/api/switch-election', 'POST', {
            election_id: electionId
        });
        
        if (result.success) {
            showNotification(result.message, 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        showNotification('Failed to switch election', 'error');
    }
});

// Load elections when page loads
document.addEventListener('DOMContentLoaded', loadElections);

// Cast Vote
document.getElementById('castVoteForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const voterId = document.getElementById('voteVoterId').value;
    const privateKey = document.getElementById('votePrivateKey').value;
    const candidateId = document.getElementById('voteCandidateId').value;
    
    if (!candidateId) {
        showNotification('Please select a candidate', 'error');
        return;
    }
    
    // Confirm vote
    const candidateSelect = document.getElementById('voteCandidateId');
    const selectedOption = candidateSelect.options[candidateSelect.selectedIndex];
    const candidateName = selectedOption.text;
    
    if (!confirm(`Are you sure you want to vote for ${candidateName}?\n\nThis action cannot be undone.`)) {
        return;
    }
    
    const btn = e.target.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.textContent = 'Submitting Vote...';
    
    try {
        const result = await apiRequest('/api/cast-vote', 'POST', {
            voter_id: voterId,
            candidate_id: candidateId,
            private_key: privateKey
        });
        
        if (result.success) {
            showNotification(result.message, 'success');
            clearForm('castVoteForm');
            
            // Show success message with transaction hash
            if (result.transaction_hash) {
                // Create modal to display transaction details
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
                    max-width: 600px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                `;
                
                content.innerHTML = `
                    <div style="text-align: center; margin-bottom: 1.5rem;">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">✅</div>
                        <h2 style="color: var(--success); margin-bottom: 0.5rem;">Vote Successfully Cast!</h2>
                        <p style="color: var(--text-muted); font-size: 0.95rem;">Your vote has been recorded in the blockchain</p>
                    </div>
                    
                    <div style="background: var(--light); padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;">
                        <div style="margin-bottom: 1rem;">
                            <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.25rem;">Transaction Hash:</div>
                            <code style="
                                display: block;
                                background: white;
                                padding: 0.75rem;
                                border-radius: 6px;
                                font-size: 0.8rem;
                                word-break: break-all;
                                border: 2px solid var(--border-color);
                                font-family: monospace;
                                color: var(--primary);
                                font-weight: 600;
                            ">${result.transaction_hash}</code>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.9rem;">
                            <div>
                                <div style="color: var(--text-muted); font-size: 0.85rem;">Transaction ID:</div>
                                <div style="font-weight: 600; color: var(--primary);">${result.transaction_id || 'N/A'}</div>
                            </div>
                            <div>
                                <div style="color: var(--text-muted); font-size: 0.85rem;">Pending Votes:</div>
                                <div style="font-weight: 600; color: var(--accent);">${result.pending_count || 0}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 1rem; border-radius: 4px; margin-bottom: 1.5rem; font-size: 0.9rem;">
                        <strong>⚠️ Important:</strong> Your vote is currently in the pending pool. It will be permanently recorded on the blockchain when the administrator mines the next block.
                    </div>
                    
                    <div style="display: flex; gap: 1rem;">
                        <button onclick="copyToClipboard('${result.transaction_hash}')" class="btn btn-secondary" style="flex: 1;">
                            📋 Copy Hash
                        </button>
                        <button onclick="this.parentElement.parentElement.parentElement.remove();" class="btn btn-primary" style="flex: 1;">
                            ✓ Close
                        </button>
                    </div>
                `;
                
                modal.appendChild(content);
                document.body.appendChild(modal);
            } else {
                setTimeout(() => {
                    alert('✓ Your vote has been successfully recorded!\n\nYour vote will be mined into the blockchain by the administrator.\n\nThank you for participating in this election.');
                    location.reload();
                }, 1000);
            }
        } else {
            showNotification(result.message, 'error');
            btn.disabled = false;
            btn.textContent = 'Submit Vote';
        }
    } catch (error) {
        showNotification('Failed to cast vote. Please try again.', 'error');
        btn.disabled = false;
        btn.textContent = 'Submit Vote';
    }
});

// Check Status
document.getElementById('checkStatusForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const voterId = document.getElementById('statusVoterId').value;
    
    try {
        const result = await apiRequest('/api/check-status', 'POST', {
            voter_id: voterId
        });
        
        const statusDisplay = document.getElementById('statusDisplay');
        
        if (result.success) {
            const voter = result.voter;
            statusDisplay.innerHTML = `
                <div class="alert alert-info">
                    <strong>Voter Information</strong><br>
                    <strong>Name:</strong> ${voter.name}<br>
                    <strong>Email:</strong> ${voter.email}<br>
                    <strong>Status:</strong> ${voter.has_voted ? 
                        '<span style="color: var(--success)">✓ Vote Recorded</span>' : 
                        '<span style="color: var(--warning)">✗ Not Yet Voted</span>'}
                </div>
            `;
            statusDisplay.style.display = 'block';
        } else {
            statusDisplay.innerHTML = `
                <div class="alert alert-error">
                    <strong>Error</strong><br>${result.message}
                </div>
            `;
            statusDisplay.style.display = 'block';
        }
    } catch (error) {
        showNotification('Failed to check status', 'error');
    }
});

// Toggle password visibility
const privateKeyInput = document.getElementById('votePrivateKey');
if (privateKeyInput) {
    const toggleBtn = document.createElement('button');
    toggleBtn.type = 'button';
    toggleBtn.textContent = '👁️';
    toggleBtn.style.cssText = 'position: absolute; right: 10px; top: 50%; transform: translateY(-50%); border: none; background: none; cursor: pointer; font-size: 1.2rem;';
    
    const formGroup = privateKeyInput.parentElement;
    formGroup.style.position = 'relative';
    formGroup.appendChild(toggleBtn);
    
    toggleBtn.addEventListener('click', () => {
        if (privateKeyInput.type === 'password') {
            privateKeyInput.type = 'text';
            toggleBtn.textContent = '🙈';
        } else {
            privateKeyInput.type = 'password';
            toggleBtn.textContent = '👁️';
        }
    });
}

// Highlight selected candidate
const candidateSelect = document.getElementById('voteCandidateId');
if (candidateSelect) {
    candidateSelect.addEventListener('change', (e) => {
        // Remove highlight from all candidates
        document.querySelectorAll('.candidate-item').forEach(item => {
            item.style.borderColor = 'var(--border)';
            item.style.background = 'white';
        });
        
        // Highlight selected candidate
        const selectedId = e.target.value;
        if (selectedId) {
            const candidateItems = document.querySelectorAll('.candidate-item');
            candidateItems.forEach(item => {
                const idElement = item.querySelector('.candidate-id');
                if (idElement && idElement.textContent.includes(selectedId)) {
                    item.style.borderColor = 'var(--primary)';
                    item.style.background = 'rgba(99, 102, 241, 0.05)';
                }
            });
        }
    });
}

// Make candidate cards clickable
document.querySelectorAll('.candidate-item').forEach(item => {
    item.style.cursor = 'pointer';
    item.addEventListener('click', () => {
        const idText = item.querySelector('.candidate-id').textContent;
        const candidateId = idText.replace('ID: ', '').trim();
        
        const select = document.getElementById('voteCandidateId');
        if (select) {
            select.value = candidateId;
            select.dispatchEvent(new Event('change'));
            
            // Scroll to voting form
            const votingForm = document.getElementById('castVoteForm');
            if (votingForm) {
                votingForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });
});

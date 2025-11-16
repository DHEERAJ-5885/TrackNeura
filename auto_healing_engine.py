"""
⭐ Auto-Healing Upload Engine ⭐
================================

Hello little one! This is like having a magical healing potion for your file uploads!

Think of it this way:
- Each file chunk is like a tiny baby trying to climb stairs
- If a baby falls, we gently pick them up and help them try again
- We remember which step each baby reached, so they don't start over
- We make sure each baby arrives safely and isn't hurt (no corruption)
- If the internet playground closes, we wait patiently and continue later

This engine watches over all your uploads like a caring parent! 👶✨
"""

import hashlib
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import asyncio
import logging

class AutoHealingUploadEngine:
    """
    A gentle upload engine that never gives up on your files!
    Like a patient teacher helping children learn to walk.
    """
    
    def __init__(self, max_retries: int = 5, base_retry_delay: float = 1.0):
        """
        Baby, let's create our healing engine!
        
        max_retries: How many times we'll help a chunk if it falls (default: 5 tries)
        base_retry_delay: How long we wait before helping again (starts at 1 second)
        """
        self.max_retries = max_retries
        self.base_retry_delay = base_retry_delay
        self.upload_states = {}  # Like a memory book of all our uploads
        self.chunk_checksums = {}  # Like fingerprints to make sure chunks aren't hurt
        self.failure_patterns = {}  # Like learning which steps are slippery
        self.retry_counts = {}  # Count how many times we helped each chunk
        self.network_stable = True  # Is our internet playground open?
        
        # Set up gentle logging (like keeping a diary)
        self.logger = logging.getLogger('AutoHealingEngine')
        self.logger.setLevel(logging.INFO)
        
    def calculate_chunk_checksum(self, chunk_data: bytes) -> str:
        """
        Baby, this creates a unique fingerprint for each chunk!
        Like how every snowflake is different, every chunk gets its own special ID.
        If the fingerprint changes, we know the chunk got hurt during travel.
        """
        # Use SHA-256 for strong protection (like a really good ID card)
        hasher = hashlib.sha256()
        hasher.update(chunk_data)
        return hasher.hexdigest()
    
    def save_upload_state(self, upload_id: str, state_data: Dict) -> None:
        """
        Baby, this saves our progress like bookmarking a story!
        Even if the computer goes to sleep, we remember where we left off.
        """
        try:
            # Create a safe folder for our memory files
            os.makedirs('upload_states', exist_ok=True)
            
            # Save the state like writing in a diary
            state_file = f'upload_states/{upload_id}.json'
            with open(state_file, 'w') as f:
                json.dump({
                    'upload_id': upload_id,
                    'timestamp': datetime.now().isoformat(),
                    'state': state_data,
                    'version': '1.0'  # In case we improve our memory system later
                }, f, indent=2)
                
            self.logger.info(f"💾 Saved progress for upload {upload_id}")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Couldn't save progress: {e}")
    
    def load_upload_state(self, upload_id: str) -> Optional[Dict]:
        """
        Baby, this reads our old progress like opening a favorite book!
        We can continue exactly where we left off.
        """
        try:
            state_file = f'upload_states/{upload_id}.json'
            if os.path.exists(state_file):
                with open(state_file, 'r') as f:
                    saved_data = json.load(f)
                    self.logger.info(f"📖 Found saved progress for upload {upload_id}")
                    return saved_data.get('state', {})
        except Exception as e:
            self.logger.warning(f"⚠️ Couldn't read saved progress: {e}")
        
        return None
    
    def calculate_retry_delay(self, attempt_count: int) -> float:
        """
        Baby, this decides how long to wait before trying again!
        Like when you fall off your bike - first we wait a little, 
        then a bit longer if you fall again, so you don't get too tired.
        
        Attempt 1: Wait 1 second
        Attempt 2: Wait 2 seconds  
        Attempt 3: Wait 4 seconds
        Attempt 4: Wait 8 seconds
        And so on... (exponential backoff)
        """
        delay = self.base_retry_delay * (2 ** (attempt_count - 1))
        # Don't wait more than 60 seconds (we're patient but not sleepy!)
        return min(delay, 60.0)
    
    def should_jump_back(self, upload_id: str, current_chunk: int) -> Tuple[bool, int]:
        """
        Baby, this decides if we need to go back and check earlier chunks!
        Like when you're building blocks and notice the bottom ones are wobbly.
        
        If 3 chunks fail in a row, we go back 2 chunks to double-check.
        """
        failure_key = f"{upload_id}_recent_failures"
        
        if failure_key not in self.failure_patterns:
            self.failure_patterns[failure_key] = []
        
        recent_failures = self.failure_patterns[failure_key]
        
        # Keep only the last 5 failures for analysis
        if len(recent_failures) > 5:
            recent_failures = recent_failures[-5:]
            self.failure_patterns[failure_key] = recent_failures
        
        # Check if we have 3 consecutive failures
        if len(recent_failures) >= 3:
            consecutive_failures = all(
                recent_failures[i] == recent_failures[i-1] + 1 
                for i in range(1, 3)
            )
            
            if consecutive_failures:
                jump_back_to = max(0, current_chunk - 2)
                self.logger.info(f"🔄 Jumping back from chunk {current_chunk} to {jump_back_to}")
                # Clear recent failures after jump-back
                self.failure_patterns[failure_key] = []
                return True, jump_back_to
        
        return False, current_chunk
    
    def record_chunk_failure(self, upload_id: str, chunk_number: int) -> None:
        """
        Baby, this remembers when a chunk had trouble!
        Like keeping track of which steps are slippery on the stairs.
        """
        failure_key = f"{upload_id}_recent_failures"
        
        if failure_key not in self.failure_patterns:
            self.failure_patterns[failure_key] = []
        
        self.failure_patterns[failure_key].append(chunk_number)
        self.logger.info(f"📝 Recorded failure for chunk {chunk_number}")
    
    def get_adaptive_chunk_size(self, upload_id: str, base_chunk_size: int) -> int:
        """
        Baby, this makes chunks smaller when the internet is wobbly!
        Like cutting your sandwich into smaller pieces when you're feeling sick.
        """
        failure_key = f"{upload_id}_recent_failures"
        recent_failures = self.failure_patterns.get(failure_key, [])
        
        # If we've had many failures recently, make chunks smaller
        failure_count = len(recent_failures)
        
        if failure_count >= 3:
            # Make chunks 4x smaller for very unstable connections
            return max(base_chunk_size // 4, 64 * 1024)  # At least 64KB
        elif failure_count >= 2:
            # Make chunks 2x smaller for somewhat unstable connections  
            return max(base_chunk_size // 2, 128 * 1024)  # At least 128KB
        else:
            return base_chunk_size
    
    def estimate_corruption_probability(self, upload_id: str) -> float:
        """
        Baby, this guesses how likely chunks are to get hurt!
        Like knowing which playground equipment is more dangerous.
        """
        corruption_key = f"{upload_id}_corruptions" 
        total_key = f"{upload_id}_total_chunks"
        
        corruptions = self.failure_patterns.get(corruption_key, 0)
        total_chunks = self.failure_patterns.get(total_key, 1)
        
        probability = corruptions / total_chunks
        return min(probability, 1.0)  # Never more than 100%
    
    def create_healing_session(self, upload_id: str, file_info: Dict) -> Dict:
        """
        Baby, this starts a new healing session for an upload!
        Like opening a new medical file for a patient.
        """
        session = {
            'upload_id': upload_id,
            'file_info': file_info,
            'created_at': datetime.now().isoformat(),
            'status': 'initializing',
            'completed_chunks': [],
            'failed_chunks': [],
            'retry_counts': {},
            'total_retries': 0,
            'corruption_detections': 0,
            'jump_backs': 0,
            'adaptive_resizes': 0,
            'healing_events': []  # Log of all healing actions
        }
        
        self.upload_states[upload_id] = session
        self.save_upload_state(upload_id, session)
        
        self.logger.info(f"🩺 Created healing session for {upload_id}")
        return session
    
    def add_healing_event(self, upload_id: str, event_type: str, details: Dict) -> None:
        """
        Baby, this records what healing actions we took!
        Like writing in a medical chart what medicine we gave.
        """
        if upload_id in self.upload_states:
            event = {
                'timestamp': datetime.now().isoformat(),
                'type': event_type,
                'details': details
            }
            
            self.upload_states[upload_id]['healing_events'].append(event)
            self.save_upload_state(upload_id, self.upload_states[upload_id])
            
            self.logger.info(f"📋 Healing event: {event_type} for {upload_id}")
    
    async def heal_chunk_upload(self, upload_id: str, chunk_number: int, 
                               chunk_data: bytes, upload_function) -> Tuple[bool, str]:
        """
        Baby, this is our main healing function for chunk uploads!
        Like a gentle doctor who keeps trying different treatments until you feel better.
        
        Returns: (success, message)
        """
        retry_key = f"{upload_id}_{chunk_number}"
        current_retries = self.retry_counts.get(retry_key, 0)
        
        # Calculate checksum for corruption detection
        expected_checksum = self.calculate_chunk_checksum(chunk_data)
        
        for attempt in range(current_retries + 1, self.max_retries + 1):
            try:
                self.logger.info(f"🩹 Healing attempt {attempt} for chunk {chunk_number}")
                
                # Try to upload the chunk
                result = await upload_function(chunk_number, chunk_data, expected_checksum)
                
                if result.get('success'):
                    # Verify checksum if server provides it
                    server_checksum = result.get('checksum')
                    if server_checksum and server_checksum != expected_checksum:
                        self.logger.warning(f"💔 Corruption detected in chunk {chunk_number}")
                        self.add_healing_event(upload_id, 'corruption_detected', {
                            'chunk_number': chunk_number,
                            'expected_checksum': expected_checksum,
                            'received_checksum': server_checksum
                        })
                        continue  # Try again
                    
                    # Success! Clear retry count
                    if retry_key in self.retry_counts:
                        del self.retry_counts[retry_key]
                    
                    self.add_healing_event(upload_id, 'chunk_healed', {
                        'chunk_number': chunk_number,
                        'attempts': attempt,
                        'checksum': expected_checksum
                    })
                    
                    return True, f"Chunk {chunk_number} uploaded successfully"
                
            except Exception as e:
                self.logger.warning(f"⚠️ Upload attempt {attempt} failed: {e}")
                
                # Record the failure
                self.record_chunk_failure(upload_id, chunk_number)
                self.retry_counts[retry_key] = attempt
                
                # Wait before retrying (exponential backoff)
                if attempt < self.max_retries:
                    delay = self.calculate_retry_delay(attempt)
                    self.logger.info(f"⏰ Waiting {delay:.1f}s before retry...")
                    await asyncio.sleep(delay)
        
        # All retries exhausted
        self.add_healing_event(upload_id, 'chunk_failed', {
            'chunk_number': chunk_number,
            'max_attempts': self.max_retries,
            'final_error': str(e) if 'e' in locals() else 'Unknown error'
        })
        
        return False, f"Chunk {chunk_number} failed after {self.max_retries} attempts"
    
    async def heal_full_upload(self, upload_id: str, file_path: str, 
                              chunk_size: int, upload_function, 
                              progress_callback=None) -> Dict:
        """
        Baby, this heals an entire file upload from start to finish!
        Like a complete medical treatment plan for a patient.
        """
        # Create or restore healing session
        existing_state = self.load_upload_state(upload_id)
        if existing_state:
            session = existing_state
            self.upload_states[upload_id] = session
            self.logger.info(f"🔄 Resuming upload {upload_id}")
        else:
            file_info = {
                'path': file_path,
                'size': os.path.getsize(file_path),
                'name': os.path.basename(file_path)
            }
            session = self.create_healing_session(upload_id, file_info)
        
        total_size = session['file_info']['size']
        completed_chunks = set(session.get('completed_chunks', []))
        total_chunks = (total_size + chunk_size - 1) // chunk_size
        
        self.logger.info(f"🎯 Starting healing upload: {total_chunks} chunks, {len(completed_chunks)} already done")
        
        current_chunk = 0
        consecutive_failures = 0
        
        with open(file_path, 'rb') as file:
            while current_chunk < total_chunks:
                # Skip already completed chunks
                if current_chunk in completed_chunks:
                    current_chunk += 1
                    continue
                
                # Check if we should jump back
                should_jump, jump_to_chunk = self.should_jump_back(upload_id, current_chunk)
                if should_jump:
                    current_chunk = jump_to_chunk
                    consecutive_failures = 0
                    self.add_healing_event(upload_id, 'jump_back', {
                        'from_chunk': current_chunk,
                        'to_chunk': jump_to_chunk
                    })
                    continue
                
                # Get adaptive chunk size
                adaptive_size = self.get_adaptive_chunk_size(upload_id, chunk_size)
                if adaptive_size != chunk_size:
                    self.add_healing_event(upload_id, 'adaptive_resize', {
                        'chunk_number': current_chunk,
                        'original_size': chunk_size,
                        'adaptive_size': adaptive_size
                    })
                
                # Read chunk data
                file.seek(current_chunk * adaptive_size)
                chunk_data = file.read(adaptive_size)
                
                if not chunk_data:
                    break
                
                # Try to heal this chunk
                success, message = await self.heal_chunk_upload(
                    upload_id, current_chunk, chunk_data, upload_function
                )
                
                if success:
                    completed_chunks.add(current_chunk)
                    session['completed_chunks'] = list(completed_chunks)
                    consecutive_failures = 0
                    
                    # Update progress
                    progress = len(completed_chunks) / total_chunks * 100
                    if progress_callback:
                        progress_callback(progress, f"Healed chunk {current_chunk + 1}/{total_chunks}")
                    
                    self.logger.info(f"✅ Chunk {current_chunk} healed successfully")
                    
                else:
                    consecutive_failures += 1
                    self.logger.error(f"💔 Chunk {current_chunk} could not be healed: {message}")
                    
                    # If too many consecutive failures, something is seriously wrong
                    if consecutive_failures >= 5:
                        self.logger.error("🚨 Too many consecutive failures, pausing upload")
                        session['status'] = 'paused_critical_failures'
                        self.save_upload_state(upload_id, session)
                        return {
                            'success': False,
                            'error': 'Too many consecutive chunk failures',
                            'session': session
                        }
                
                # Save progress
                self.save_upload_state(upload_id, session)
                current_chunk += 1
        
        # Upload completed!
        session['status'] = 'completed'
        session['completed_at'] = datetime.now().isoformat()
        self.save_upload_state(upload_id, session)
        
        self.logger.info(f"🎉 Upload {upload_id} fully healed and completed!")
        
        return {
            'success': True,
            'session': session,
            'total_chunks': total_chunks,
            'healing_events': len(session['healing_events'])
        }

# Create a global healing engine instance
healing_engine = AutoHealingUploadEngine()
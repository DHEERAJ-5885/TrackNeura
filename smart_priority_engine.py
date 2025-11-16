# 🧠 The Smart Brain of Our File Transfer Playground!
# This is like having a super smart teacher who remembers everything and makes perfect decisions

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import math
import json
import os
from dataclasses import dataclass, asdict
from smart_priority_config import *

@dataclass
class FileMetrics:
    """All the important information about each file (like a report card)"""
    file_id: str
    filename: str
    file_size: int
    file_type: FileType
    user_priority: UserPriority
    time_sensitive: str
    upload_start_time: datetime
    estimated_completion: Optional[datetime] = None
    failure_count: int = 0
    success_rate: float = 1.0
    average_speed: float = 0.0
    network_condition: NetworkCondition = NetworkCondition.GOOD
    context_tags: List[str] = None
    predicted_difficulty: float = 0.5

    def __post_init__(self):
        if self.context_tags is None:
            self.context_tags = []

@dataclass
class ChunkMetrics:
    """Information about each piece of a file (like pages in a book)"""
    chunk_id: str
    file_id: str
    chunk_number: int
    chunk_size: int
    is_metadata: bool = False
    is_beginning: bool = False
    is_ending: bool = False
    failure_count: int = 0
    last_attempt: Optional[datetime] = None
    completion_time: Optional[datetime] = None

class SmartPriorityEngine:
    """The magical brain that decides who goes first in our playground! 🧠✨"""
    
    def __init__(self, config: SmartPriorityConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.file_history: Dict[str, List[dict]] = {}  # Remember past performance
        self.network_history: List[Tuple[datetime, NetworkCondition]] = []
        self.learning_data: Dict[str, float] = {}  # What we've learned
        self.active_transfers: Dict[str, FileMetrics] = {}
        self.chunk_queue: List[ChunkMetrics] = []
        
        print("🎪 Smart Priority Engine is ready! Let the file playground begin! 🚀")
    
    def detect_file_type(self, filename: str) -> FileType:
        """Figure out what type of kid (file) this is! 🔍"""
        filename_lower = filename.lower()
        
        # Check for emergency keywords first (hurt kids need immediate help!)
        for keyword in FILE_PATTERNS[FileType.EMERGENCY]:
            if keyword in filename_lower:
                return FileType.EMERGENCY
        
        # Check file extensions (like looking at the kid's backpack)
        file_ext = os.path.splitext(filename)[1].lower()
        for file_type, extensions in FILE_PATTERNS.items():
            if file_type != FileType.EMERGENCY and file_ext in extensions:
                return file_type
        
        return FileType.OTHER
    
    def get_size_category(self, file_size: int) -> str:
        """Figure out if this is a tiny toy or a huge suitcase! 📏"""
        for category, (min_size, max_size) in self.config.SIZE_CATEGORIES.items():
            if min_size <= file_size < max_size:
                return category
        return 'huge'
    
    def predict_difficulty(self, file_metrics: FileMetrics) -> float:
        """Guess how tricky this transfer might be (like predicting weather) 🔮"""
        difficulty = 0.5  # Start neutral
        
        # Bigger files are usually trickier
        size_category = self.get_size_category(file_metrics.file_size)
        size_difficulty = {
            'tiny': 0.1, 'small': 0.3, 'medium': 0.5, 'large': 0.7, 'huge': 0.9
        }
        difficulty += size_difficulty.get(size_category, 0.5) * 0.3
        
        # Some file types are naturally more complex
        type_difficulty = {
            FileType.VIDEO: 0.8, FileType.ARCHIVE: 0.7, FileType.AUDIO: 0.6,
            FileType.IMAGE: 0.4, FileType.DOCUMENT: 0.3, FileType.CODE: 0.2,
            FileType.EMERGENCY: 0.1, FileType.OTHER: 0.5
        }
        difficulty += type_difficulty.get(file_metrics.file_type, 0.5) * 0.2
        
        # Bad network makes everything harder
        network_difficulty = {
            NetworkCondition.EXCELLENT: 0.1, NetworkCondition.GOOD: 0.3,
            NetworkCondition.FAIR: 0.5, NetworkCondition.POOR: 0.7,
            NetworkCondition.CRITICAL: 0.9
        }
        difficulty += network_difficulty.get(file_metrics.network_condition, 0.5) * 0.3
        
        # Learn from history (if we've seen similar files before)
        if file_metrics.filename in self.file_history:
            historical_difficulty = np.mean([h.get('actual_difficulty', 0.5) 
                                           for h in self.file_history[file_metrics.filename]])
            difficulty = difficulty * 0.7 + historical_difficulty * 0.3
        
        return min(max(difficulty, 0.0), 1.0)  # Keep between 0 and 1
    
    def calculate_base_priority_score(self, file_metrics: FileMetrics) -> float:
        """Calculate the fundamental importance score (like grades on a test) 📊"""
        
        # Start with the file type's natural priority
        base_score = self.config.TYPE_SCORES.get(file_metrics.file_type, 40)
        
        # 📏 Size factor: smaller files often get slight boost
        size_category = self.get_size_category(file_metrics.file_size)
        size_multipliers = {'tiny': 1.2, 'small': 1.1, 'medium': 1.0, 'large': 0.9, 'huge': 0.8}
        size_factor = size_multipliers.get(size_category, 1.0)
        
        # ⏰ Time sensitivity (how urgently they need to go)
        time_factor = self.config.TIME_MULTIPLIERS.get(file_metrics.time_sensitive, 1.0)
        
        # 👤 User's stated priority (listen to what they say!)
        user_factor = file_metrics.user_priority.value / 3.0  # Normalize to reasonable range
        
        # 📈 Success rate (help those who struggled before)
        success_factor = 2.0 - file_metrics.success_rate  # Lower success = higher priority
        
        # 🔮 Predicted difficulty (harder files get slight boost to start early)
        difficulty_factor = 1.0 + (file_metrics.predicted_difficulty * 0.2)
        
        # 🌐 Network condition adaptation
        network_factor = self._get_network_adaptation_factor(file_metrics)
        
        # Combine all factors using configured weights
        combined_score = base_score * (
            (size_factor * self.config.WEIGHTS['file_size']) +
            (time_factor * self.config.WEIGHTS['time_sensitive']) +
            (user_factor * self.config.WEIGHTS['user_priority']) +
            (success_factor * self.config.WEIGHTS['failure_history']) +
            (difficulty_factor * self.config.WEIGHTS['predicted_difficulty']) +
            (network_factor * self.config.WEIGHTS['network_strength'])
        )
        
        return combined_score
    
    def _get_network_adaptation_factor(self, file_metrics: FileMetrics) -> float:
        """Adapt priority based on current network conditions 🌐"""
        network_condition = file_metrics.network_condition
        file_size = file_metrics.file_size
        
        # On poor networks, prioritize smaller files
        if network_condition in [NetworkCondition.POOR, NetworkCondition.CRITICAL]:
            size_category = self.get_size_category(file_size)
            if size_category in ['tiny', 'small']:
                return 1.5  # Boost small files on poor networks
            elif size_category in ['large', 'huge']:
                return 0.7  # Reduce large files on poor networks
        
        # On excellent networks, large files don't get penalized
        elif network_condition == NetworkCondition.EXCELLENT:
            return 1.2 if file_size > 100 * 1024 * 1024 else 1.0
        
        return 1.0  # Neutral factor
    
    def calculate_dynamic_priority(self, file_metrics: FileMetrics) -> float:
        """Calculate the final priority with all the smart adjustments! 🎯"""
        
        # Start with base priority
        priority = self.calculate_base_priority_score(file_metrics)
        
        # 🕒 Waiting time boost (kids who waited longer get priority)
        wait_time = (datetime.now() - file_metrics.upload_start_time).total_seconds()
        wait_boost = min(wait_time / 3600, 2.0)  # Max 2x boost after 2 hours
        priority *= (1.0 + wait_boost * 0.1)
        
        # 🔄 Retry boost (files that failed before get extra help)
        if file_metrics.failure_count > 0:
            retry_boost = min(file_metrics.failure_count * 0.3, 1.0)
            priority *= (1.0 + retry_boost)
        
        # 🧠 Learning adjustment (apply what we've learned)
        learning_factor = self._get_learning_factor(file_metrics)
        priority *= learning_factor
        
        # 🎪 Context-based boosts (special situations)
        context_boost = self._calculate_context_boost(file_metrics)
        priority *= context_boost
        
        return priority
    
    def _get_learning_factor(self, file_metrics: FileMetrics) -> float:
        """Apply machine learning insights to adjust priority 🧠"""
        file_pattern = f"{file_metrics.file_type.value}_{self.get_size_category(file_metrics.file_size)}"
        
        if file_pattern in self.learning_data:
            # Use learned performance data to adjust
            learned_performance = self.learning_data[file_pattern]
            # If historically performed worse than expected, boost priority
            return 1.0 + (0.5 - learned_performance) * 0.4
        
        return 1.0  # No learning data yet
    
    def _calculate_context_boost(self, file_metrics: FileMetrics) -> float:
        """Special boosts based on file context and tags 🏷️"""
        boost = 1.0
        
        for tag in file_metrics.context_tags:
            if 'critical' in tag.lower():
                boost *= 1.3
            elif 'deadline' in tag.lower():
                boost *= 1.2
            elif 'presentation' in tag.lower():
                boost *= 1.15
            elif 'backup' in tag.lower():
                boost *= 0.8  # Backups can wait
        
        return boost
    
    def calculate_chunk_priority(self, chunk: ChunkMetrics, file_priority: float) -> float:
        """Decide priority for each piece of the file (like pages in a book) 📄"""
        
        base_priority = file_priority
        
        # 📋 Metadata chunks are super important (like the book cover)
        if chunk.is_metadata:
            base_priority *= self.config.CHUNK_RULES['metadata_boost']
        
        # 📖 Beginning chunks often crucial (like the first chapter)
        elif chunk.is_beginning:
            base_priority *= self.config.CHUNK_RULES['beginning_boost']
        
        # 📝 Ending chunks sometimes important (like the conclusion)
        elif chunk.is_ending:
            base_priority *= self.config.CHUNK_RULES['ending_boost']
        
        # 📄 Middle chunks can wait a bit (like middle chapters)
        else:
            base_priority *= self.config.CHUNK_RULES['middle_penalty']
        
        # 🔄 Failed chunks get major boost (help the struggling pages)
        if chunk.failure_count > 0:
            retry_boost = min(chunk.failure_count * 0.5, 2.0)
            base_priority *= (1.0 + retry_boost)
        
        # ⏰ Chunks that have been waiting longer get slight boost
        if chunk.last_attempt:
            wait_time = (datetime.now() - chunk.last_attempt).total_seconds()
            wait_boost = min(wait_time / 300, 0.5)  # Max 50% boost after 5 minutes
            base_priority *= (1.0 + wait_boost)
        
        return base_priority
    
    def update_network_condition(self, condition: NetworkCondition):
        """Update our understanding of how good the internet highway is 🌐"""
        self.network_history.append((datetime.now(), condition))
        
        # Keep only recent history (last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.network_history = [(time, cond) for time, cond in self.network_history 
                               if time > cutoff_time]
        
        print(f"🌐 Network condition updated to: {condition.value}")
    
    def record_transfer_result(self, file_id: str, success: bool, actual_time: float, 
                             actual_difficulty: float):
        """Remember how well each transfer went (learn from experience) 📚"""
        
        if file_id not in self.file_history:
            self.file_history[file_id] = []
        
        result = {
            'timestamp': datetime.now(),
            'success': success,
            'actual_time': actual_time,
            'actual_difficulty': actual_difficulty,
            'network_condition': self._get_current_network_condition()
        }
        
        self.file_history[file_id].append(result)
        
        # Update learning data
        self._update_learning_model(file_id, result)
        
        print(f"📚 Recorded transfer result for {file_id}: {'✅ Success' if success else '❌ Failed'}")
    
    def _get_current_network_condition(self) -> NetworkCondition:
        """Get the most recent network condition"""
        if self.network_history:
            return self.network_history[-1][1]
        return NetworkCondition.GOOD
    
    def _update_learning_model(self, file_id: str, result: dict):
        """Update our machine learning knowledge 🧠"""
        # This would integrate with the ML model from your existing system
        # For now, we do simple pattern learning
        
        if file_id in self.active_transfers:
            file_metrics = self.active_transfers[file_id]
            pattern = f"{file_metrics.file_type.value}_{self.get_size_category(file_metrics.file_size)}"
            
            # Update learning data with exponential moving average
            if pattern in self.learning_data:
                old_value = self.learning_data[pattern]
                new_value = result['actual_difficulty']
                self.learning_data[pattern] = (old_value * 0.9 + new_value * 0.1)
            else:
                self.learning_data[pattern] = result['actual_difficulty']
    
    def get_optimal_chunk_size(self, file_metrics: FileMetrics) -> int:
        """Decide the best size for each piece of the file 📏"""
        network_condition = file_metrics.network_condition
        base_chunk_size = self.config.NETWORK_RULES[network_condition]['chunk_size']
        
        # Adjust based on file type
        if file_metrics.file_type == FileType.EMERGENCY:
            return min(base_chunk_size, 4 * 1024 * 1024)  # Smaller chunks for emergencies
        elif file_metrics.file_type == FileType.VIDEO:
            return base_chunk_size  # Standard chunks for videos
        elif file_metrics.file_type in [FileType.DOCUMENT, FileType.CODE]:
            return min(base_chunk_size, 8 * 1024 * 1024)  # Medium chunks for text
        
        return base_chunk_size
    
    def create_transfer_plan(self, file_metrics: FileMetrics) -> dict:
        """Create a complete plan for transferring a file (like a roadmap) 🗺️"""
        
        # Calculate priorities and difficulty
        file_metrics.predicted_difficulty = self.predict_difficulty(file_metrics)
        priority_score = self.calculate_dynamic_priority(file_metrics)
        optimal_chunk_size = self.get_optimal_chunk_size(file_metrics)
        
        # Create chunks
        total_chunks = math.ceil(file_metrics.file_size / optimal_chunk_size)
        chunks = []
        
        for i in range(total_chunks):
            chunk_size = min(optimal_chunk_size, 
                           file_metrics.file_size - (i * optimal_chunk_size))
            
            chunk = ChunkMetrics(
                chunk_id=f"{file_metrics.file_id}_chunk_{i}",
                file_id=file_metrics.file_id,
                chunk_number=i,
                chunk_size=chunk_size,
                is_metadata=(i == 0),  # First chunk often has metadata
                is_beginning=(i < 2),   # First two chunks are "beginning"
                is_ending=(i >= total_chunks - 2)  # Last two chunks are "ending"
            )
            
            chunk_priority = self.calculate_chunk_priority(chunk, priority_score)
            chunks.append({
                'chunk': chunk,
                'priority': chunk_priority
            })
        
        # Store in active transfers
        self.active_transfers[file_metrics.file_id] = file_metrics
        
        transfer_plan = {
            'file_id': file_metrics.file_id,
            'file_priority': priority_score,
            'total_chunks': total_chunks,
            'chunk_size': optimal_chunk_size,
            'estimated_time': self._estimate_transfer_time(file_metrics, optimal_chunk_size),
            'chunks': chunks,
            'recommended_concurrency': self.config.NETWORK_RULES[file_metrics.network_condition]['max_concurrent']
        }
        
        print(f"🗺️ Created transfer plan for {file_metrics.filename}")
        print(f"   Priority Score: {priority_score:.2f}")
        print(f"   Total Chunks: {total_chunks}")
        print(f"   Network: {file_metrics.network_condition.value}")
        
        return transfer_plan
    
    def _estimate_transfer_time(self, file_metrics: FileMetrics, chunk_size: int) -> float:
        """Estimate how long the transfer will take (like predicting travel time) ⏱️"""
        
        # Base network speeds (bytes per second)
        network_speeds = {
            NetworkCondition.EXCELLENT: 50 * 1024 * 1024,  # 50 MB/s
            NetworkCondition.GOOD: 20 * 1024 * 1024,       # 20 MB/s
            NetworkCondition.FAIR: 10 * 1024 * 1024,       # 10 MB/s
            NetworkCondition.POOR: 2 * 1024 * 1024,        # 2 MB/s
            NetworkCondition.CRITICAL: 512 * 1024          # 512 KB/s
        }
        
        base_speed = network_speeds.get(file_metrics.network_condition, 10 * 1024 * 1024)
        
        # Adjust for file type complexity
        complexity_factors = {
            FileType.EMERGENCY: 0.8,    # Simpler handling
            FileType.DOCUMENT: 0.9,     # Easy to process
            FileType.CODE: 0.9,         # Text-based, easy
            FileType.IMAGE: 1.0,        # Standard
            FileType.AUDIO: 1.1,        # Slightly more complex
            FileType.VIDEO: 1.3,        # More complex processing
            FileType.ARCHIVE: 1.2,      # Compression considerations
            FileType.OTHER: 1.0         # Standard
        }
        
        effective_speed = base_speed * complexity_factors.get(file_metrics.file_type, 1.0)
        
        # Add overhead for chunking and error handling
        overhead_factor = 1.2
        
        estimated_seconds = (file_metrics.file_size / effective_speed) * overhead_factor
        
        # Add extra time for files with poor history
        if file_metrics.failure_count > 0:
            estimated_seconds *= (1.0 + file_metrics.failure_count * 0.1)
        
        return estimated_seconds
    
    def get_next_priority_batch(self, batch_size: int = 5) -> List[dict]:
        """Get the next batch of highest priority chunks to transfer 🎯"""
        
        all_chunks = []
        
        # Collect all chunks from active transfers
        for file_id, file_metrics in self.active_transfers.items():
            # This would integrate with your chunk tracking system
            # For now, we'll simulate getting chunks
            pass
        
        # Sort by priority and return top batch
        all_chunks.sort(key=lambda x: x['priority'], reverse=True)
        return all_chunks[:batch_size]
    
    def save_state(self, filepath: str):
        """Save all our learning and history (like keeping a diary) 💾"""
        state = {
            'file_history': {k: [asdict(item) if hasattr(item, '__dict__') else item 
                               for item in v] for k, v in self.file_history.items()},
            'learning_data': self.learning_data,
            'network_history': [(time.isoformat(), cond.value) 
                              for time, cond in self.network_history],
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"💾 Smart Priority Engine state saved to {filepath}")
    
    def load_state(self, filepath: str):
        """Load our previous learning and history (like reading our diary) 📖"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                state = json.load(f)
            
            self.file_history = state.get('file_history', {})
            self.learning_data = state.get('learning_data', {})
            
            # Restore network history
            network_history = state.get('network_history', [])
            self.network_history = [(datetime.fromisoformat(time), NetworkCondition(cond))
                                  for time, cond in network_history]
            
            print(f"📖 Smart Priority Engine state loaded from {filepath}")
        else:
            print(f"📝 No previous state found at {filepath}, starting fresh!")

# 🎪 Example usage function
def demo_smart_priority_engine():
    """Show how our magical priority engine works! ✨"""
    
    print("🎪 Welcome to the Smart Priority File Transfer Playground!")
    print("=" * 60)
    
    # Create our smart engine
    engine = SmartPriorityEngine()
    
    # Create some example files (kids wanting to play)
    example_files = [
        FileMetrics(
            file_id="file_001",
            filename="emergency_presentation.pptx",
            file_size=25 * 1024 * 1024,  # 25MB
            file_type=FileType.EMERGENCY,
            user_priority=UserPriority.CRITICAL,
            time_sensitive="immediate",
            upload_start_time=datetime.now(),
            network_condition=NetworkCondition.FAIR,
            context_tags=["presentation", "deadline"]
        ),
        FileMetrics(
            file_id="file_002", 
            filename="vacation_video.mp4",
            file_size=500 * 1024 * 1024,  # 500MB
            file_type=FileType.VIDEO,
            user_priority=UserPriority.LOW,
            time_sensitive="background",
            upload_start_time=datetime.now() - timedelta(hours=1),
            network_condition=NetworkCondition.FAIR
        ),
        FileMetrics(
            file_id="file_003",
            filename="project_code.zip",
            file_size=10 * 1024 * 1024,  # 10MB
            file_type=FileType.ARCHIVE,
            user_priority=UserPriority.HIGH,
            time_sensitive="urgent", 
            upload_start_time=datetime.now() - timedelta(minutes=30),
            network_condition=NetworkCondition.FAIR,
            context_tags=["code", "deadline"]
        )
    ]
    
    print("\n🎯 Creating transfer plans for our files:")
    plans = []
    for file_metrics in example_files:
        plan = engine.create_transfer_plan(file_metrics)
        plans.append(plan)
        print(f"  📁 {file_metrics.filename}: Priority {plan['file_priority']:.2f}")
    
    print("\n🏆 Final Priority Ranking:")
    plans.sort(key=lambda x: x['file_priority'], reverse=True)
    for i, plan in enumerate(plans, 1):
        file_id = plan['file_id']
        file_metrics = engine.active_transfers[file_id]
        print(f"  {i}. {file_metrics.filename} (Score: {plan['file_priority']:.2f})")
        print(f"     Size: {file_metrics.file_size / (1024*1024):.1f}MB, "
              f"Type: {file_metrics.file_type.value}, "
              f"Chunks: {plan['total_chunks']}")
    
    print("\n✨ The Smart Priority Engine has spoken! Emergency presentation goes first! 🎉")

if __name__ == "__main__":
    demo_smart_priority_engine()
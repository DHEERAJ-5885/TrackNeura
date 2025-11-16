# 🎯 Dynamic Queue Scheduler - The Master Playground Organizer!
# This is like having the world's smartest line manager who can rearrange kids perfectly!

import heapq
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from concurrent.futures import ThreadPoolExecutor

from smart_priority_config import *
from smart_priority_engine import SmartPriorityEngine, FileMetrics, ChunkMetrics

class TransferState(Enum):
    """Different states our files can be in (like positions in line)"""
    WAITING = "waiting"          # Standing in line patiently
    ACTIVE = "active"            # Currently going down the slide!
    PAUSED = "paused"           # Taking a break (maybe network is slow)
    COMPLETED = "completed"      # All done! Success! 🎉
    FAILED = "failed"           # Didn't work out, need to try again
    CANCELLED = "cancelled"      # Decided not to go after all

@dataclass
class TransferTask:
    """A complete task for transferring a file chunk (like a ticket to play)"""
    task_id: str
    file_id: str
    chunk: ChunkMetrics
    priority: float
    state: TransferState = TransferState.WAITING
    assigned_worker: Optional[str] = None
    start_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    retry_count: int = 0
    last_error: Optional[str] = None
    progress: float = 0.0  # 0.0 to 1.0
    
    # Make this work with heapq (priority queue)
    def __lt__(self, other):
        return self.priority > other.priority  # Higher priority = lower value for heapq

class NetworkAdapter:
    """Smart network condition monitor (like a weather station for internet) 🌐"""
    
    def __init__(self):
        self.current_condition = NetworkCondition.GOOD
        self.speed_history: List[Tuple[datetime, float]] = []
        self.error_rate_history: List[Tuple[datetime, float]] = []
        self.monitoring = False
        
    def start_monitoring(self):
        """Start watching the network like a weather reporter 📡"""
        self.monitoring = True
        # In a real implementation, this would start actual network monitoring
        print("📡 Network monitoring started!")
    
    def stop_monitoring(self):
        """Stop watching the network"""
        self.monitoring = False
        print("📡 Network monitoring stopped!")
    
    def record_transfer_speed(self, speed_bps: float):
        """Record how fast a transfer went"""
        self.speed_history.append((datetime.now(), speed_bps))
        
        # Keep only recent history (last hour)
        cutoff = datetime.now() - timedelta(hours=1)
        self.speed_history = [(time, speed) for time, speed in self.speed_history if time > cutoff]
        
        # Update network condition based on recent speeds
        self._update_network_condition()
    
    def record_error_rate(self, error_rate: float):
        """Record how many errors we're seeing"""
        self.error_rate_history.append((datetime.now(), error_rate))
        
        # Keep only recent history
        cutoff = datetime.now() - timedelta(minutes=30)
        self.error_rate_history = [(time, rate) for time, rate in self.error_rate_history if time > cutoff]
        
        self._update_network_condition()
    
    def _update_network_condition(self):
        """Analyze recent data and update network condition"""
        if not self.speed_history:
            return
        
        # Calculate average speed from recent transfers
        recent_speeds = [speed for _, speed in self.speed_history[-10:]]  # Last 10 transfers
        avg_speed = sum(recent_speeds) / len(recent_speeds)
        
        # Calculate error rate
        error_rate = 0.0
        if self.error_rate_history:
            recent_errors = [rate for _, rate in self.error_rate_history[-5:]]
            error_rate = sum(recent_errors) / len(recent_errors)
        
        # Determine network condition
        old_condition = self.current_condition
        
        if avg_speed > 40 * 1024 * 1024 and error_rate < 0.01:  # 40MB/s, <1% errors
            self.current_condition = NetworkCondition.EXCELLENT
        elif avg_speed > 15 * 1024 * 1024 and error_rate < 0.05:  # 15MB/s, <5% errors
            self.current_condition = NetworkCondition.GOOD
        elif avg_speed > 5 * 1024 * 1024 and error_rate < 0.10:   # 5MB/s, <10% errors
            self.current_condition = NetworkCondition.FAIR
        elif avg_speed > 1 * 1024 * 1024 and error_rate < 0.20:   # 1MB/s, <20% errors
            self.current_condition = NetworkCondition.POOR
        else:
            self.current_condition = NetworkCondition.CRITICAL
        
        if old_condition != self.current_condition:
            print(f"🌐 Network condition changed: {old_condition.value} → {self.current_condition.value}")

class DynamicQueueScheduler:
    """The ultimate smart queue manager for our file playground! 🎪👑"""
    
    def __init__(self, priority_engine: SmartPriorityEngine, max_workers: int = 4):
        self.priority_engine = priority_engine
        self.max_workers = max_workers
        self.network_adapter = NetworkAdapter()
        
        # Our different queues (like different lines for different activities)
        self.high_priority_queue = []      # Emergency line - always goes first!
        self.normal_priority_queue = []    # Regular line - most files go here
        self.background_queue = []         # Patient line - can wait longer
        
        # Active management
        self.active_tasks: Dict[str, TransferTask] = {}
        self.completed_tasks: List[TransferTask] = []
        self.failed_tasks: List[TransferTask] = []
        
        # Worker management
        self.workers: Dict[str, dict] = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
        # Scheduling control
        self.running = False
        self.scheduler_thread = None
        self.rebalance_interval = 30  # Recheck priorities every 30 seconds
        
        # Statistics
        self.stats = {
            'total_processed': 0,
            'total_successful': 0,
            'total_failed': 0,
            'average_wait_time': 0.0,
            'average_transfer_time': 0.0
        }
        
        print("🎪 Dynamic Queue Scheduler is ready to manage the playground! 👑")
    
    def add_transfer_task(self, file_metrics: FileMetrics, chunk: ChunkMetrics) -> str:
        """Add a new file chunk to our smart queue system 📥"""
        
        # Calculate current priority
        priority = self.priority_engine.calculate_chunk_priority(chunk, 
                   self.priority_engine.calculate_dynamic_priority(file_metrics))
        
        # Create transfer task
        task = TransferTask(
            task_id=f"task_{chunk.chunk_id}_{int(time.time())}",
            file_id=file_metrics.file_id,
            chunk=chunk,
            priority=priority
        )
        
        # Route to appropriate queue based on priority
        self._route_to_queue(task)
        
        print(f"📥 Added task {task.task_id} with priority {priority:.2f}")
        return task.task_id
    
    def _route_to_queue(self, task: TransferTask):
        """Decide which line (queue) this task should join 🚦"""
        
        if task.priority > 80:  # High priority threshold
            heapq.heappush(self.high_priority_queue, task)
            print(f"🚨 Task routed to HIGH priority queue (priority: {task.priority:.2f})")
        
        elif task.priority > 30:  # Normal priority threshold
            heapq.heappush(self.normal_priority_queue, task)
            print(f"📋 Task routed to NORMAL priority queue (priority: {task.priority:.2f})")
        
        else:  # Background priority
            heapq.heappush(self.background_queue, task)
            print(f"⏳ Task routed to BACKGROUND priority queue (priority: {task.priority:.2f})")
    
    def start_scheduler(self):
        """Start the magical queue management system! ✨"""
        if self.running:
            print("⚠️ Scheduler is already running!")
            return
        
        self.running = True
        self.network_adapter.start_monitoring()
        
        # Start the main scheduler loop
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        
        print("✨ Dynamic Queue Scheduler has started! The magic begins! 🎪")
    
    def stop_scheduler(self):
        """Stop the queue management system"""
        print("🛑 Stopping Dynamic Queue Scheduler...")
        self.running = False
        self.network_adapter.stop_monitoring()
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        self.executor.shutdown(wait=True)
        print("🛑 Dynamic Queue Scheduler stopped!")
    
    def _scheduler_loop(self):
        """The main brain loop that keeps everything organized! 🧠⚡"""
        
        last_rebalance = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                # 🔄 Rebalance queues periodically (rearrange the lines)
                if current_time - last_rebalance > self.rebalance_interval:
                    self._rebalance_queues()
                    last_rebalance = current_time
                
                # 🎯 Assign work to available workers
                self._assign_work_to_workers()
                
                # 🧹 Clean up completed and failed tasks
                self._cleanup_completed_tasks()
                
                # 📊 Update statistics
                self._update_statistics()
                
                # 💤 Brief rest before next cycle
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error in scheduler loop: {e}")
                time.sleep(5)  # Wait longer if there's an error
    
    def _rebalance_queues(self):
        """Rearrange all the lines based on new conditions! 🔄"""
        print("🔄 Rebalancing queues based on current conditions...")
        
        # Collect all waiting tasks from all queues
        all_tasks = []
        
        # Empty all queues and collect tasks
        while self.high_priority_queue:
            task = heapq.heappop(self.high_priority_queue)
            if task.state == TransferState.WAITING:
                all_tasks.append(task)
        
        while self.normal_priority_queue:
            task = heapq.heappop(self.normal_priority_queue)
            if task.state == TransferState.WAITING:
                all_tasks.append(task)
        
        while self.background_queue:
            task = heapq.heappop(self.background_queue)
            if task.state == TransferState.WAITING:
                all_tasks.append(task)
        
        # Recalculate priorities for all tasks
        for task in all_tasks:
            if task.file_id in self.priority_engine.active_transfers:
                file_metrics = self.priority_engine.active_transfers[task.file_id]
                # Update network condition
                file_metrics.network_condition = self.network_adapter.current_condition
                # Recalculate priority
                new_priority = self.priority_engine.calculate_chunk_priority(
                    task.chunk, 
                    self.priority_engine.calculate_dynamic_priority(file_metrics)
                )
                task.priority = new_priority
        
        # Re-route all tasks to appropriate queues
        for task in all_tasks:
            self._route_to_queue(task)
        
        print(f"🔄 Rebalanced {len(all_tasks)} tasks across queues")
    
    def _assign_work_to_workers(self):
        """Give tasks to available workers (like assigning kids to playground equipment) 👷"""
        
        # Count available workers
        available_workers = self.max_workers - len(self.active_tasks)
        
        if available_workers <= 0:
            return  # All workers are busy
        
        # Get next tasks to process (priority order)
        tasks_to_assign = []
        
        # 1. First, check high priority queue
        while self.high_priority_queue and len(tasks_to_assign) < available_workers:
            task = heapq.heappop(self.high_priority_queue)
            if task.state == TransferState.WAITING:
                tasks_to_assign.append(task)
        
        # 2. Then, check normal priority queue  
        while self.normal_priority_queue and len(tasks_to_assign) < available_workers:
            task = heapq.heappop(self.normal_priority_queue)
            if task.state == TransferState.WAITING:
                tasks_to_assign.append(task)
        
        # 3. Finally, check background queue
        while self.background_queue and len(tasks_to_assign) < available_workers:
            task = heapq.heappop(self.background_queue)
            if task.state == TransferState.WAITING:
                tasks_to_assign.append(task)
        
        # Assign tasks to workers
        for task in tasks_to_assign:
            self._assign_task_to_worker(task)
    
    def _assign_task_to_worker(self, task: TransferTask):
        """Give a specific task to a worker 👷‍♀️"""
        
        worker_id = f"worker_{len(self.active_tasks) + 1}"
        task.state = TransferState.ACTIVE
        task.assigned_worker = worker_id
        task.start_time = datetime.now()
        
        self.active_tasks[task.task_id] = task
        
        # Submit to thread pool for actual processing
        future = self.executor.submit(self._process_transfer_task, task)
        
        print(f"👷 Assigned task {task.task_id} to {worker_id}")
    
    def _process_transfer_task(self, task: TransferTask) -> bool:
        """Actually process a transfer task (the real work!) ⚡"""
        
        try:
            print(f"⚡ Processing {task.task_id} (chunk {task.chunk.chunk_number})")
            
            # Simulate transfer work (in real implementation, this would do actual transfer)
            file_metrics = self.priority_engine.active_transfers.get(task.file_id)
            if not file_metrics:
                raise Exception("File metrics not found")
            
            # Simulate transfer time based on chunk size and network conditions
            chunk_size = task.chunk.chunk_size
            network_condition = self.network_adapter.current_condition
            
            # Calculate transfer time
            base_speeds = {
                NetworkCondition.EXCELLENT: 50 * 1024 * 1024,
                NetworkCondition.GOOD: 20 * 1024 * 1024,
                NetworkCondition.FAIR: 10 * 1024 * 1024,
                NetworkCondition.POOR: 2 * 1024 * 1024,
                NetworkCondition.CRITICAL: 512 * 1024
            }
            
            speed = base_speeds.get(network_condition, 10 * 1024 * 1024)
            transfer_time = chunk_size / speed
            
            # Simulate the transfer (with progress updates)
            steps = 10
            for i in range(steps):
                if not self.running:  # Check if we should stop
                    break
                
                time.sleep(transfer_time / steps)
                task.progress = (i + 1) / steps
                
                # Simulate occasional failures for demonstration
                if task.chunk.failure_count > 0 and i == 5:  # Fail halfway through retry
                    if task.retry_count < 2:  # Allow some retries
                        raise Exception("Simulated network hiccup")
            
            # Success!
            task.state = TransferState.COMPLETED
            task.completion_time = datetime.now()
            task.progress = 1.0
            
            # Record success in network adapter
            actual_speed = chunk_size / transfer_time
            self.network_adapter.record_transfer_speed(actual_speed)
            self.network_adapter.record_error_rate(0.0)  # No errors
            
            # Update priority engine
            actual_time = (task.completion_time - task.start_time).total_seconds()
            self.priority_engine.record_transfer_result(
                task.file_id, True, actual_time, task.priority / 100.0
            )
            
            print(f"✅ Successfully completed {task.task_id}")
            return True
            
        except Exception as e:
            # Handle failure
            task.state = TransferState.FAILED
            task.last_error = str(e)
            task.retry_count += 1
            
            # Record failure in network adapter
            self.network_adapter.record_error_rate(1.0)  # 100% error for this transfer
            
            print(f"❌ Task {task.task_id} failed: {e}")
            
            # Decide whether to retry
            if task.retry_count < 3:  # Max 3 retries
                print(f"🔄 Will retry {task.task_id} (attempt {task.retry_count + 1})")
                task.state = TransferState.WAITING
                task.priority *= 1.2  # Boost priority for retry
                self._route_to_queue(task)  # Re-queue with higher priority
            else:
                print(f"💔 Task {task.task_id} failed permanently after {task.retry_count} retries")
            
            return False
        
        finally:
            # Clean up worker assignment
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]
    
    def _cleanup_completed_tasks(self):
        """Clean up old completed and failed tasks 🧹"""
        
        # Move completed tasks to history (keep last 100)
        completed_today = [task for task in self.completed_tasks 
                          if task.completion_time and 
                          task.completion_time > datetime.now() - timedelta(hours=24)]
        
        self.completed_tasks = completed_today[-100:]  # Keep last 100
        
        # Same for failed tasks
        failed_today = [task for task in self.failed_tasks
                       if task.start_time and
                       task.start_time > datetime.now() - timedelta(hours=24)]
        
        self.failed_tasks = failed_today[-100:]  # Keep last 100
    
    def _update_statistics(self):
        """Update our performance statistics 📊"""
        
        total_completed = len(self.completed_tasks)
        total_failed = len(self.failed_tasks)
        
        self.stats['total_processed'] = total_completed + total_failed
        self.stats['total_successful'] = total_completed
        self.stats['total_failed'] = total_failed
        
        # Calculate average wait time
        if self.completed_tasks:
            wait_times = []
            for task in self.completed_tasks[-50:]:  # Last 50 tasks
                if task.start_time and hasattr(task, 'created_time'):
                    wait_time = (task.start_time - task.created_time).total_seconds()
                    wait_times.append(wait_time)
            
            if wait_times:
                self.stats['average_wait_time'] = sum(wait_times) / len(wait_times)
        
        # Calculate average transfer time
        if self.completed_tasks:
            transfer_times = []
            for task in self.completed_tasks[-50:]:  # Last 50 tasks
                if task.start_time and task.completion_time:
                    transfer_time = (task.completion_time - task.start_time).total_seconds()
                    transfer_times.append(transfer_time)
            
            if transfer_times:
                self.stats['average_transfer_time'] = sum(transfer_times) / len(transfer_times)
    
    def get_queue_status(self) -> dict:
        """Get current status of all our queues 📊"""
        return {
            'high_priority_queue': len(self.high_priority_queue),
            'normal_priority_queue': len(self.normal_priority_queue), 
            'background_queue': len(self.background_queue),
            'active_tasks': len(self.active_tasks),
            'network_condition': self.network_adapter.current_condition.value,
            'statistics': self.stats.copy()
        }
    
    def pause_transfers(self):
        """Pause all transfers (like calling a timeout in the playground) ⏸️"""
        for task in self.active_tasks.values():
            if task.state == TransferState.ACTIVE:
                task.state = TransferState.PAUSED
        print("⏸️ All transfers paused")
    
    def resume_transfers(self):
        """Resume all transfers (like saying 'play time continues!') ▶️"""
        for task in self.active_tasks.values():
            if task.state == TransferState.PAUSED:
                task.state = TransferState.ACTIVE
        print("▶️ All transfers resumed")
    
    def force_rebalance(self):
        """Force an immediate rebalancing of all queues 🔄"""
        print("🔄 Forcing immediate queue rebalance...")
        self._rebalance_queues()

# 🎪 Demo function to show how our scheduler works
def demo_dynamic_scheduler():
    """Show off our amazing dynamic queue scheduler! ✨"""
    
    print("🎪 Welcome to the Dynamic Queue Scheduler Demo!")
    print("=" * 60)
    
    # Create our systems
    priority_engine = SmartPriorityEngine()
    scheduler = DynamicQueueScheduler(priority_engine, max_workers=3)
    
    # Start the scheduler
    scheduler.start_scheduler()
    
    try:
        # Create some example files and chunks
        example_files = [
            FileMetrics(
                file_id="urgent_file",
                filename="emergency_report.pdf", 
                file_size=10 * 1024 * 1024,
                file_type=FileType.EMERGENCY,
                user_priority=UserPriority.CRITICAL,
                time_sensitive="immediate",
                upload_start_time=datetime.now(),
                network_condition=NetworkCondition.FAIR
            ),
            FileMetrics(
                file_id="video_file",
                filename="presentation.mp4",
                file_size=200 * 1024 * 1024,
                file_type=FileType.VIDEO,
                user_priority=UserPriority.NORMAL,
                time_sensitive="normal",
                upload_start_time=datetime.now(),
                network_condition=NetworkCondition.FAIR
            ),
            FileMetrics(
                file_id="backup_file",
                filename="backup.zip",
                file_size=50 * 1024 * 1024,
                file_type=FileType.ARCHIVE,
                user_priority=UserPriority.LOW,
                time_sensitive="background",
                upload_start_time=datetime.now(),
                network_condition=NetworkCondition.FAIR
            )
        ]
        
        # Add files to priority engine
        for file_metrics in example_files:
            priority_engine.active_transfers[file_metrics.file_id] = file_metrics
        
        # Create and add chunks to scheduler
        print("\n📥 Adding chunks to scheduler...")
        for file_metrics in example_files:
            # Create a few chunks for each file
            chunk_size = 5 * 1024 * 1024  # 5MB chunks
            num_chunks = min(3, (file_metrics.file_size + chunk_size - 1) // chunk_size)
            
            for i in range(num_chunks):
                chunk = ChunkMetrics(
                    chunk_id=f"{file_metrics.file_id}_chunk_{i}",
                    file_id=file_metrics.file_id,
                    chunk_number=i,
                    chunk_size=min(chunk_size, file_metrics.file_size - i * chunk_size),
                    is_metadata=(i == 0),
                    is_beginning=(i == 0),
                    is_ending=(i == num_chunks - 1)
                )
                
                task_id = scheduler.add_transfer_task(file_metrics, chunk)
                print(f"   Added {task_id}")
        
        # Let it run for a while
        print("\n⚡ Scheduler is running... Watch the magic happen!")
        
        for i in range(15):  # Run for 15 seconds
            time.sleep(1)
            
            if i % 5 == 0:  # Every 5 seconds, show status
                status = scheduler.get_queue_status()
                print(f"\n📊 Queue Status (t={i}s):")
                print(f"   High Priority: {status['high_priority_queue']} tasks")
                print(f"   Normal Priority: {status['normal_priority_queue']} tasks")
                print(f"   Background: {status['background_queue']} tasks")
                print(f"   Active: {status['active_tasks']} tasks")
                print(f"   Network: {status['network_condition']}")
                print(f"   Success Rate: {status['statistics']['total_successful']}/{status['statistics']['total_processed']}")
        
        print("\n✨ Demo completed! The Dynamic Queue Scheduler works like magic! 🎉")
        
    finally:
        # Clean shutdown
        scheduler.stop_scheduler()

if __name__ == "__main__":
    demo_dynamic_scheduler()
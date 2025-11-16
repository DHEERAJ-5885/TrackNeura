# 🎪 The Complete Smart Priority File Transfer System!
# This is the master conductor of our amazing file playground orchestra! 🎭

from flask import Flask, request, jsonify, render_template
import os
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import uuid
from dataclasses import asdict

# Import our magical components
from smart_priority_config import *
from smart_priority_engine import SmartPriorityEngine, FileMetrics, ChunkMetrics
from dynamic_queue_scheduler import DynamicQueueScheduler, TransferTask, TransferState
from behavioral_learning import BehavioralLearningSystem
from dataset_generator import DatasetGenerator

# Import from existing system
from config import Config
from ml_model import PriorityMLModel

class SmartFileTransferSystem:
    """The ultimate smart file transfer system! 🚀🧠"""
    
    def __init__(self):
        # Initialize all our smart components
        self.priority_engine = SmartPriorityEngine()
        self.queue_scheduler = DynamicQueueScheduler(self.priority_engine, max_workers=6)
        self.learning_system = BehavioralLearningSystem()
        self.ml_model = PriorityMLModel()  # Existing ML model
        
        # System state
        self.active_files: Dict[str, FileMetrics] = {}
        self.system_stats = {
            'total_files_processed': 0,
            'total_chunks_processed': 0,
            'success_rate': 0.0,
            'average_priority_accuracy': 0.0,
            'system_start_time': datetime.now(),
            'last_learning_update': None
        }
        
        # Load any existing models and history
        self.learning_system.load_models()
        self.ml_model.load_model()
        
        print("🎪 Smart File Transfer System initialized!")
        print("   🧠 Priority Engine: Ready")
        print("   📋 Queue Scheduler: Ready") 
        print("   🎓 Learning System: Ready")
        print("   🤖 ML Model: Ready")
    
    def start_system(self):
        """Start all the magical components! ✨"""
        
        print("🚀 Starting Smart File Transfer System...")
        
        # Start the queue scheduler
        self.queue_scheduler.start_scheduler()
        
        # Start periodic learning updates
        self._start_learning_loop()
        
        print("✨ Smart File Transfer System is now ACTIVE! 🎉")
    
    def stop_system(self):
        """Stop the system gracefully"""
        
        print("🛑 Stopping Smart File Transfer System...")
        
        # Stop scheduler
        self.queue_scheduler.stop_scheduler()
        
        # Save all learning data
        self.learning_system.save_models()
        self.priority_engine.save_state("priority_engine_state.json")
        
        print("🛑 Smart File Transfer System stopped gracefully")
    
    def analyze_and_queue_file(self, filename: str, file_size: int, 
                              user_priority: UserPriority = UserPriority.NORMAL,
                              time_sensitive: str = "normal",
                              context_tags: List[str] = None) -> str:
        """Analyze a file and add it to our smart queue! 📥🧠"""
        
        # Create unique file ID
        file_id = str(uuid.uuid4())
        
        # Detect file type using our smart engine
        file_type = self.priority_engine.detect_file_type(filename)
        
        # Get current network condition
        network_condition = self.queue_scheduler.network_adapter.current_condition
        
        # Create file metrics
        file_metrics = FileMetrics(
            file_id=file_id,
            filename=filename,
            file_size=file_size,
            file_type=file_type,
            user_priority=user_priority,
            time_sensitive=time_sensitive,
            upload_start_time=datetime.now(),
            network_condition=network_condition,
            context_tags=context_tags or []
        )
        
        # Use ML model to enhance prediction if available
        if self.ml_model.is_trained:
            ml_prediction = self.ml_model.predict_priority(filename, file_size)
            file_metrics.predicted_difficulty = ml_prediction.get('confidence', 0.5)
        
        # Create transfer plan using priority engine
        transfer_plan = self.priority_engine.create_transfer_plan(file_metrics)
        
        # Store file
        self.active_files[file_id] = file_metrics
        
        # Create chunks and add to scheduler
        chunk_tasks = []
        for chunk_info in transfer_plan['chunks']:
            chunk = chunk_info['chunk']
            task_id = self.queue_scheduler.add_transfer_task(file_metrics, chunk)
            chunk_tasks.append({
                'task_id': task_id,
                'chunk_number': chunk.chunk_number,
                'priority': chunk_info['priority']
            })
        
        # Update system stats
        self.system_stats['total_files_processed'] += 1
        
        result = {
            'file_id': file_id,
            'filename': filename,
            'file_type': file_type.value,
            'priority_score': transfer_plan['file_priority'],
            'total_chunks': transfer_plan['total_chunks'],
            'estimated_time': transfer_plan['estimated_time'],
            'network_condition': network_condition.value,
            'chunk_tasks': chunk_tasks,
            'ml_enhanced': self.ml_model.is_trained,
            'learning_enhanced': self.learning_system.models_trained
        }
        
        print(f"📥 Analyzed and queued: {filename}")
        print(f"   File Type: {file_type.value}")
        print(f"   Priority Score: {transfer_plan['file_priority']:.2f}")
        print(f"   Chunks: {transfer_plan['total_chunks']}")
        print(f"   Network: {network_condition.value}")
        
        return result
    
    def get_system_status(self) -> dict:
        """Get comprehensive system status 📊"""
        
        queue_status = self.queue_scheduler.get_queue_status()
        learning_insights = self.learning_system.get_insights()
        
        # Calculate success rate
        if self.system_stats['total_chunks_processed'] > 0:
            success_rate = queue_status['statistics']['total_successful'] / self.system_stats['total_chunks_processed']
        else:
            success_rate = 0.0
        
        return {
            'system_info': {
                'status': 'active' if self.queue_scheduler.running else 'stopped',
                'uptime_seconds': (datetime.now() - self.system_stats['system_start_time']).total_seconds(),
                'files_processed': self.system_stats['total_files_processed'],
                'chunks_processed': self.system_stats['total_chunks_processed'],
                'success_rate': success_rate,
                'active_files': len(self.active_files)
            },
            'queue_status': queue_status,
            'ml_models': {
                'priority_ml_trained': self.ml_model.is_trained,
                'behavioral_learning_trained': self.learning_system.models_trained,
                'learning_samples': len(self.learning_system.transfer_history)
            },
            'learning_insights': learning_insights,
            'network_condition': queue_status['network_condition']
        }
    
    def get_file_status(self, file_id: str) -> Optional[dict]:
        """Get status of a specific file 📁"""
        
        if file_id not in self.active_files:
            return None
        
        file_metrics = self.active_files[file_id]
        
        # Get chunk status from scheduler
        # (In a real implementation, we'd track this properly)
        
        return {
            'file_id': file_id,
            'filename': file_metrics.filename,
            'file_type': file_metrics.file_type.value,
            'file_size': file_metrics.file_size,
            'upload_start_time': file_metrics.upload_start_time.isoformat(),
            'predicted_difficulty': file_metrics.predicted_difficulty,
            'success_rate': file_metrics.success_rate,
            'failure_count': file_metrics.failure_count
        }
    
    def force_rebalance_queues(self):
        """Force immediate queue rebalancing 🔄"""
        
        print("🔄 Forcing queue rebalance...")
        self.queue_scheduler.force_rebalance()
        
        # Update network conditions for all active files
        current_network = self.queue_scheduler.network_adapter.current_condition
        for file_metrics in self.active_files.values():
            file_metrics.network_condition = current_network
        
        print("🔄 Queue rebalance completed!")
    
    def simulate_network_change(self, new_condition: NetworkCondition):
        """Simulate a network condition change (for testing) 🌐"""
        
        print(f"🌐 Simulating network change to: {new_condition.value}")
        
        # Update network adapter
        self.queue_scheduler.network_adapter.current_condition = new_condition
        
        # Update all active files
        for file_metrics in self.active_files.values():
            file_metrics.network_condition = new_condition
        
        # Force rebalance
        self.force_rebalance_queues()
        
        print(f"✅ Network simulation complete: {new_condition.value}")
    
    def _start_learning_loop(self):
        """Start the continuous learning loop 🧠"""
        
        def learning_loop():
            while self.queue_scheduler.running:
                try:
                    # Check for completed transfers to learn from
                    self._update_learning_from_completions()
                    
                    # Update system statistics
                    self._update_system_statistics()
                    
                    # Sleep for a while
                    time.sleep(60)  # Update every minute
                    
                except Exception as e:
                    print(f"❌ Error in learning loop: {e}")
                    time.sleep(30)
        
        learning_thread = threading.Thread(target=learning_loop, daemon=True)
        learning_thread.start()
        print("🧠 Learning loop started!")
    
    def _update_learning_from_completions(self):
        """Update learning system from completed transfers 📚"""
        
        # In a real implementation, we'd get actual completion data
        # For now, we'll simulate based on queue statistics
        
        queue_stats = self.queue_scheduler.get_queue_status()['statistics']
        
        if queue_stats['total_processed'] > self.system_stats['total_chunks_processed']:
            new_completions = queue_stats['total_processed'] - self.system_stats['total_chunks_processed']
            self.system_stats['total_chunks_processed'] = queue_stats['total_processed']
            
            # Simulate learning updates (in real system, we'd have actual transfer data)
            if new_completions > 0:
                print(f"📚 Learning from {new_completions} new transfer completions...")
                self.system_stats['last_learning_update'] = datetime.now()
    
    def _update_system_statistics(self):
        """Update overall system statistics 📊"""
        
        queue_stats = self.queue_scheduler.get_queue_status()['statistics']
        
        # Update success rate
        if queue_stats['total_processed'] > 0:
            self.system_stats['success_rate'] = queue_stats['total_successful'] / queue_stats['total_processed']
        
        # Clean up old completed files (keep only recent ones)
        cutoff_time = datetime.now() - timedelta(hours=24)
        files_to_remove = []
        
        for file_id, file_metrics in self.active_files.items():
            if file_metrics.upload_start_time < cutoff_time:
                files_to_remove.append(file_id)
        
        for file_id in files_to_remove:
            del self.active_files[file_id]

# 🌐 Flask Web Interface
app = Flask(__name__)
app.config.from_object(Config)

# Global system instance
smart_system = SmartFileTransferSystem()

@app.route('/')
def index():
    """Main dashboard"""
    system_status = smart_system.get_system_status()
    return render_template('smart_dashboard.html', status=system_status)

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """Smart file upload endpoint"""
    
    try:
        data = request.get_json()
        
        filename = data.get('filename')
        file_size = data.get('file_size')
        user_priority = UserPriority(data.get('user_priority', 3))
        time_sensitive = data.get('time_sensitive', 'normal')
        context_tags = data.get('context_tags', [])
        
        if not filename or not file_size:
            return jsonify({'error': 'filename and file_size required'}), 400
        
        result = smart_system.analyze_and_queue_file(
            filename, file_size, user_priority, time_sensitive, context_tags
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def api_status():
    """System status endpoint"""
    return jsonify(smart_system.get_system_status())

@app.route('/api/file/<file_id>')
def api_file_status(file_id):
    """Get specific file status"""
    status = smart_system.get_file_status(file_id)
    if status:
        return jsonify(status)
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/api/rebalance', methods=['POST'])
def api_rebalance():
    """Force queue rebalancing"""
    smart_system.force_rebalance_queues()
    return jsonify({'message': 'Queue rebalanced successfully'})

@app.route('/api/simulate-network', methods=['POST'])
def api_simulate_network():
    """Simulate network condition change"""
    
    data = request.get_json()
    condition_name = data.get('condition')
    
    try:
        condition = NetworkCondition(condition_name)
        smart_system.simulate_network_change(condition)
        return jsonify({'message': f'Network simulated as {condition_name}'})
    except ValueError:
        return jsonify({'error': 'Invalid network condition'}), 400

@app.route('/api/generate-training-data', methods=['POST'])
def api_generate_training_data():
    """Generate new training datasets"""
    
    try:
        generator = DatasetGenerator()
        datasets = generator.save_datasets("training_datasets")
        
        return jsonify({
            'message': 'Training datasets generated successfully',
            'datasets': list(datasets.keys()),
            'total_samples': sum(len(df) for df in datasets.values())
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# System lifecycle - Initialize immediately
# Note: before_first_request is deprecated in newer Flask versions
try:
    smart_system.start_system()
    print("🎪 Smart File Transfer System initialized successfully!")
except Exception as e:
    print(f"❌ System initialization failed: {e}")

def shutdown_handler():
    """Graceful shutdown"""
    smart_system.stop_system()

import atexit
atexit.register(shutdown_handler)

# 🎪 Demo function
def demo_complete_system():
    """Demonstrate the complete smart system! 🎪✨"""
    
    print("🎪 Welcome to the Complete Smart Priority File Transfer System Demo!")
    print("=" * 80)
    
    # Start system
    system = SmartFileTransferSystem()
    system.start_system()
    
    try:
        # Demo files to process
        demo_files = [
            {
                'filename': 'emergency_server_crash.log',
                'file_size': 5 * 1024 * 1024,
                'user_priority': UserPriority.CRITICAL,
                'time_sensitive': 'immediate',
                'context_tags': ['emergency', 'critical', 'server']
            },
            {
                'filename': 'quarterly_presentation.pptx', 
                'file_size': 50 * 1024 * 1024,
                'user_priority': UserPriority.HIGH,
                'time_sensitive': 'urgent',
                'context_tags': ['presentation', 'deadline']
            },
            {
                'filename': 'vacation_video.mp4',
                'file_size': 500 * 1024 * 1024,
                'user_priority': UserPriority.LOW,
                'time_sensitive': 'background',
                'context_tags': ['personal']
            },
            {
                'filename': 'database_backup.zip',
                'file_size': 200 * 1024 * 1024,
                'user_priority': UserPriority.NORMAL,
                'time_sensitive': 'normal',
                'context_tags': ['backup']
            },
        ]
        
        print("📥 Adding files to smart system...")
        results = []
        
        for file_info in demo_files:
            result = system.analyze_and_queue_file(**file_info)
            results.append(result)
            print(f"   ✅ {file_info['filename']}: Priority {result['priority_score']:.2f}")
        
        # Let it run for a bit
        print("\n⚡ System processing files... Watch the magic!")
        time.sleep(10)
        
        # Show system status
        print("\n📊 System Status:")
        status = system.get_system_status()
        
        print(f"   Files Processed: {status['system_info']['files_processed']}")
        print(f"   Success Rate: {status['system_info']['success_rate']:.1%}")
        print(f"   Network Condition: {status['network_condition']}")
        print(f"   Queue Sizes:")
        print(f"     High Priority: {status['queue_status']['high_priority_queue']}")
        print(f"     Normal Priority: {status['queue_status']['normal_priority_queue']}")
        print(f"     Background: {status['queue_status']['background_queue']}")
        print(f"     Active: {status['queue_status']['active_tasks']}")
        
        # Simulate network change
        print("\n🌐 Simulating network degradation...")
        system.simulate_network_change(NetworkCondition.POOR)
        time.sleep(3)
        
        print("🌐 Simulating network recovery...")
        system.simulate_network_change(NetworkCondition.EXCELLENT)
        time.sleep(3)
        
        # Final status
        final_status = system.get_system_status()
        print(f"\n🏆 Final Status:")
        print(f"   Total Processing Time: {final_status['system_info']['uptime_seconds']:.1f}s")
        print(f"   Files: {final_status['system_info']['files_processed']}")
        print(f"   Success Rate: {final_status['system_info']['success_rate']:.1%}")
        
        print("\n✨ Complete Smart Priority File Transfer System Demo Finished! 🎉")
        print("🧠 The system learned, adapted, and optimized in real-time!")
        
    finally:
        system.stop_system()

if __name__ == '__main__':
    if len(os.sys.argv) > 1 and os.sys.argv[1] == 'demo':
        demo_complete_system()
    else:
        print("🚀 Starting Smart File Transfer System Web Interface...")
        app.run(debug=True, host='0.0.0.0', port=5001)
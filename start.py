#!/usr/bin/env python3
"""
Film Manager - Quick Start Script
Starts both the Django API and the frontend server
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a command in a subprocess"""
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        print(f"❌ Error starting command: {command}")
        print(f"Error: {e}")
        return None

def main():
    print("🎬 Film Manager - Starting both API and Frontend")
    print("=" * 50)

    project_root = Path(__file__).parent

    # Check if we're in the right directory
    if not (project_root / "manage.py").exists():
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)

    if not (project_root / "frontend" / "server.py").exists():
        print("❌ Error: frontend/server.py not found.")
        sys.exit(1)

    print("🚀 Starting Django API server...")
    api_process = run_command("python manage.py runserver", cwd=project_root)

    if api_process is None:
        print("❌ Failed to start API server")
        sys.exit(1)

    # Wait a moment for API to start
    time.sleep(2)

    print("🌐 Starting Frontend server...")
    frontend_process = run_command("python server.py", cwd=project_root / "frontend")

    if frontend_process is None:
        print("❌ Failed to start frontend server")
        api_process.terminate()
        sys.exit(1)

    print("\n✅ Both servers started successfully!")
    print("\n📋 Access your application at:")
    print("   🎭 Frontend: http://localhost:3000")
    print("   🔧 API:      http://localhost:8000")
    print("\n📖 API Documentation: http://localhost:8000/ (if browsable API enabled)")
    print("\n❌ Press Ctrl+C to stop both servers")

    try:
        # Wait for both processes
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        api_process.terminate()
        frontend_process.terminate()

        # Wait for processes to terminate
        try:
            api_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            api_process.kill()
            frontend_process.kill()

        print("👋 Both servers stopped. Goodbye!")

if __name__ == "__main__":
    main()
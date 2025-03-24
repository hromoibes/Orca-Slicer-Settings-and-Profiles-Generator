#!/bin/bash
# Run tests for Orca Slicer Settings Generator

# Set up environment
echo "Setting up test environment..."
mkdir -p /home/ubuntu/orca_slicer_generator/data/test
mkdir -p /home/ubuntu/orca_slicer_generator/data/test/exports

# Run unit tests
echo -e "\n=== Running Unit Tests ==="
python3 /home/ubuntu/orca_slicer_generator/tests/test_application.py

# Run integration tests
echo -e "\n=== Running Integration Tests ==="
python3 /home/ubuntu/orca_slicer_generator/tests/integration_test.py --data-dir /home/ubuntu/orca_slicer_generator/data/test --output-dir /home/ubuntu/orca_slicer_generator/data/test/exports

echo -e "\n=== Tests Completed ==="

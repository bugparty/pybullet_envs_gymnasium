# Testing Guide

This directory contains comprehensive tests for HopperBulletEnv-v0 and AsyncVectorEnv compatibility.

## Test Files

### test_hopper.py
Basic functionality tests for HopperBulletEnv-v0:
- Environment creation and reset
- Step execution
- Gymnasium environment checker validation
- 100-step episode testing

**Run**: `python test_hopper.py`

### test_async_env.py
AsyncVectorEnv compatibility tests:
- Parallel environment creation (4 envs)
- Parallel reset and step
- Numpy random number generator verification
- Gymnasium version compatibility check

**Run**: `python test_async_env.py`

### diagnose_hopper.py
Detailed diagnostic script:
- Multi-episode testing with statistics
- Reward component breakdown
- Observation space analysis
- Zero-action gravity test

**Run**: `python diagnose_hopper.py`

## GitHub Actions CI

The project includes two CI workflows:

1. **ci.yml** - Main CI pipeline
   - Python 3.9, 3.10, 3.11, 3.12
   - Linting, type checking, pytest
   - Runs all three test scripts

2. **test-async-env.yml** - AsyncVectorEnv specific tests
   - Matrix testing (2, 4, 8 parallel envs)
   - Seed reproducibility verification
   - Multiprocessing safety tests

## Quick Start

```bash
# Install package
pip install -e .

# Run all tests
python test_hopper.py
python test_async_env.py
python diagnose_hopper.py

# Run pytest suite
pytest tests/ -v
```

## Key Features Tested

✅ HopperBulletEnv-v0 full functionality
✅ AsyncVectorEnv compatibility (2-8 parallel environments)
✅ Numpy random number generator (proper seeding)
✅ Gymnasium API compliance
✅ Stable Baselines3 compatibility
✅ Python 3.9-3.12 support

## Expected Results

- **Random policy**: 10-20 steps per episode, low rewards
- **Trained policy**: 100+ steps, rewards approaching 2500+
- **AsyncVectorEnv**: No RNG issues, independent environment behavior
- **Reproducibility**: Same seed produces identical results

## Troubleshooting

If tests fail with display errors, use xvfb:
```bash
xvfb-run -a python test_hopper.py
```

## Contributing

When adding new tests, ensure they:
- Work on Python 3.9-3.12
- Are purely in English
- Include clear docstrings
- Pass CI checks

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

### record_video.py
Video recording script:
- Records HopperBulletEnv-v0 in action
- Generates MP4 video (5 seconds, 30 fps)
- Uses rgb_array render mode
- Visual verification of environment behavior

**Run**: `python record_video.py`

## GitHub Actions CI

The project includes three CI workflows:

1. **ci.yml** - Main CI pipeline
   - Python 3.9, 3.10, 3.11, 3.12
   - Linting, type checking, pytest
   - Runs all test scripts
   - Records demo video (Python 3.11 only)
   - Uploads video as artifact (30 days retention)

2. **test-async-env.yml** - AsyncVectorEnv specific tests
   - Matrix testing (2, 4, 8 parallel envs)
   - Seed reproducibility verification
   - Multiprocessing safety tests

3. **generate-videos.yml** - Demo video generation
   - Manual trigger or on code changes
   - Records HopperBulletEnv-v0 videos
   - Uploads videos as artifacts (90 days retention)

## Quick Start

```bash
# Install package
pip install -e .

# Run all tests
python test_hopper.py
python test_async_env.py
python diagnose_hopper.py

# Record demo video
python record_video.py

# Run pytest suite
pytest tests/ -v
```

## Video Recording

Generate visual demonstrations of the environment:

```bash
# Record 5-second video with random policy
python record_video.py

# Install dependencies if needed
pip install imageio imageio-ffmpeg
```

**Output**: `hopper_random_policy.mp4` (approximately 0.3 MB)

The video demonstrates:
- Environment rendering works correctly
- Physics simulation is functioning
- Robot dynamics are realistic
- rgb_array render mode is operational

## Key Features Tested

✅ HopperBulletEnv-v0 full functionality
✅ AsyncVectorEnv compatibility (2-8 parallel environments)
✅ Numpy random number generator (proper seeding)
✅ Gymnasium API compliance
✅ Stable Baselines3 compatibility
✅ Python 3.9-3.12 support
✅ Video rendering (rgb_array mode)

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

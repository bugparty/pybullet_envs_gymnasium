# GitHub Actions CI Workflows

This directory contains GitHub Actions workflows for continuous integration testing.

## Workflows

### 1. `ci.yml` - Main CI Pipeline

**Trigger**: Push to `master`, Pull Requests

**Jobs**:
- **Build & Test** (Python 3.9, 3.10, 3.11, 3.12)
  - Lint with ruff
  - Check code style with black
  - Type check with mypy
  - Run pytest test suite
  - Test HopperBulletEnv-v0 functionality
  - Test AsyncVectorEnv compatibility
  - Run diagnostic tests

**Features**:
- Matrix testing across Python versions
- Skips CI if commit message contains `[ci skip]`
- Uses `uv` for faster dependency installation
- Installs PyTorch CPU version to test with Stable Baselines3

### 2. `test-async-env.yml` - AsyncVectorEnv Tests

**Trigger**: Push to `master`, Pull Requests, Manual dispatch

**Jobs**:

#### test-async-compatibility
Tests AsyncVectorEnv with different configurations:
- **Python versions**: 3.9, 3.11, 3.12
- **Number of environments**: 2, 4, 8

Validates:
- Correct observation shapes
- Step execution
- Different environments produce different rewards (RNG works correctly)

#### test-seed-reproducibility
Verifies that:
- Same seed produces identical results
- Environment state is deterministic when seeded
- Observations and rewards are reproducible

#### test-multiprocessing
Tests:
- Multiprocessing safety
- Different seeds produce different behaviors
- No RNG state leakage between processes

## Running Workflows Locally

### Main CI Tests
```bash
# Install dependencies
pip install -e .
pip install "stable-baselines3[tests]>=2.4.0a11"

# Run linting
make lint

# Check code style
make check-codestyle

# Type check
make mypy

# Run tests
make pytest
python test_hopper.py
python test_async_env.py
python diagnose_hopper.py
```

### AsyncVectorEnv Tests
```bash
# Install dependencies
pip install -e .

# Test with 4 parallel environments
python -c "
from gymnasium.vector import AsyncVectorEnv
import gymnasium as gym
import pybullet_envs_gymnasium

envs = AsyncVectorEnv([lambda: gym.make('HopperBulletEnv-v0') for _ in range(4)])
obs = envs.reset()
print(f'Observation shape: {obs[0].shape}')
envs.close()
"

# Test seed reproducibility
python -c "
import gymnasium as gym
import pybullet_envs_gymnasium

env = gym.make('HopperBulletEnv-v0')
obs1, _ = env.reset(seed=42)
env.close()

env = gym.make('HopperBulletEnv-v0')
obs2, _ = env.reset(seed=42)
env.close()

import numpy as np
print(f'Observations identical: {np.allclose(obs1, obs2)}')
"
```

## Badge Status

Add these badges to your README.md:

```markdown
[![CI](https://github.com/araffin/pybullet_envs_gymnasium/workflows/CI/badge.svg)](https://github.com/araffin/pybullet_envs_gymnasium/actions/workflows/ci.yml)
[![AsyncVectorEnv Tests](https://github.com/araffin/pybullet_envs_gymnasium/workflows/AsyncVectorEnv%20Tests/badge.svg)](https://github.com/araffin/pybullet_envs_gymnasium/actions/workflows/test-async-env.yml)
```

## Troubleshooting

### PyBullet GUI Issues
If tests fail with display errors, ensure `xvfb` is used:
```bash
xvfb-run -a python test_hopper.py
```

### AsyncVectorEnv Hangs
If AsyncVectorEnv tests hang:
1. Check for PyBullet GUI mode being enabled (should use DIRECT mode)
2. Verify proper environment cleanup in `close()`
3. Check for deadlocks in multiprocessing

### RNG Issues
If tests fail with identical rewards across environments:
1. Verify `gymnasium.utils.seeding.np_random()` is used
2. Check that each environment gets a unique seed
3. Ensure `self.np_random` is properly set in `reset()`

## Contributing

When adding new tests:
1. Add them to the appropriate workflow
2. Ensure they work with all Python versions (3.9-3.12)
3. Use `xvfb-run` for headless PyBullet tests
4. Test locally before pushing

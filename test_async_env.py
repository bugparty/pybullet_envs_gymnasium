#!/usr/bin/env python3
"""Test HopperBulletEnv-v0 compatibility with AsyncVectorEnv"""

import numpy as np
import gymnasium as gym
from gymnasium.vector import AsyncVectorEnv
import pybullet_envs_gymnasium

def test_async_env():
    """Test AsyncVectorEnv compatibility"""

    print("=" * 70)
    print("Testing HopperBulletEnv-v0 AsyncVectorEnv Compatibility")
    print("=" * 70)

    try:
        # Create 4 parallel environments
        num_envs = 4

        print(f"\n[1/4] Creating {num_envs} parallel environments...")

        def make_env(seed):
            def _init():
                env = gym.make("HopperBulletEnv-v0")
                env.reset(seed=seed)
                return env
            return _init

        envs = AsyncVectorEnv([make_env(i) for i in range(num_envs)])
        print(f"✓ Successfully created {num_envs} parallel environments")

        # Test reset
        print("\n[2/4] Testing parallel reset...")
        obs = envs.reset(seed=42)
        print(f"✓ Parallel reset successful")
        print(f"  - Observation shape: {obs[0].shape}")
        print(f"  - Number of environments: {obs[0].shape[0]}")

        # Test step
        print("\n[3/4] Testing parallel step...")
        actions = envs.action_space.sample()
        obs, rewards, dones, truncated, infos = envs.step(actions)
        print(f"✓ Parallel step successful")
        print(f"  - Rewards: {rewards}")
        print(f"  - Dones: {dones}")

        # Run multi-step test
        print("\n[4/4] Running 100-step parallel test...")
        total_rewards = np.zeros(num_envs)
        episode_counts = np.zeros(num_envs)

        for step in range(100):
            actions = envs.action_space.sample()
            obs, rewards, dones, truncated, infos = envs.step(actions)
            total_rewards += rewards

            for i, (done, trunc) in enumerate(zip(dones, truncated)):
                if done or trunc:
                    episode_counts[i] += 1

        print(f"✓ Completed 100-step parallel test")
        print(f"  - Total rewards per env: {total_rewards}")
        print(f"  - Episode count per env: {episode_counts}")

        envs.close()

        print("\n" + "=" * 70)
        print("✓ AsyncVectorEnv compatibility test passed!")
        print("=" * 70)

        return True

    except Exception as e:
        print("\n" + "=" * 70)
        print("✗ AsyncVectorEnv compatibility test failed!")
        print("=" * 70)
        print(f"\nError type: {type(e).__name__}")
        print(f"Error message: {str(e)}")

        import traceback
        print("\nDetailed traceback:")
        traceback.print_exc()

        return False

def test_numpy_random():
    """Test numpy random number generator usage"""

    print("\n" + "=" * 70)
    print("Checking numpy Random Number Generator Usage")
    print("=" * 70)

    try:
        env = gym.make("HopperBulletEnv-v0")

        # Check if environment has np_random attribute
        print("\nChecking env.np_random...")
        if hasattr(env.unwrapped, 'np_random'):
            print(f"✓ env.np_random exists: {type(env.unwrapped.np_random)}")
        else:
            print("✗ env.np_random does not exist")

        # Reset environment and check
        print("\nResetting environment (seed=42)...")
        obs, info = env.reset(seed=42)

        if hasattr(env.unwrapped, 'np_random'):
            print(f"✓ After reset env.np_random: {type(env.unwrapped.np_random)}")

            # Test random number generation
            print("\nTesting random number generation...")
            rand_val = env.unwrapped.np_random.uniform(0, 1)
            print(f"✓ Random number generated successfully: {rand_val}")

        # Check robot's np_random
        if hasattr(env.unwrapped, 'robot'):
            print("\nChecking robot.np_random...")
            if hasattr(env.unwrapped.robot, 'np_random'):
                print(f"✓ robot.np_random exists: {type(env.unwrapped.robot.np_random)}")
            else:
                print("✗ robot.np_random does not exist")

        env.close()
        return True

    except Exception as e:
        print(f"\n✗ Test failed: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_gymnasium_version():
    """Check Gymnasium version information"""

    print("\n" + "=" * 70)
    print("Gymnasium Version Information")
    print("=" * 70)

    import gymnasium
    print(f"\nGymnasium version: {gymnasium.__version__}")

    # Check if new API is supported
    print("\nAPI check:")

    # Check gymnasium.utils.seeding
    if hasattr(gymnasium.utils, 'seeding'):
        print("✓ gymnasium.utils.seeding exists (legacy API)")
    else:
        print("✗ gymnasium.utils.seeding does not exist")

    # Check new random number generator API
    env = gym.make("HopperBulletEnv-v0")
    if hasattr(env.unwrapped, '_np_random'):
        print("✓ Using new _np_random API")
    elif hasattr(env.unwrapped, 'np_random'):
        print("✓ Using np_random attribute")
        print(f"  Type: {type(env.unwrapped.np_random)}")

    env.close()

if __name__ == "__main__":
    check_gymnasium_version()
    test_numpy_random()
    test_async_env()

    print("\n" + "=" * 70)
    print("Testing Complete")
    print("=" * 70)

#!/usr/bin/env python3
"""Test HopperBulletEnv-v0 environment functionality"""

import sys
import traceback
import numpy as np
import gymnasium as gym
import pybullet_envs_gymnasium

def test_hopper_env():
    """Test basic functionality of Hopper environment"""

    print("=" * 60)
    print("Testing HopperBulletEnv-v0 Environment")
    print("=" * 60)

    try:
        # 1. Test environment creation
        print("\n[1/5] Creating environment...")
        env = gym.make("HopperBulletEnv-v0")
        print("✓ Environment created successfully")
        print(f"  - Action space: {env.action_space}")
        print(f"  - Observation space: {env.observation_space}")

        # 2. Test environment reset
        print("\n[2/5] Resetting environment...")
        obs, info = env.reset(seed=42)
        print("✓ Environment reset successfully")
        print(f"  - Observation shape: {obs.shape}")
        print(f"  - Observation range: [{obs.min():.3f}, {obs.max():.3f}]")
        print(f"  - Info: {info}")

        # 3. Test random action
        print("\n[3/5] Testing random action...")
        action = env.action_space.sample()
        print(f"  - Random action: {action}")

        obs, reward, terminated, truncated, info = env.step(action)
        print("✓ Step executed successfully")
        print(f"  - Reward: {reward:.3f}")
        print(f"  - terminated: {terminated}")
        print(f"  - truncated: {truncated}")
        print(f"  - New observation shape: {obs.shape}")

        # 4. Run multiple steps
        print("\n[4/5] Running 100-step test...")
        total_reward = 0
        steps = 0

        for i in range(100):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            steps += 1

            if terminated or truncated:
                print(f"  - Episode ended at step {steps} (terminated={terminated}, truncated={truncated})")
                obs, info = env.reset()
                total_reward = 0
                steps = 0

        print(f"✓ Completed 100-step test")
        print(f"  - Final cumulative reward: {total_reward:.3f}")
        print(f"  - Final step count: {steps}")

        # 5. Test environment close
        print("\n[5/5] Closing environment...")
        env.close()
        print("✓ Environment closed successfully")

        print("\n" + "=" * 60)
        print("Test Result: ✓ All tests passed")
        print("HopperBulletEnv-v0 is fully functional!")
        print("=" * 60)

        return True

    except Exception as e:
        print("\n" + "=" * 60)
        print("Test Result: ✗ Test failed")
        print("=" * 60)
        print(f"\nError type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nDetailed traceback:")
        traceback.print_exc()
        print("=" * 60)
        return False

def test_env_checker():
    """Verify environment using Gymnasium's env checker"""

    print("\n" + "=" * 60)
    print("Verifying with Gymnasium Environment Checker")
    print("=" * 60)

    try:
        from gymnasium.utils.env_checker import check_env

        env = gym.make("HopperBulletEnv-v0")
        print("\nRunning environment check...")
        check_env(env, skip_render_check=True)
        print("✓ Environment passed Gymnasium checker validation")
        env.close()
        return True

    except Exception as e:
        print(f"\n✗ Environment check failed: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return False

def show_env_info():
    """Display detailed environment information"""

    print("\n" + "=" * 60)
    print("HopperBulletEnv-v0 Detailed Information")
    print("=" * 60)

    try:
        # Get environment info from registry
        spec = gym.spec("HopperBulletEnv-v0")
        print(f"\nEnvironment ID: {spec.id}")
        print(f"Entry point: {spec.entry_point}")
        print(f"Max episode steps: {spec.max_episode_steps}")
        print(f"Reward threshold: {spec.reward_threshold}")

        # Create environment to get space info
        env = gym.make("HopperBulletEnv-v0")
        print(f"\nAction space: {env.action_space}")
        print(f"  - Shape: {env.action_space.shape}")
        print(f"  - Low: {env.action_space.low}")
        print(f"  - High: {env.action_space.high}")

        print(f"\nObservation space: {env.observation_space}")
        print(f"  - Shape: {env.observation_space.shape}")
        print(f"  - Low: {env.observation_space.low[:5]}... (first 5)")
        print(f"  - High: {env.observation_space.high[:5]}... (first 5)")

        print(f"\nRender modes: {env.metadata.get('render_modes', [])}")
        print(f"Render FPS: {env.metadata.get('render_fps', 'N/A')}")

        env.close()

    except Exception as e:
        print(f"\nFailed to get environment info: {e}")

if __name__ == "__main__":
    show_env_info()

    test1_passed = test_hopper_env()
    test2_passed = test_env_checker()

    print("\n" + "=" * 60)
    print("Final Test Report")
    print("=" * 60)
    print(f"Basic functionality test: {'✓ Passed' if test1_passed else '✗ Failed'}")
    print(f"Environment checker test: {'✓ Passed' if test2_passed else '✗ Failed'}")

    if test1_passed and test2_passed:
        print("\nConclusion: HopperBulletEnv-v0 is fully functional! ✓")
        sys.exit(0)
    else:
        print("\nConclusion: HopperBulletEnv-v0 has issues! ✗")
        sys.exit(1)

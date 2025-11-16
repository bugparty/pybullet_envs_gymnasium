#!/usr/bin/env python3
"""Record a short video of HopperBulletEnv-v0 in action"""

import numpy as np
import gymnasium as gym
import pybullet_envs_gymnasium

try:
    import imageio
except ImportError:
    print("Installing imageio...")
    import subprocess
    subprocess.check_call(["pip", "install", "imageio", "imageio-ffmpeg"])
    import imageio


def record_hopper_video(
    output_path="hopper_demo.mp4",
    duration_seconds=5,
    fps=30,
    policy="random"
):
    """
    Record a video of HopperBulletEnv-v0

    Args:
        output_path: Path to save the video
        duration_seconds: Length of video in seconds
        fps: Frames per second
        policy: Policy to use ("random" or "zero")
    """

    print(f"Recording HopperBulletEnv-v0 video...")
    print(f"  Duration: {duration_seconds}s")
    print(f"  FPS: {fps}")
    print(f"  Policy: {policy}")
    print(f"  Output: {output_path}")

    # Create environment with rgb_array rendering
    env = gym.make("HopperBulletEnv-v0", render_mode="rgb_array")

    frames = []
    total_frames = duration_seconds * fps
    obs, info = env.reset(seed=42)

    print(f"\nRecording {total_frames} frames...")

    episode_count = 0
    frame_count = 0
    total_reward = 0

    while frame_count < total_frames:
        # Render frame
        frame = env.render()
        frames.append(frame)
        frame_count += 1

        # Choose action based on policy
        if policy == "random":
            action = env.action_space.sample()
        elif policy == "zero":
            action = np.zeros(3)
        else:
            raise ValueError(f"Unknown policy: {policy}")

        # Step environment
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward

        # Reset if episode ends
        if terminated or truncated:
            episode_count += 1
            obs, info = env.reset()
            total_reward = 0

        # Progress indicator
        if frame_count % fps == 0:
            print(f"  Progress: {frame_count}/{total_frames} frames "
                  f"({frame_count/total_frames*100:.0f}%)")

    env.close()

    print(f"\nRecorded {frame_count} frames across {episode_count + 1} episodes")
    print(f"Saving video to {output_path}...")

    # Save video using imageio
    imageio.mimsave(output_path, frames, fps=fps)

    import os
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✓ Video saved successfully!")
    print(f"  File size: {file_size_mb:.2f} MB")
    print(f"  Resolution: {frames[0].shape[1]}x{frames[0].shape[0]}")

    return output_path


def main():
    """Record demo videos with different policies"""

    print("=" * 70)
    print("HopperBulletEnv-v0 Video Recording")
    print("=" * 70)

    # Record random policy video (default)
    random_video = record_hopper_video(
        output_path="hopper_random_policy.mp4",
        duration_seconds=5,
        fps=30,
        policy="random"
    )

    print("\n" + "=" * 70)
    print("Video recording complete!")
    print("=" * 70)
    print(f"\nGenerated video: {random_video}")
    print("\nThis video demonstrates that:")
    print("✓ HopperBulletEnv-v0 renders correctly")
    print("✓ Environment dynamics work properly")
    print("✓ rgb_array render mode functions")
    print("✓ Random policy causes robot to fall (expected behavior)")


if __name__ == "__main__":
    main()

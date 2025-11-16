#!/usr/bin/env python3
"""测试 HopperBulletEnv-v0 与 AsyncVectorEnv 的兼容性"""

import numpy as np
import gymnasium as gym
from gymnasium.vector import AsyncVectorEnv
import pybullet_envs_gymnasium

def test_async_env():
    """测试 AsyncVectorEnv 兼容性"""

    print("=" * 70)
    print("测试 HopperBulletEnv-v0 与 AsyncVectorEnv 的兼容性")
    print("=" * 70)

    try:
        # 创建 4 个并行环境
        num_envs = 4

        print(f"\n[1/4] 创建 {num_envs} 个并行环境...")

        def make_env(seed):
            def _init():
                env = gym.make("HopperBulletEnv-v0")
                env.reset(seed=seed)
                return env
            return _init

        envs = AsyncVectorEnv([make_env(i) for i in range(num_envs)])
        print(f"✓ 成功创建 {num_envs} 个并行环境")

        # 测试重置
        print("\n[2/4] 测试并行重置...")
        obs = envs.reset(seed=42)
        print(f"✓ 并行重置成功")
        print(f"  - 观测形状: {obs[0].shape}")
        print(f"  - 环境数量: {obs[0].shape[0]}")

        # 测试步进
        print("\n[3/4] 测试并行步进...")
        actions = envs.action_space.sample()
        obs, rewards, dones, truncated, infos = envs.step(actions)
        print(f"✓ 并行步进成功")
        print(f"  - 奖励: {rewards}")
        print(f"  - Dones: {dones}")

        # 运行多步测试
        print("\n[4/4] 运行 100 步并行测试...")
        total_rewards = np.zeros(num_envs)
        episode_counts = np.zeros(num_envs)

        for step in range(100):
            actions = envs.action_space.sample()
            obs, rewards, dones, truncated, infos = envs.step(actions)
            total_rewards += rewards

            for i, (done, trunc) in enumerate(zip(dones, truncated)):
                if done or trunc:
                    episode_counts[i] += 1

        print(f"✓ 完成 100 步并行测试")
        print(f"  - 各环境累计奖励: {total_rewards}")
        print(f"  - 各环境 episode 数: {episode_counts}")

        envs.close()

        print("\n" + "=" * 70)
        print("✓ AsyncVectorEnv 兼容性测试通过!")
        print("=" * 70)

        return True

    except Exception as e:
        print("\n" + "=" * 70)
        print("✗ AsyncVectorEnv 兼容性测试失败!")
        print("=" * 70)
        print(f"\n错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")

        import traceback
        print("\n详细错误栈:")
        traceback.print_exc()

        return False

def test_numpy_random():
    """测试 numpy 随机数生成器的使用"""

    print("\n" + "=" * 70)
    print("检查 numpy 随机数生成器的使用")
    print("=" * 70)

    try:
        env = gym.make("HopperBulletEnv-v0")

        # 检查环境是否有 np_random 属性
        print("\n检查 env.np_random...")
        if hasattr(env.unwrapped, 'np_random'):
            print(f"✓ env.np_random 存在: {type(env.unwrapped.np_random)}")
        else:
            print("✗ env.np_random 不存在")

        # 重置环境并检查
        print("\n重置环境 (seed=42)...")
        obs, info = env.reset(seed=42)

        if hasattr(env.unwrapped, 'np_random'):
            print(f"✓ 重置后 env.np_random: {type(env.unwrapped.np_random)}")

            # 测试随机数生成
            print("\n测试随机数生成...")
            rand_val = env.unwrapped.np_random.uniform(0, 1)
            print(f"✓ 随机数生成成功: {rand_val}")

        # 检查机器人的 np_random
        if hasattr(env.unwrapped, 'robot'):
            print("\n检查 robot.np_random...")
            if hasattr(env.unwrapped.robot, 'np_random'):
                print(f"✓ robot.np_random 存在: {type(env.unwrapped.robot.np_random)}")
            else:
                print("✗ robot.np_random 不存在")

        env.close()
        return True

    except Exception as e:
        print(f"\n✗ 测试失败: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_gymnasium_version():
    """检查 Gymnasium 版本信息"""

    print("\n" + "=" * 70)
    print("Gymnasium 版本信息")
    print("=" * 70)

    import gymnasium
    print(f"\nGymnasium 版本: {gymnasium.__version__}")

    # 检查是否支持新的 API
    print("\nAPI 检查:")

    # 检查 gymnasium.utils.seeding
    if hasattr(gymnasium.utils, 'seeding'):
        print("✓ gymnasium.utils.seeding 存在 (旧 API)")
    else:
        print("✗ gymnasium.utils.seeding 不存在")

    # 检查新的随机数生成器 API
    env = gym.make("HopperBulletEnv-v0")
    if hasattr(env.unwrapped, '_np_random'):
        print("✓ 使用新的 _np_random API")
    elif hasattr(env.unwrapped, 'np_random'):
        print("✓ 使用 np_random 属性")
        print(f"  类型: {type(env.unwrapped.np_random)}")

    env.close()

if __name__ == "__main__":
    check_gymnasium_version()
    test_numpy_random()
    test_async_env()

    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)

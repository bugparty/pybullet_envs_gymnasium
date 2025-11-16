#!/usr/bin/env python3
"""测试 HopperBulletEnv-v0 环境是否可用"""

import sys
import traceback
import numpy as np
import gymnasium as gym
import pybullet_envs_gymnasium

def test_hopper_env():
    """测试 Hopper 环境的基本功能"""

    print("=" * 60)
    print("测试 HopperBulletEnv-v0 环境")
    print("=" * 60)

    try:
        # 1. 测试环境创建
        print("\n[1/5] 创建环境...")
        env = gym.make("HopperBulletEnv-v0")
        print("✓ 环境创建成功")
        print(f"  - 动作空间: {env.action_space}")
        print(f"  - 观测空间: {env.observation_space}")

        # 2. 测试环境重置
        print("\n[2/5] 重置环境...")
        obs, info = env.reset(seed=42)
        print("✓ 环境重置成功")
        print(f"  - 观测维度: {obs.shape}")
        print(f"  - 观测值范围: [{obs.min():.3f}, {obs.max():.3f}]")
        print(f"  - Info: {info}")

        # 3. 测试随机动作
        print("\n[3/5] 测试随机动作...")
        action = env.action_space.sample()
        print(f"  - 随机动作: {action}")

        obs, reward, terminated, truncated, info = env.step(action)
        print("✓ 步进成功")
        print(f"  - 奖励: {reward:.3f}")
        print(f"  - terminated: {terminated}")
        print(f"  - truncated: {truncated}")
        print(f"  - 新观测维度: {obs.shape}")

        # 4. 运行多个步骤
        print("\n[4/5] 运行 100 步测试...")
        total_reward = 0
        steps = 0

        for i in range(100):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            steps += 1

            if terminated or truncated:
                print(f"  - 第 {steps} 步结束 (terminated={terminated}, truncated={truncated})")
                obs, info = env.reset()
                total_reward = 0
                steps = 0

        print(f"✓ 完成 100 步测试")
        print(f"  - 最终累计奖励: {total_reward:.3f}")
        print(f"  - 最终步数: {steps}")

        # 5. 测试环境关闭
        print("\n[5/5] 关闭环境...")
        env.close()
        print("✓ 环境关闭成功")

        print("\n" + "=" * 60)
        print("测试结果: ✓ 所有测试通过")
        print("HopperBulletEnv-v0 环境完全可用!")
        print("=" * 60)

        return True

    except Exception as e:
        print("\n" + "=" * 60)
        print("测试结果: ✗ 测试失败")
        print("=" * 60)
        print(f"\n错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print("\n详细错误栈:")
        traceback.print_exc()
        print("=" * 60)
        return False

def test_env_checker():
    """使用 Gymnasium 的环境检查器验证环境"""

    print("\n" + "=" * 60)
    print("使用 Gymnasium 环境检查器验证")
    print("=" * 60)

    try:
        from gymnasium.utils.env_checker import check_env

        env = gym.make("HopperBulletEnv-v0")
        print("\n运行环境检查...")
        check_env(env, skip_render_check=True)
        print("✓ 环境通过 Gymnasium 检查器验证")
        env.close()
        return True

    except Exception as e:
        print(f"\n✗ 环境检查失败: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return False

def show_env_info():
    """显示环境的详细信息"""

    print("\n" + "=" * 60)
    print("HopperBulletEnv-v0 详细信息")
    print("=" * 60)

    try:
        # 从注册表获取环境信息
        spec = gym.spec("HopperBulletEnv-v0")
        print(f"\n环境ID: {spec.id}")
        print(f"入口点: {spec.entry_point}")
        print(f"最大步数: {spec.max_episode_steps}")
        print(f"奖励阈值: {spec.reward_threshold}")

        # 创建环境获取空间信息
        env = gym.make("HopperBulletEnv-v0")
        print(f"\n动作空间: {env.action_space}")
        print(f"  - 形状: {env.action_space.shape}")
        print(f"  - 最小值: {env.action_space.low}")
        print(f"  - 最大值: {env.action_space.high}")

        print(f"\n观测空间: {env.observation_space}")
        print(f"  - 形状: {env.observation_space.shape}")
        print(f"  - 最小值: {env.observation_space.low[:5]}... (前5个)")
        print(f"  - 最大值: {env.observation_space.high[:5]}... (前5个)")

        print(f"\n渲染模式: {env.metadata.get('render_modes', [])}")
        print(f"渲染FPS: {env.metadata.get('render_fps', 'N/A')}")

        env.close()

    except Exception as e:
        print(f"\n获取环境信息失败: {e}")

if __name__ == "__main__":
    show_env_info()

    test1_passed = test_hopper_env()
    test2_passed = test_env_checker()

    print("\n" + "=" * 60)
    print("最终测试报告")
    print("=" * 60)
    print(f"基本功能测试: {'✓ 通过' if test1_passed else '✗ 失败'}")
    print(f"环境检查器测试: {'✓ 通过' if test2_passed else '✗ 失败'}")

    if test1_passed and test2_passed:
        print("\n结论: HopperBulletEnv-v0 完全可用! ✓")
        sys.exit(0)
    else:
        print("\n结论: HopperBulletEnv-v0 存在问题! ✗")
        sys.exit(1)

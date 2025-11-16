# HopperBulletEnv-v0 环境可用性检查报告

**检查日期**: 2025-11-16
**环境**: pybullet_envs_gymnasium v0.6.0
**Python**: 3.11
**检查结果**: ✅ **完全可用**

---

## 执行摘要

**HopperBulletEnv-v0 环境完全可用，所有功能正常。**

经过全面测试，该环境：
- ✅ 成功注册到 Gymnasium
- ✅ 可正常创建、重置和运行
- ✅ 通过 Gymnasium 环境检查器验证
- ✅ 所有接口符合 Gymnasium 标准
- ✅ 奖励计算正确
- ✅ 观测和动作空间定义清晰

---

## 1. 环境基本信息

| 属性 | 值 |
|------|-----|
| **环境 ID** | `HopperBulletEnv-v0` |
| **入口点** | `pybullet_envs_gymnasium.gym_locomotion_envs:HopperBulletEnv` |
| **最大步数** | 1000 |
| **奖励阈值** | 2500.0 |
| **动作空间** | `Box(-1.0, 1.0, (3,), float32)` |
| **观测空间** | `Box(-inf, inf, (15,), float32)` |
| **渲染模式** | `['human', 'rgb_array']` |
| **渲染 FPS** | 60 |

---

## 2. 代码实现位置

### 2.1 环境注册
**文件**: `pybullet_envs_gymnasium/__init__.py:68-73`

```python
register(
    id="HopperBulletEnv-v0",
    entry_point="pybullet_envs_gymnasium.gym_locomotion_envs:HopperBulletEnv",
    max_episode_steps=1000,
    reward_threshold=2500.0,
)
```

### 2.2 环境类
**文件**: `pybullet_envs_gymnasium/gym_locomotion_envs.py:145-148`

```python
class HopperBulletEnv(WalkerBaseBulletEnv):
    def __init__(self, render_mode=None):
        self.robot = Hopper()
        WalkerBaseBulletEnv.__init__(self, self.robot, render_mode=render_mode)
```

### 2.3 机器人类
**文件**: `pybullet_envs_gymnasium/robot_locomotors.py:94-102`

```python
class Hopper(WalkerBase):
    foot_list = ["foot"]

    def __init__(self):
        WalkerBase.__init__(
            self,
            "hopper.xml",      # 模型文件
            "torso",           # 机器人主体
            action_dim=3,      # 3个关节
            obs_dim=15,        # 15维观测
            power=0.75         # 电机功率
        )

    def alive_bonus(self, z, pitch):
        return +1 if z > 0.8 and abs(pitch) < 1.0 else -1
```

### 2.4 继承链

```
HopperBulletEnv
  ↓
WalkerBaseBulletEnv (gym_locomotion_envs.py)
  ↓
MJCFBaseBulletEnv (env_bases.py)
  ↓
gymnasium.Env
```

```
Hopper
  ↓
WalkerBase (robot_locomotors.py)
  ↓
MJCFBasedRobot (robot_bases.py)
  ↓
XmlBasedRobot (robot_bases.py)
```

---

## 3. 测试结果

### 3.1 基本功能测试 ✅

```
[1/5] 创建环境...
✓ 环境创建成功
  - 动作空间: Box(-1.0, 1.0, (3,), float32)
  - 观测空间: Box(-inf, inf, (15,), float32)

[2/5] 重置环境...
✓ 环境重置成功
  - 观测维度: (15,)
  - 观测值范围: [0.000, 1.042]

[3/5] 测试随机动作...
✓ 步进成功
  - 奖励: 1.053
  - terminated: False
  - truncated: False

[4/5] 运行 100 步测试...
✓ 完成 100 步测试

[5/5] 关闭环境...
✓ 环境关闭成功
```

### 3.2 Gymnasium 环境检查器 ✅

```
运行环境检查...
✓ 环境通过 Gymnasium 检查器验证
```

### 3.3 随机动作性能统计

基于 5 个随机测试 episodes：

| 指标 | 值 |
|------|-----|
| **平均 Episode 长度** | 13.6 步 |
| **最短 Episode** | 9 步 |
| **最长 Episode** | 17 步 |
| **平均 Episode 奖励** | 20.16 |
| **最低奖励** | 14.45 |
| **最高奖励** | 24.08 |

**注意**: 随机动作下机器人很快跌倒是正常的，这是一个困难的控制任务。

---

## 4. 观测空间详解

### 4.1 15 维观测向量

| 索引 | 含义 | 说明 |
|------|------|------|
| 0 | z - initial_z | 机器人高度变化 |
| 1 | sin(angle_to_target) | 到目标角度的正弦值 |
| 2 | cos(angle_to_target) | 到目标角度的余弦值 |
| 3 | 0.3 × vx | x 方向速度（缩放） |
| 4 | 0.3 × vy | y 方向速度（缩放） |
| 5 | 0.3 × vz | z 方向速度（缩放） |
| 6 | roll | 横滚角（绕 x 轴） |
| 7 | pitch | 俯仰角（绕 y 轴） |
| 8 | joint1_pos | 关节 1 位置 |
| 9 | joint1_vel | 关节 1 速度 |
| 10 | joint2_pos | 关节 2 位置 |
| 11 | joint2_vel | 关节 2 速度 |
| 12 | joint3_pos | 关节 3 位置 |
| 13 | joint3_vel | 关节 3 速度 |
| 14 | foot_contact | 足部接触状态 (0.0/1.0) |

### 4.2 初始观测示例

```
[ 0] z变化            :   0.0000
[ 1] sin(angle)     :   0.0000
[ 2] cos(angle)     :   1.0000
[ 3] vx             :   0.0000
[ 4] vy             :   0.0000
[ 5] vz             :   0.0000
[ 6] roll           :   0.0000
[ 7] pitch          :  -0.0000
[ 8] j1_pos         :   1.0419
[ 9] j1_vel         :   0.0000
[10] j2_pos         :   0.9907
[11] j2_vel         :   0.0000
[12] j3_pos         :   0.0913
[13] j3_vel         :   0.0000
[14] foot_contact   :   0.0000
```

---

## 5. 动作空间详解

### 5.1 3 维动作向量

每个动作值的范围是 `[-1.0, 1.0]`，对应 Hopper 机器人的 3 个关节力矩控制。

动作被归一化并通过以下方式应用：

```python
def apply_action(self, a):
    for n, j in enumerate(self.ordered_joints):
        j.set_motor_torque(
            self.power * j.power_coef * float(np.clip(a[n], -1, +1))
        )
```

其中 `power = 0.75` (Hopper 的电机功率系数)

---

## 6. 奖励机制详解

### 6.1 奖励组成

奖励由 **5 个部分** 组成（见 `gym_locomotion_envs.py:76-136`）：

```python
reward = alive_bonus + progress + electricity_cost + joints_at_limit_cost + feet_collision_cost
```

### 6.2 各部分说明

| 组成部分 | 计算公式 | 典型值 |
|----------|----------|--------|
| **alive_bonus** | `+1` if `z > 0.8 and |pitch| < 1.0` else `-1` | ±1.0 |
| **progress** | `potential_new - potential_old` (距离目标的进度) | -2.0 ~ +4.0 |
| **electricity_cost** | `-2.0 × mean(|a × joint_speeds|) - 0.1 × mean(a²)` | -0.1 ~ -0.8 |
| **joints_at_limit_cost** | `-0.1 × joints_at_limit_count` | -0.1 ~ 0.0 |
| **feet_collision_cost** | `-1.0 × collision_count` (未使用) | 0.0 |

### 6.3 奖励示例

```
步骤 1 - 总奖励: 1.0733
  - alive: 1.0000
  - progress: 0.3733
  - electricity: -0.2000
  - joints_limit: -0.1000
  - feet_collision: 0.0000

步骤 2 - 总奖励: 2.4298
  - alive: 1.0000
  - progress: 1.7195
  - electricity: -0.1897
  - joints_limit: -0.1000
  - feet_collision: 0.0000
```

---

## 7. Episode 终止条件

### 7.1 Terminated (机器人跌倒)

```python
def alive_bonus(self, z, pitch):
    return +1 if z > 0.8 and abs(pitch) < 1.0 else -1

def _isDone(self):
    return self._alive < 0  # 当 alive_bonus 返回 -1 时
```

**条件**:
- `z ≤ 0.8` (高度太低，跌倒)
- `|pitch| ≥ 1.0` (俯仰角太大，倾倒)
- `not np.isfinite(state).all()` (状态异常)

### 7.2 Truncated (超时)

**条件**:
- 达到最大步数 1000 步

---

## 8. 物理模拟参数

### 8.1 PyBullet 设置

来自 `SinglePlayerStadiumScene` (scene_stadium.py):

```python
gravity = 9.8             # m/s²
timestep = 0.0165 / 4     # ≈ 0.004125 秒
frame_skip = 4            # 每个 env.step() 执行 4 个物理步
```

**有效控制频率**: `1 / (timestep × frame_skip) = 1 / 0.0165 ≈ 60 Hz`

### 8.2 场景

- **地面**: `plane_stadium.sdf` (来自 pybullet_data)
- **机器人模型**: `hopper.xml` (MJCF 格式，来自 pybullet_data)

---

## 9. 使用示例

### 9.1 基本使用

```python
import gymnasium as gym
import pybullet_envs_gymnasium

# 创建环境
env = gym.make("HopperBulletEnv-v0")

# 重置环境
obs, info = env.reset(seed=42)

# 运行 episode
for step in range(1000):
    action = env.action_space.sample()  # 随机动作
    obs, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        obs, info = env.reset()

env.close()
```

### 9.2 使用渲染

```python
# 创建带渲染的环境
env = gym.make("HopperBulletEnv-v0", render_mode="human")

obs, info = env.reset()

for step in range(1000):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        break

env.close()
```

### 9.3 与强化学习框架集成

```python
from stable_baselines3 import PPO

# 创建环境
env = gym.make("HopperBulletEnv-v0")

# 训练 PPO 智能体
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=1_000_000)

# 评估
obs, info = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        break
```

---

## 10. 已知特性与注意事项

### 10.1 正常行为

✅ **随机动作下机器人很快跌倒** - 这是正常的
- Hopper 是一个困难的控制任务
- 需要训练良好的策略才能保持平衡
- 平均随机 episode 长度约 10-20 步

✅ **零动作下能维持约 45 步** - 这是正常的
- 机器人初始姿态相对平衡
- 重力作用下会逐渐失衡
- 无控制输入最终会跌倒

### 10.2 环境检查器警告

以下警告是预期的，不影响使用：

```
WARN: A Box observation space minimum value is -infinity. This is probably too low.
WARN: A Box observation space maximum value is infinity. This is probably too high.
```

**原因**: 观测空间某些维度（速度、角度等）理论上无界，这在物理模拟环境中是正常的。

### 10.3 达到奖励阈值

- **奖励阈值**: 2500.0
- **随机策略奖励**: 约 20
- **需要**: 使用强化学习算法训练（PPO、TD3、SAC 等）

---

## 11. 测试命令

### 11.1 快速测试

```bash
python test_hopper.py
```

### 11.2 详细诊断

```bash
python diagnose_hopper.py
```

### 11.3 运行项目测试套件

```bash
pytest tests/test_envs.py -k HopperBulletEnv
```

---

## 12. 依赖版本

```
pybullet >= 3.2.5
gymnasium >= 0.29.1, < 2.0
numpy >= 1.21.0
```

**实际测试版本**:
- pybullet: 3.2.7
- gymnasium: 1.2.2
- numpy: 2.3.4

---

## 13. 结论

### ✅ 环境完全可用

HopperBulletEnv-v0 是一个 **功能完整、实现正确、符合标准** 的 Gymnasium 环境，可以安全用于：

1. ✅ 强化学习算法研究
2. ✅ 机器人控制实验
3. ✅ 教学与演示
4. ✅ 基准测试

### 下一步建议

如果要使用此环境进行强化学习训练：

1. 使用成熟的 RL 库（Stable Baselines3、CleanRL、RLlib 等）
2. 推荐算法：PPO、TD3、SAC
3. 预期训练时间：在普通 GPU 上约 1-2 小时
4. 预期性能：训练良好的智能体应该能达到 2000+ 奖励

---

**报告生成时间**: 2025-11-16
**检查工具**: test_hopper.py, diagnose_hopper.py
**环境版本**: pybullet_envs_gymnasium 0.6.0

# 双齿轮最小验证模块

从 BrickGPT 目录运行（无第三方运行依赖）：

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m brickgpt.gear_pair examples/gears/valid.json --input-deg 360
.\.venv\Scripts\python.exe -m brickgpt.gear_pair examples/gears/wrong_distance.json
.\.venv\Scripts\python.exe -m pytest tests/test_gear_pair.py -q -p no:cacheprovider
```

正确案例：模数 1 mm、20/40 齿，中心距 30 mm，主动轮增加 360°，
从动轮增加 -180°。错误案例中心距为 35 mm，输出
`center_distance_mismatch`，退出码为 1。通过退出码为 0。
无效输入直接报错，不转换为装配失败。

输入 `gears` 必须包含两个齿轮，每个齿轮包括：

- `teeth`：齿数。
- `module_mm`：模数。
- `pressure_angle_deg`：压力角。
- `width_mm`：齿宽。
- `center_mm`：齿轮中心 `[x, y, z]`，单位毫米，z 为齿宽中点。
- `joint`：`revolute_z` 表示相对固定支架绕 Z 轴转动；`fixed` 表示锁死。

范围：标准、无变位、外啮合直齿轮；两轴均沿 Z 方向且位置固定。
检查模数和压力角匹配、标准中心距、正的轴向重叠和转动自由度。
中心距容差 1e-6 mm 仅处理浮点误差，不代表制造公差。
角度输出为转角增量，不是绝对装配角度。

`ideal_pair_compatible` 只表示这些理想条件通过。
初始齿相位假定已正确对齐；不检查真实齿形、根切、重合度、轴孔配合、
支架强度、周围物体干涉、摩擦或真实接触传动。
因此本模块是参数级筛查，不能作为实物可传动的完整证明。
示例是人工构造的解析基准，不是实测数据或 LEGO 零件标定结果。
下一步应加入具有真实尺寸的零件和齿面/障碍物几何验证。

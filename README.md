# BrickGPT 双齿轮验证增量

本仓库仅保存基于 [BrickGPT](https://github.com/AvaLovelace1/BrickGPT) 新增的机械验证代码，不包含上游源码、上游提交历史、模型、缓存和渲染输出。对应本地上游基线为 `da01aab`。

## 最近更新：2026-10-21

- 新增参数级双齿轮验证：模数、压力角、标准中心距、轴向重叠和转动连接。
- 新增理想传动比和转角增量计算。
- 新增正确装配、错误中心距示例以及 15 项自动测试。
- 20/40 齿案例输入 360°，输出 -180°；错误中心距被拒绝。

当前范围为固定平行 Z 轴上的标准无变位外啮合直齿轮。初始齿相位假定正确，不检查真实齿面、根切、重合度、支架干涉和实物传动，不包含摩擦或完整动力学。

## 独立运行（PowerShell）

Python 3.10 或更高版本，无第三方运行依赖。

```powershell
$env:PYTHONPATH = 'src'
python -m brickgpt.gear_pair examples/gears/valid.json --input-deg 360
python -m brickgpt.gear_pair examples/gears/wrong_distance.json
```

第二个命令预期返回退出码 1，表示正确识别到不兼容装配。

## 测试

在有 pytest 的 Python 环境下运行：

```powershell
$env:PYTHONPATH = 'src'
python -m pytest tests/test_gear_pair.py -q -p no:cacheprovider
```

预期 `15 passed`。输入字段详见 [示例说明](examples/gears/README.md)。示例说明中的 `.venv` 命令适用于已有虚拟环境；本仓库不上传虚拟环境。

## 合回 BrickGPT

将本仓库 `src/brickgpt/gear_pair.py`、`tests/test_gear_pair.py` 和 `examples/gears/` 复制到 BrickGPT 对应目录即可。没有修改原有生成流程。

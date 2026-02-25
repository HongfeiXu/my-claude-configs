---
name: windows-toast-notification
description: 为 Claude Code 配置 Windows Toast 通知。当用户要求配置系统通知、任务完成提醒、hooks 通知时使用此 skill。使用 SnoreToast（GUI 程序）实现零窗口闪烁。
disable-model-invocation: true
allowed-tools: Bash(npm *), Bash(pwsh *), Bash(find *), Read, Edit, Write
argument-hint: "[setup|test|uninstall]"
---

# Windows Toast 通知配置

为 Claude Code CLI 配置 Windows 系统 Toast 通知，在任务完成、等待输入、需要权限确认时自动弹出提醒。

## 参数模式

| 参数 | 执行范围 | 说明 |
|------|---------|------|
| `setup` (默认) | 步骤 1 + 2 + 3 | 完整安装配置流程 |
| `test` | 仅步骤 3 | 测试已安装的 SnoreToast 是否正常工作 |
| `uninstall` | 卸载章节 | 移除 hooks 配置并可选卸载 node-notifier |

## 前置条件

- Windows 10/11
- Node.js + npm
- Claude Code CLI

## 执行步骤

### 1. 安装 SnoreToast

通过 node-notifier 获取（内含预编译的 SnoreToast.exe）：

```bash
npm install -g node-notifier
```

### 2. 探测 SnoreToast 路径

如果通过方式 A 安装，使用以下命令查找实际路径：

```bash
find "$(npm root -g)" -name "snoretoast-x64.exe" 2>/dev/null
```

备用（PowerShell）：
```powershell
Get-ChildItem -Recurse -Filter "snoretoast-x64.exe" (npm root -g) | Select-Object -ExpandProperty FullName
```

典型路径：
```
C:\Users\<用户名>\AppData\Roaming\npm\node_modules\node-notifier\vendor\snoreToast\snoretoast-x64.exe
```

### 3. 配置 Hooks

编辑 `~/.claude/settings.json`，在 `hooks` 字段中添加以下条目（保留已有的其他 hooks 配置）：

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "\"<SNORETOAST_PATH>\" -t \"Claude Code\" -m \"⏸️ 等待输入\" -silent || exit 0"
          }
        ]
      },
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "\"<SNORETOAST_PATH>\" -t \"Claude Code\" -m \"🔐 需要权限确认\" -silent || exit 0"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"<SNORETOAST_PATH>\" -t \"Claude Code\" -m \"✅ 任务完成\" -silent || exit 0"
          }
        ]
      }
    ]
  }
}
```

> 将 `<SNORETOAST_PATH>` 替换为第 2 步获取的实际路径（注意 JSON 中反斜杠需要转义为 `\\`）。

### 4. 验证

直接在终端运行 SnoreToast 测试：

```bash
"<SNORETOAST_PATH>" -t "Claude Code" -m "配置成功" -silent
```

右下角弹出通知且无窗口闪烁即为成功。**重启 Claude Code 会话**使 hooks 生效。

## Hook 事件说明

| Hook 事件 | Matcher | 触发时机 | 通知内容 |
|-----------|---------|---------|---------|
| `Stop` | — | 任务结束/停止 | ✅ 任务完成 |
| `Notification` | `idle_prompt` | 等待用户输入超 60 秒 | ⏸️ 等待输入 |
| `Notification` | `permission_prompt` | 需要用户批准权限 | 🔐 需要权限确认 |

## 自定义选项

- **启用提示音**：去掉 `-silent` 参数
- **自定义文案**：修改 `-m` 参数内容
- **添加图标**：增加 `-p "C:\path\to\icon.png"` 参数

## 卸载

1. 从 `settings.json` 的 `hooks` 中删除包含 SnoreToast 命令的条目（`Notification` 和 `Stop` 中的相关项）。如果 hooks 中没有其他配置了，可以整个删除 `hooks` 字段
2. `npm uninstall -g node-notifier`（可选）

## 技术说明

- 在 Windows 上，Claude Code hooks 通过 bash（Git Bash/MSYS2）执行命令。bash 启动控制台子系统程序（pwsh、node、cmd）时会短暂弹出命令行窗口。SnoreToast 是 Windows GUI 子系统程序（PE 头标记 WINDOWS_GUI），不创建控制台窗口，彻底解决闪烁问题。
- SnoreToast 在通知被用户关闭、超时消失等情况下会返回非零退出码，Claude Code 的 hook 系统会将其视为错误并输出警告。命令末尾的 `|| exit 0` 确保无论 SnoreToast 返回什么退出码，hook 都视为成功。

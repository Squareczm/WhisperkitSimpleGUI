# WhisperKit GUI

这是一个为 [WhisperKit](https://github.com/argmaxinc/WhisperKit) 项目开发的图形用户界面（GUI），使用 Python 和 Tkinter 构建。它提供了一个简洁直观的桌面应用，让用户可以轻松地使用 WhisperKit 的语音转文字功能。

## 功能特性

- **文件选择**: 方便地从您的电脑中选择音频文件（支持 `.wav`, `.mp3`, `.m4a`, `.flac` 格式）。
- **一键转录**: 点击按钮即可开始转录，界面会实时显示状态。
- **结果展示**: 在文本框中清晰地展示转录后的文字结果。
- **文本导出**: 轻松将转录内容导出为 `.txt` 文件，方便后续编辑和存档。

## 运行截图

![GUI Screenshot](https://private-user-images.githubusercontent.com/177656913/356543946-81413a69-a111-4f1b-a534-19069a531f82.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjA2ODkxMzEsIm5iZiI6MTcyMDY4ODgzMSwicGF0aCI6Ii8xNzc2NTY5MTMvMzU2NTQzOTQ2LTgxNDEzYTY5LWExMTEtNGYxYi1hNTM0LTE5MDY5YTUzMWY4Mi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYiLCJYLUFtei1DcmVkZW50aWFsPUFLSUFWQ0E5REtHSEI3NjJCQ1QyJTJGMjAyNDA3MTElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCIsIlgtQW16LURhdGU9MjAyNDA3MTFUMTEyMDMxWiIsIlgtQW16LUV4cGlyZXM9MzAwIiwiWC1BbXotU2lnbmF0dXJlPWVmNTAyNjE3YzM3ZWEzOWU5YjI3ZDIyMmM3ZTBlMDQ3NjQxNzk5ZmFjZDgxYmM3ZDBkODJkZTRiYzM3NjgyOTgiLCJYLUFtei1TdWJqZWN0IjoiIiwidG9rZW4iOiIiLCJ2ZXJzaW9uIjoidjIifQ.M7GfC9tW8G89fP87l5h5t1t6cKMMx1T063i-o4mD_5U)

## 环境要求

1.  **macOS**: 此 GUI 通过调用 WhisperKit 的 Swift CLI 工作，因此需要在 macOS 环境下运行。
2.  **Xcode Command Line Tools**: 请确保已安装 Xcode 及其命令行工具。
3.  **WhisperKit 项目**:
    - 您需要先克隆 [WhisperKit 的主仓库](https.github.com/argmaxinc/WhisperKit)。
    - 根据 WhisperKit 的指引完成环境设置 (`make setup`)。
4.  **WhisperKit 模型**:
    - 此 GUI 默认使用 `medium` 模型。
    - 请在 WhisperKit 项目的根目录运行以下命令来下载所需模型：
      ```bash
      make download-model MODEL=medium
      ```
    - 如果您想使用其他模型，请修改 `WhisperKit-GUI/transcriber.py` 文件中的 `model_name` 默认值。

## 如何使用

1.  **启动应用**:
    - 打开您的终端 (Terminal)。
    - `cd` 到 `WhisperKit` 项目的根目录。
    - 运行以下命令来启动 GUI 程序：
      ```bash
      python3 WhisperKit-GUI/app.py
      ```

2.  **操作步骤**:
    - **选择音频文件**: 点击 "选择音频文件" 按钮，然后从弹出的窗口中选择您想要转录的音频。
    - **开始转录**: 选择文件后，"开始转录" 按钮会变为可用。点击它，程序将开始处理音频。请耐心等待，初次运行模型加载可能会花费一些时间。
    - **查看与导出**: 转录完成后，文本会显示在下方的文本框中。此时，"导出文本" 按钮会变为可用。点击它可以将结果保存为 `.txt` 文件。

## 工作原理

本 GUI 程序通过 Python 的 `subprocess` 模块，在后台调用 WhisperKit 项目自带的 Swift 命令行工具 (`whisperkit-cli`) 来执行实际的转录任务。GUI 程序负责构建命令、传递参数（如模型路径和音频文件路径）、捕获输出，并将其美观地呈现在用户面前。 
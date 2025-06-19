import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import subprocess
import os
from datetime import datetime
from transcriber import transcribe_audio

class WhisperKitGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Whisper语音转文字")
        self.geometry("450x600")
        self.configure(bg="#f0f2f5")

        self.selected_audio_path = None

        # Main frame
        main_frame = tk.Frame(self, bg="#f0f2f5", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # --- Widgets ---

        # Title Label
        title_label = tk.Label(main_frame, text="Whisper语音转文字", font=("Arial", 24, "bold"), bg="#f0f2f5")
        title_label.pack(pady=(0, 20))

        # Select File Button
        select_button = tk.Button(main_frame, text="选择音频文件", font=("Arial", 14), bg="#6a5acd", fg="white", command=self.select_file, relief="flat", padx=20, pady=10)
        select_button.pack(fill="x", pady=5)

        # Selected File Label
        self.selected_file_label = tk.Label(main_frame, text="已选择: 未选择文件", font=("Arial", 12), bg="#e0e0e0", wraplength=400)
        self.selected_file_label.pack(fill="x", pady=10, ipady=10)

        # Transcribe Button
        self.transcribe_button = tk.Button(main_frame, text="开始转录", font=("Arial", 14), bg="#dcdcdc", fg="#808080", command=self.start_transcription_thread, state="disabled", relief="flat", padx=20, pady=10)
        self.transcribe_button.pack(fill="x", pady=5)

        # Status Label
        self.status_label = tk.Label(main_frame, text="", font=("Arial", 12, "italic"), bg="#f0f2f5")
        self.status_label.pack(pady=5)

        # Result Text Area
        self.result_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=("Arial", 12), borderwidth=1, relief="solid", state="disabled")
        self.result_text.pack(expand=True, fill="both", pady=10)

        # Export Button
        self.export_button = tk.Button(main_frame, text="导出文本", font=("Arial", 14), bg="#d3d3d3", fg="#a9a9a9", command=self.export_text, state="disabled", relief="flat", padx=20, pady=10)
        self.export_button.pack(fill="x", pady=5)

    def select_file(self):
        """Opens a file dialog to select an audio file."""
        filepath = filedialog.askopenfilename(
            title="选择音频文件",
            filetypes=(("Audio Files", "*.wav *.mp3 *.m4a *.flac"), ("All files", "*.*"))
        )
        if filepath:
            self.selected_audio_path = filepath
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath) / (1024 * 1024)  # in MB
            self.selected_file_label.config(text=f"已选择: {filename} ({filesize:.1f} MB)")
            self.transcribe_button.config(state="normal", bg="#a9a9a9", fg="#ffffff")
            self.status_label.config(text="")
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.config(state="disabled")
            self.export_button.config(state="disabled", bg="#d3d3d3", fg="#a9a9a9")


    def start_transcription_thread(self):
        """Starts the transcription in a new thread to avoid freezing the GUI."""
        if not self.selected_audio_path:
            messagebox.showerror("错误", "请先选择一个音频文件!")
            return

        self.transcribe_button.config(state="disabled", bg="#dcdcdc", fg="#808080")
        self.status_label.config(text="正在转录中，请稍候...")
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "正在初始化模型，这可能需要一些时间，请稍等...")
        self.result_text.config(state="disabled")

        # Run transcription in a separate thread
        thread = threading.Thread(target=self.run_transcription)
        thread.daemon = True
        thread.start()

    def run_transcription(self):
        """The actual transcription process."""
        transcription, error = transcribe_audio(self.selected_audio_path, progress_callback=self.update_progress)

        if error:
            self.update_gui_with_result(f"转录失败:\\n\\n{error}", is_error=True)
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            final_text = f"[{timestamp}]\\n{transcription}"
            self.update_gui_with_result(final_text)

    def update_progress(self, message):
        """Callback to update the GUI with progress."""
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.config(state="disabled")


    def update_gui_with_result(self, text, is_error=False):
        """Updates the GUI with the transcription result."""
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

        if is_error:
            self.status_label.config(text="转录出错!")
            self.export_button.config(state="disabled", bg="#d3d3d3", fg="#a9a9a9")
        else:
            self.status_label.config(text="转录完成!")
            self.export_button.config(state="normal", bg="#6a5acd", fg="white")

        self.transcribe_button.config(state="normal", bg="#a9a9a9", fg="#ffffff") # Re-enable for another run

    def export_text(self):
        """Exports the content of the result text area to a .txt file."""
        content = self.result_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "没有内容可以导出。")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Documents", "*.txt")],
            title="导出为文本文档"
        )
        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("成功", f"文件已成功保存到:\n{save_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件失败: {e}")


if __name__ == "__main__":
    app = WhisperKitGUI()
    app.mainloop() 
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QApplication, QListWidget
import sys
import os
import json
from multiprocessing import Queue, Process, set_start_method
from src.bot import bot_process  # Import bot process function

# Ensure the multiprocessing context is explicitly set to 'spawn'
set_start_method('spawn', force=True)

UPLOAD_LOG = "uploaded_files.json"
DOWNLOAD_FOLDER = "downloads"

def load_uploaded_files():
    """Load uploaded files from JSON log."""
    if not os.path.exists(UPLOAD_LOG):
        return []
    with open(UPLOAD_LOG, 'r') as f:
        return json.load(f)

class BotWorker(QThread):
    result_received = pyqtSignal(str)

    def __init__(self, task_queue_instance, result_queue_instance):
        super().__init__()
        self.task_queue = task_queue_instance
        self.result_queue = result_queue_instance

    def run(self):
        while True:
            if not self.result_queue.empty():
                result = self.result_queue.get()
                self.result_received.emit(result)

    def upload_file(self, file_path):
        self.task_queue.put({"file_path": file_path})

    def list_files(self):
        self.task_queue.put({"list_files": True})

    def download_files(self, selected_indexes):
        self.task_queue.put({"download_files": selected_indexes})

class MainWindow(QMainWindow):
    def __init__(self, task_queue_instance, result_queue_instance):
        super().__init__()
        self.setWindowTitle("Discord File Uploader")
        self.setGeometry(100, 100, 600, 400)

        self.label = QLabel("Select a file to upload to Discord.")
        self.file_path = None

        self.select_button = QPushButton("Select File")
        self.select_button.clicked.connect(self.select_file)

        self.upload_button = QPushButton("Upload File")
        self.upload_button.setEnabled(False)
        self.upload_button.clicked.connect(self.upload_file)

        self.list_button = QPushButton("List Uploaded Files")
        self.list_button.clicked.connect(self.list_files)

        self.download_button = QPushButton("Download Selected Files")
        self.download_button.clicked.connect(self.download_files)

        self.file_list_widget = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.list_button)
        layout.addWidget(self.file_list_widget)
        layout.addWidget(self.download_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.worker = BotWorker(task_queue_instance, result_queue_instance)
        self.worker.result_received.connect(self.update_label)
        self.worker.start()

        # Load and display previously uploaded files
        self.show_uploaded_files()

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file:
            self.file_path = file
            self.label.setText(f"Selected: {file}")
            self.upload_button.setEnabled(True)
        else:
            self.label.setText("No file selected.")

    def upload_file(self):
        if self.file_path:
            self.label.setText(f"Uploading {self.file_path}...")
            self.worker.upload_file(self.file_path)

    def list_files(self):
        files = load_uploaded_files()
        self.file_list_widget.clear()
        if not files:
            self.label.setText("No files uploaded yet.")
        else:
            for file in files:
                metadata = f"Parts: {file['total_parts']}" if file.get("is_part") else "Single file"
                self.file_list_widget.addItem(f"{file['name']} - {file['url']} ({metadata})")

    def download_files(self):
        files = load_uploaded_files()
        if not files:
            self.label.setText("No files available to download.")
            return

        # Get selected files
        selected_items = self.file_list_widget.selectedItems()
        selected_indexes = [self.file_list_widget.row(item) for item in selected_items]
        if selected_indexes:
            self.worker.download_files(selected_indexes)
            self.label.setText("Downloading selected files...")
        else:
            self.label.setText("No files selected for download.")

    def update_label(self, message):
        self.label.setText(message)

    def show_uploaded_files(self):
        """Load previously uploaded files into the list widget."""
        files = load_uploaded_files()
        self.file_list_widget.clear()
        if files:
            for file in files:
                metadata = f"Parts: {file['total_parts']}" if file.get("is_part") else "Single file"
                self.file_list_widget.addItem(f"{file['name']} - {file['url']} ({metadata})")

if __name__ == "__main__":
    task_queue = Queue()
    result_queue = Queue()

    bot_proc = Process(target=bot_process, args=(task_queue, result_queue))
    bot_proc.start()

    app = QApplication(sys.argv)
    window = MainWindow(task_queue, result_queue)
    window.show()

    try:
        sys.exit(app.exec_())
    finally:
        task_queue.put("STOP")
        bot_proc.join()

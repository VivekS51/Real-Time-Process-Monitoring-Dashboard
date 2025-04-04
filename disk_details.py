# import psutil
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
# from PyQt5.QtCore import QTimer
# import pyqtgraph as pg
# import time

# class DiskMonitorWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         layout = QVBoxLayout(self)

#         # Disk Read & Write Graph
#         self.disk_plot = pg.PlotWidget(title="Disk Read/Write Speed (MB/s)")
#         self.disk_plot.showGrid(x=True, y=True)
#         self.read_curve = self.disk_plot.plot(pen='y', name="Read Speed")
#         self.write_curve = self.disk_plot.plot(pen='r', name="Write Speed")
#         layout.addWidget(self.disk_plot)

#         # Disk Details Label
#         self.details_label = QLabel()
#         layout.addWidget(self.details_label)

#         self.read_data = [0] * 60
#         self.write_data = [0] * 60

#         self.prev_disk = psutil.disk_io_counters()
#         self.prev_time = time.time()

#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_stats)
#         self.timer.start(1000)

#     def update_stats(self):
#         curr_disk = psutil.disk_io_counters()
#         interval = time.time() - self.prev_time

#         read_speed = (curr_disk.read_bytes - self.prev_disk.read_bytes) / interval / (1024 * 1024) if interval > 0 else 0
#         write_speed = (curr_disk.write_bytes - self.prev_disk.write_bytes) / interval / (1024 * 1024) if interval > 0 else 0

#         self.prev_disk = curr_disk
#         self.prev_time = time.time()

#         self.read_data = self.read_data[1:] + [read_speed]
#         self.write_data = self.write_data[1:] + [write_speed]

#         self.read_curve.setData(self.read_data)
#         self.write_curve.setData(self.write_data)

#         details = (
#             f"<b>Read Speed:</b> {read_speed:.2f} MB/s<br>"
#             f"<b>Write Speed:</b> {write_speed:.2f} MB/s"
#         )
#         self.details_label.setText(details)

import psutil
import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
import pyqtgraph as pg

class DiskMonitorThread(QThread):
    update_signal = pyqtSignal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True
        self.prev_disk = psutil.disk_io_counters()
        self.prev_time = time.time()

    def run(self):
        while self.running:
            curr_disk = psutil.disk_io_counters()
            interval = time.time() - self.prev_time

            read_speed = (curr_disk.read_bytes - self.prev_disk.read_bytes) / interval / (1024 * 1024) if interval > 0 else 0
            write_speed = (curr_disk.write_bytes - self.prev_disk.write_bytes) / interval / (1024 * 1024) if interval > 0 else 0

            self.prev_disk = curr_disk
            self.prev_time = time.time()

            self.update_signal.emit(read_speed, write_speed)
            self.msleep(1000)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
        self.deleteLater()

class DiskMonitorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.disk_plot = pg.PlotWidget(title="Disk Read/Write Speed (MB/s)")
        self.disk_plot.showGrid(x=True, y=True)
        self.read_curve = self.disk_plot.plot(pen='y', name="Read Speed")
        self.write_curve = self.disk_plot.plot(pen='r', name="Write Speed")
        layout.addWidget(self.disk_plot)

        self.details_label = QLabel()
        layout.addWidget(self.details_label)

        self.read_data = [0] * 60
        self.write_data = [0] * 60

        self.monitor_thread = DiskMonitorThread()
        self.monitor_thread.update_signal.connect(self.update_stats)
        self.monitor_thread.start()

    def update_stats(self, read_speed, write_speed):
        self.read_data = self.read_data[1:] + [read_speed]
        self.write_data = self.write_data[1:] + [write_speed]

        self.read_curve.setData(self.read_data)
        self.write_curve.setData(self.write_data)

        details = (
            f"<b>Read Speed:</b> {read_speed:.2f} MB/s<br>"
            f"<b>Write Speed:</b> {write_speed:.2f} MB/s"
        )
        self.details_label.setText(details)

    def closeEvent(self, event):
        self.monitor_thread.stop()
        self.monitor_thread.quit()
        self.monitor_thread.wait()
        self.monitor_thread.deleteLater()
        event.accept()

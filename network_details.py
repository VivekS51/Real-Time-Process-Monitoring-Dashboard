# import psutil
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
# from PyQt5.QtCore import QTimer
# import pyqtgraph as pg
# import time

# class NetworkMonitorWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         layout = QVBoxLayout(self)

#         # Upload & Download Graph
#         self.net_plot = pg.PlotWidget(title="Network Speed (Kb/s)")
#         self.net_plot.showGrid(x=True, y=True)
#         self.upload_curve = self.net_plot.plot(pen='g', name="Upload")
#         self.download_curve = self.net_plot.plot(pen='m', name="Download")
#         layout.addWidget(self.net_plot)

#         # Network Details Label
#         self.details_label = QLabel()
#         layout.addWidget(self.details_label)

#         self.upload_data = [0] * 60
#         self.download_data = [0] * 60

#         self.prev_net = psutil.net_io_counters()
#         self.prev_time = time.time()

#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_stats)
#         self.timer.start(1000)

#     def update_stats(self):
#         curr_net = psutil.net_io_counters()
#         interval = time.time() - self.prev_time

#         upload = (curr_net.bytes_sent - self.prev_net.bytes_sent) / interval / 1024 * 8 if interval > 0 else 0
#         download = (curr_net.bytes_recv - self.prev_net.bytes_recv) / interval / 1024 * 8 if interval > 0 else 0

#         self.prev_net = curr_net
#         self.prev_time = time.time()

#         self.upload_data = self.upload_data[1:] + [upload]
#         self.download_data = self.download_data[1:] + [download]

#         self.upload_curve.setData(self.upload_data)
#         self.download_curve.setData(self.download_data)

#         details = (
#             f"<b>Upload Speed:</b> {upload:.2f} Kb/s<br>"
#             f"<b>Download Speed:</b> {download:.2f} Kb/s"
#         )
#         self.details_label.setText(details)

import psutil
import time
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
import pyqtgraph as pg

class NetworkWorker(QObject):
    data_ready = pyqtSignal(float, float)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = True
        self.prev_net = psutil.net_io_counters()
        self.prev_time = time.time()

    def run(self):
        while self.running:
            curr_net = psutil.net_io_counters()
            interval = time.time() - self.prev_time

            upload = (curr_net.bytes_sent - self.prev_net.bytes_sent) / interval / 1024 * 8 if interval > 0 else 0
            download = (curr_net.bytes_recv - self.prev_net.bytes_recv) / interval / 1024 * 8 if interval > 0 else 0

            self.prev_net = curr_net
            self.prev_time = time.time()

            self.data_ready.emit(upload, download)
            time.sleep(1)

        self.finished.emit()

class NetworkMonitorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.net_plot = pg.PlotWidget(title="Network Speed (Kb/s)")
        self.net_plot.showGrid(x=True, y=True)
        self.upload_curve = self.net_plot.plot(pen='g', name="Upload")
        self.download_curve = self.net_plot.plot(pen='m', name="Download")
        layout.addWidget(self.net_plot)

        self.details_label = QLabel()
        layout.addWidget(self.details_label)

        self.upload_data = [0] * 60
        self.download_data = [0] * 60

        self.thread = QThread()
        self.worker = NetworkWorker()
        self.worker.moveToThread(self.thread)

        self.worker.data_ready.connect(self.update_display)
        self.thread.started.connect(self.worker.run)

        self.thread.start()

    def update_display(self, upload, download):
        self.upload_data = self.upload_data[1:] + [upload]
        self.download_data = self.download_data[1:] + [download]

        self.upload_curve.setData(self.upload_data)
        self.download_curve.setData(self.download_data)

        details = (
            f"<b>Upload Speed:</b> {upload:.2f} Kb/s<br>"
            f"<b>Download Speed:</b> {download:.2f} Kb/s"
        )
        self.details_label.setText(details)

    def closeEvent(self, event):
        self.worker.running = False
        self.thread.quit()
        self.thread.wait()
        self.worker.deleteLater()
        super().closeEvent(event)

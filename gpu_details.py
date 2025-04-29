import GPUtil
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
import pyqtgraph as pg
import time

class GPUWorker(QThread):
    gpu_data_updated = pyqtSignal(float, float, dict)

    def run(self):
        self.running = True
        while self.running:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                load = gpu.load * 100
                mem_percent = (gpu.memoryUsed / gpu.memoryTotal) * 100

                details = {
                    "name": gpu.name,
                    "temp": gpu.temperature,
                    "load": load,
                    "mem_used": gpu.memoryUsed,
                    "mem_total": gpu.memoryTotal,
                    "driver": gpu.driver,
                }
                self.gpu_data_updated.emit(load, mem_percent, details)
            time.sleep(1)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
        self.deleteLater()

class GPUMonitorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.gpu_plot = pg.PlotWidget(title="GPU Load (%)")
        self.gpu_plot.setYRange(0, 100)
        self.gpu_plot.showGrid(x=True, y=True)
        self.gpu_curve = self.gpu_plot.plot(pen='m')
        layout.addWidget(self.gpu_plot)

        self.gpu_mem_plot = pg.PlotWidget(title="GPU Memory Usage (%)")
        self.gpu_mem_plot.setYRange(0, 100)
        self.gpu_mem_plot.showGrid(x=True, y=True)
        self.gpu_mem_curve = self.gpu_mem_plot.plot(pen='c')
        layout.addWidget(self.gpu_mem_plot)

        self.details_label = QLabel()
        layout.addWidget(self.details_label)

        self.gpu_usage_data = [0] * 60
        self.gpu_mem_data = [0] * 60

        self.worker = GPUWorker()
        self.worker.gpu_data_updated.connect(self.update_graph_and_info)
        self.worker.start()

    def update_graph_and_info(self, load, mem_percent, details):
        self.gpu_usage_data = self.gpu_usage_data[1:] + [load]
        self.gpu_mem_data = self.gpu_mem_data[1:] + [mem_percent]

        self.gpu_curve.setData(self.gpu_usage_data)
        self.gpu_mem_curve.setData(self.gpu_mem_data)

        details_str = (
            f"<b>Name:</b> {details['name']}<br>"
            f"<b>Temperature:</b> {details['temp']}°C<br>"
            f"<b>Load:</b> {details['load']:.2f}%<br>"
            f"<b>Memory Used:</b> {details['mem_used']} MB / {details['mem_total']} MB<br>"
            f"<b>Driver:</b> {details['driver']}"
        )
        self.details_label.setText(details_str)

    def closeEvent(self, event):
        self.worker.stop()
        self.worker.quit()
        self.worker.wait()
        self.worker.deleteLater()
        super().closeEvent(event)

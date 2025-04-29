import psutil
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QSizePolicy, QGraphicsRectItem
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import pyqtgraph as pg
import time

class MemoryWorker(QThread):
    data_updated = pyqtSignal(float, dict)
    def __init__(self):
        super().__init__()
        self.total_mem = psutil.virtual_memory().total / (1024 ** 3)
    def run(self):
        while True:
            mem = psutil.virtual_memory()
            details = {
                'total': self.total_mem,
                'available': mem.available / (1024 ** 3),
                'used': mem.used / (1024 ** 3),
                'free': mem.free / (1024 ** 3),
                'percent': mem.percent,
                'cached': getattr(mem,'cached',mem.available/4) / (1024**3),
                'committed': mem.total * mem.percent / 100 / (1024**3)
            }
            self.data_updated.emit(mem.percent, details)
            time.sleep(1)

class MemoryMonitorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mem_usage_data = [0] * 60

        self.worker_thread = MemoryWorker()
        self.worker_thread.data_updated.connect(self.update_display)
        self.worker_thread.start()

        layout = QGridLayout(self)

        top_label = QHBoxLayout()
        self.left_label = QLabel("Memory")
        self.left_label.setStyleSheet("color: white; font-size: 20pt;")
        self.right_label = QLabel(f"{round(self.worker_thread.total_mem):.1f} GB")
        self.right_label.setStyleSheet("color: white; font-size: 12pt;")
        top_label.addWidget(self.left_label, alignment=Qt.AlignLeft)
        top_label.addWidget(self.right_label, alignment=Qt.AlignRight)
        layout.addLayout(top_label, 0, 0, 1, 2)

        # Memory Usage Graph
        self.mem_plot = pg.PlotWidget()
        self.mem_plot.setBackground('#1C1C1C')
        self.mem_plot.getPlotItem().showGrid(x=True, y=True, alpha=0.2)
        self.mem_plot.getPlotItem().hideAxis('bottom')
        self.mem_plot.getPlotItem().hideAxis('left')
        self.mem_plot.setYRange(0, 100)
        self.mem_curve = self.mem_plot.plot(pen=pg.mkPen('#8A2BE2', width=2), fillLevel=0, brush=(138, 43, 226, 80))
        layout.addWidget(self.mem_plot, 1, 0, 1, 2)

        # Memory Composition Bar
        self.composition_plot = pg.PlotWidget()
        self.composition_plot.setBackground('#1C1C1C')
        self.composition_plot.hideAxis('bottom')
        self.composition_plot.hideAxis('left')
        self.composition_plot.setMouseEnabled(x=False, y=False)
        layout.addWidget(self.composition_plot, 2, 0, 1, 2)

        # Details label
        self.details_label = QLabel()
        self.details_label.setStyleSheet("color: #E0E0E0; font-size: 9pt;")
        self.details_label.setWordWrap(True)
        layout.addWidget(self.details_label, 3, 0, 1, 2)

    def update_display(self, percent, details):
        self.mem_usage_data = self.mem_usage_data[1:] + [percent]
        self.mem_curve.setData(self.mem_usage_data)

        self.composition_plot.clear()
        used_ratio = details['used']/details['total']
        cached_ratio = details['cached']/details['total']
        available_ratio = details['available']/details['total']

        self.composition_plot.setYRange(0,1)

        x_start = 0
        bar_height = 1
        used_bar = QGraphicsRectItem(x_start, 0, used_ratio * 10, bar_height)
        used_bar.setBrush(pg.mkBrush('#8A2BE2'))
        self.composition_plot.addItem(used_bar)

        x_start += used_ratio
        cached_bar = QGraphicsRectItem(x_start, 0, cached_ratio * 10, bar_height)
        cached_bar.setBrush(pg.mkBrush('#BA68C8'))
        self.composition_plot.addItem(cached_bar)

        x_start += cached_ratio
        available_bar = QGraphicsRectItem(x_start, 0, available_ratio * 10, bar_height)
        available_bar.setBrush(pg.mkBrush('#E0E0E0'))
        self.composition_plot.addItem(available_bar)

        details_str = (
            f"<b>Total:</b> {details['total']:.2f} GB<br>"
            f"<b>Available:</b> {details['available']:.2f} GB<br>"
            f"<b>Used:</b> {details['used']:.2f} GB<br>"
            f"<b>Cached:</b> {details['cached']:.2f} GB<br>"
            f"<b>Usage Percent:</b> {details['percent']}%"
        )
        self.details_label.setText(details_str)

    def closeEvent(self, event):
        self.worker_thread.terminate()
        self.worker_thread.wait()
        event.accept()

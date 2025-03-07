import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN


class OrderLinesMapper:
    def __init__(self, orderlines, orders_number, coord_columns=('x', 'y', 'z'), eps=5.0, min_samples=2):
        """
        Khởi tạo lớp với các tham số:
        :param orderlines: DataFrame chứa dữ liệu các đơn hàng
        :param orders_number: Số lượng đơn hàng mỗi wave (dùng sau)
        :param coord_columns: Tên các cột chứa tọa độ (ví dụ: 'x', 'y', 'z')
        :param eps: Khoảng cách tối đa giữa các đơn hàng để nhóm lại
        :param min_samples: Số lượng tối thiểu đơn hàng trong một cụm để tạo thành một wave
        """
        self.orderlines = orderlines
        self.orders_number = orders_number
        self.coord_columns = coord_columns
        self.eps = eps
        self.min_samples = min_samples

    def map_orders(self):
        # Lấy tọa độ từ DataFrame
        coords = self.orderlines[list(self.coord_columns)].values

        # Áp dụng DBSCAN để phân nhóm các đơn hàng dựa trên tọa độ 3D
        dbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples, metric='euclidean')
        self.orderlines['WaveID'] = dbscan.fit_predict(coords)

        # Gán WaveID cho những điểm không thuộc bất kỳ cụm nào (outliers)
        # DBSCAN sẽ gán giá trị -1 cho các outlier
        self.orderlines['WaveID'] = self.orderlines['WaveID'].apply(lambda x: x if x != -1 else -1)

        # Đếm số lượng wave
        waves_number = len(np.unique(self.orderlines['WaveID']))

        return self.orderlines, waves_number

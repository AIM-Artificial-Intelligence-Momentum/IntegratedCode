# BasicChart.py
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from APIModule.KopisAPI import KopisAPI

class BasicChart:
    def __init__(self):
        load_dotenv()
        self.kopis_api  = KopisAPI()
        
    def show_statistics_chart(self, mode="period", x_index=6, y_index=3):
        headers, data = self.kopis_api.fetch_statistics_data(mode=mode)

        # 문자열로 넘어온 x/y 인덱스를 실제 인덱스로 변환
        if isinstance(x_index, str):
            try:
                x_index = headers.index(x_index)
            except ValueError:
                raise ValueError(f"'{x_index}' not found in headers: {headers}")

        if isinstance(y_index, str):
            try:
                y_index = headers.index(y_index)
            except ValueError:
                raise ValueError(f"'{y_index}' not found in headers: {headers}")

        x = [row[x_index] for row in data]
        y = [int(row[y_index]) if row[y_index].isdigit() else 0 for row in data]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(x, y) if mode == "genre" else ax.plot(x, y, marker='o')
        ax.set_title("Performance Statistics")
        ax.set_xlabel(headers[x_index])
        ax.set_ylabel(headers[y_index])
        fig.autofmt_xdate()

        return fig
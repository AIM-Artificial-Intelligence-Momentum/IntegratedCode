# KopisAPI.py
from dotenv import load_dotenv
import os
import xml.etree.ElementTree as ET
import requests

class KopisAPI:
    def __init__(self):
        load_dotenv()
        self.service_key = os.getenv("KOPIS_API_KEY")  # .env 파일에서 API 키 가져오기
        self.base_url = "http://www.kopis.or.kr/openApi/restful"
        self.data = None

    def fetch(self, endpoint: str, params: dict, parse_tags: list = None, item_tag: str = "db"):
        """
        endpoint: API 경로 (예: 'pblprfr', 'prfstsTotal')
        params: API에 전달할 쿼리스트링 파라미터
        parse_tags: XML에서 추출할 태그 리스트
        item_tag: 반복되는 항목의 태그명 (예: 'db', 'prfsts')
        """
        params["service"] = self.service_key
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        print(response.text)  
        if response.status_code != 200:
            raise Exception(f"API 요청 실패: {response.status_code}")
        root = ET.fromstring(response.content)

        if parse_tags:
            results = []
            for item in root.findall(item_tag):  # 핵심 부분!
                row = []
                for tag in parse_tags:
                    el = item.find(tag)
                    row.append(el.text if el is not None else "N/A")
                results.append(row)
            print('this is parsed : ', results)
            self.data = results
            return parse_tags, results
        else:
            return root  # 생 raw XML

    # 공연 목록 데이터 요청 함수
    def fetch_performance_list(self):
        params = {
            "stdate": "20230601",
            "eddate": "20230630",
            "cpage": 1,
            "rows": 10,
            "prfstate": "02",
            "signgucode": "11",
            "signgucodesub": "1111",
            "kidstate": "Y"
        }
        tags = ["prfnm", "prfpdfrom", "prfpdto", "fcltynm", "area", "genrenm", "openrun", "prfstate"]
        return self.fetch("pblprfr", params, parse_tags=tags, item_tag="db")

    # 공연 포스터만 따로 추출
    def fetch_posters_only(self):
        params = {
            "stdate": "20230601",
            "eddate": "20230630",
            "cpage": 1,
            "rows": 10,
            "prfstate": "02",
            "signgucode": "11",
            "signgucodesub": "1111",
            "kidstate": "Y"
        }
        root = self.fetch("pblprfr", params)
        posters = []
        for db in root.findall("db"):
            poster = db.find("poster").text if db.find("poster") is not None else None
            title = db.find("prfnm").text if db.find("prfnm") is not None else "No Title"
            if poster:
                posters.append((poster, title))
        return posters

    # 기간별 통계 요청 함수
    def fetch_statistics_data(self, mode="period", stdate="20240901", eddate="20240930"):
        if mode == "period":
            endpoint = "prfstsTotal"
            tags = ["prfcnt", "ntssnmrs", "cancelnmrs", "amount", "nmrs", "prfdtcnt", "prfdt", "prfprocnt"]
            item_tag = "prfst"
            params = {"stdate": stdate, "eddate": eddate, "ststype":"day"}
        elif mode == "genre":
            endpoint = "prfstsCate"
            tags = ["cate", "amount", "nmrs", "prfdtcnt", "prfprocnt", "nmrsprcnt", "amountspr"]
            item_tag = "prfst"
            params = {"stdate": stdate, "eddate": eddate}
        else:
            raise ValueError("Invalid mode. Use 'period' or 'genre'")

        
        return self.fetch(endpoint, params, parse_tags=tags, item_tag=item_tag)

# backend/AzureServiceModule/ChatbotService.py

from .modules.AzureOpenAIClient import get_azure_openai_client
from .modules.IntentClassifier import IntentClassifier
from .modules.StageDetector import StageDetector
from .modules.VariableExtractor import AITextExtractor
from .modules.PromptGenerator import PromptGenerator
from .modules.AISearchClient import AISearchService
from .config.VariableConfig import required_keys, categorical_keys, planning_stage_keys, sales_stage_keys
import json
import re
import httpx  # 비동기 HTTP 요청을 위한 라이브러리
from datetime import datetime

import logging

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("chatbot")

class ChatbotService:
    def __init__(self, api_key, endpoint, deployment, search_key, search_endpoint, search_index):
        # Azure OpenAI 클라이언트 초기화
        self.client = get_azure_openai_client(api_key, endpoint)
        self.deployment = deployment
        
        # 4가지 핵심 기능 초기화
        self.extractor = AITextExtractor(self.client, self.deployment, required_keys, categorical_keys)  # JSON 변수 추출기
        self.prompter = PromptGenerator(self.client, self.deployment, categorical_keys)                  # 챗봇 질문 생성기
        self.search = AISearchService(self.client, self.deployment, search_key, search_endpoint, search_index)  # 문서 검색기
        self.detector = StageDetector(self.client, self.deployment)
        self.classifier = IntentClassifier(self.client, self.deployment)

        # 상태 정보
        self.collected_vars = {}
        self.last_asked_key = None
        
        # ML API 기본 URL (같은 서버에서 실행 중이라고 가정)
        self.ml_api_base_url = "http://localhost:8000/api/ml"  # 필요에 따라 조정
        
    # 날짜를 숫자로 변환하는 함수 (ML 모델 입력용)
    def _convert_date_to_numeric(self, date_str):
        """YYYY-MM-DD 형식의 날짜를 1~365 사이의 숫자로 변환"""
        if not date_str:
            return 1.0  # 기본값
        
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day_of_year = date_obj.timetuple().tm_yday  # 1부터 365(366)까지의 날짜
            return float(day_of_year)
        except:
            return 1.0  # 변환 실패 시 기본값

    # 분석 요청 감지 함수
    def _detect_analysis_request(self, user_input):
        """사용자 입력에서 분석 요청을 감지"""
        # 단순 키워드 확인 (한국어 환경)
        simple_keywords = ["분석", "예측", "계산", "ROI", "BEP"]
        for keyword in simple_keywords:
            if keyword in user_input:
                logger.debug(f"키워드 '{keyword}'로 분석 요청 감지됨")
                return True
        
        # 정규표현식 패턴 확인
        analysis_patterns = [
            r"분석.*(해줘|해 ?주세요|부탁|부탁해|부탁드려|알려줘)",
            r"예측.*(해줘|해 ?주세요|부탁|부탁해|부탁드려|알려줘)",
            r"(관객|티켓|매출|수익|손익).*(얼마나|어떻게|예상|예측|분석)",
            r"위험.*(분석|평가|예측)",
            r"(ROI|BEP).*(알려|계산|예측)",
            r"분석.*(결과|해보|시작)"
        ]
        
        for pattern in analysis_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                logger.debug(f"패턴 '{pattern}'으로 분석 요청 감지됨")
                return True
        
        logger.debug("분석 요청 감지되지 않음")
        return False
    
    # 필요한 분석 유형 결정 함수
    def _determine_analysis_type(self, user_input, stage):
        """사용자 입력과 단계를 기반으로 필요한 분석 유형 결정"""
        # 통계 분석 우선 검출 (단계 구분 없음)
        if re.search(r"(장르별|장르.{0,5}통계|장르.{0,5}분석|장르.{0,5}결산|장르.{0,5}추이)", user_input, re.IGNORECASE):
            return ["genre_stats"]
            
        if re.search(r"(지역별|지역.{0,5}통계|지역.{0,5}분석|지역.{0,5}결산|지역.{0,5}추이)", user_input, re.IGNORECASE):
            return ["regional_stats"]
        
        if re.search(r"(공연장.{0,5}규모|규모별|좌석.{0,5}규모|규모.{0,5}분석)", user_input, re.IGNORECASE):
            return ["venue_scale_stats"]
        
        # 티켓 위험도 분석은 단계에 관계없이 요청 가능하도록 설정
        if re.search(r"(티켓.{0,5}위험|위험.{0,5}분석|티켓.{0,5}리스크|위험도)", user_input, re.IGNORECASE):
            return ["ticket_risk_selling"]
        
        # 기존 분석 유형 (단계 구분 적용)
        # 기본 분석 유형
        if stage == "기획":
            analysis_types = ["accumulated_sales_planning", "roi_bep_planning"]
        else:  # 판매 단계
            analysis_types = ["accumulated_sales_selling", "roi_bep_selling", "ticket_risk_selling"]
        
        # 특정 분석 유형 검출
        if re.search(r"(관객|티켓|판매량|매출액)", user_input, re.IGNORECASE):
            if stage == "기획":
                return ["accumulated_sales_planning"]
            else:
                return ["accumulated_sales_selling"]
                
        elif re.search(r"(손익|수익|ROI|BEP|손익분기점)", user_input, re.IGNORECASE):
            if stage == "기획":
                return ["roi_bep_planning"]
            else:
                return ["roi_bep_selling"]
                
        elif re.search(r"(위험|리스크|가능성|실패)", user_input, re.IGNORECASE) and stage == "판매":
            return ["ticket_risk_selling"]
            
        # 명확한 패턴이 없으면 단계별 기본 분석 실행
        return analysis_types
    
    # 변수 포맷 변환 함수
    def _format_variables_for_ml_api(self, analysis_type):
        """수집된 변수를 ML API 형식에 맞게 변환"""
        formatted_vars = self.collected_vars.copy()
        
        # 날짜를 숫자로 변환
        if "start_date" in formatted_vars:
            formatted_vars["start_date_numeric"] = self._convert_date_to_numeric(formatted_vars["start_date"])
        
        # 모든 숫자 필드를 float로 변환
        numeric_fields = [
            "capacity", "star_power", "ticket_price", "marketing_budget", 
            "sns_mention_count", "daily_sales", "booking_rate", "ad_exposure", 
            "sns_mention_daily", "production_cost", "variable_cost_rate", 
            "accumulated_sales"
        ]
        
        for field in numeric_fields:
            if field in formatted_vars:
                try:
                    if isinstance(formatted_vars[field], str):
                        # 문자열에서 숫자만 추출
                        formatted_vars[field] = float(''.join(c for c in formatted_vars[field] if c.isdigit() or c == '.'))
                    else:
                        formatted_vars[field] = float(formatted_vars[field])
                except (ValueError, TypeError):
                    # 변환 실패 시 해당 필드 제거
                    formatted_vars.pop(field, None)
        
        # promo_event_flag를 정수로 변환
        if "promo_event_flag" in formatted_vars:
            if isinstance(formatted_vars["promo_event_flag"], str):
                formatted_vars["promo_event_flag"] = 1 if formatted_vars["promo_event_flag"].lower() == "true" else 0
            elif isinstance(formatted_vars["promo_event_flag"], bool):
                formatted_vars["promo_event_flag"] = 1 if formatted_vars["promo_event_flag"] else 0
        
        # 분석 유형별 필수 필드 설정
        if analysis_type == "accumulated_sales_planning":
            defaults = {
                "genre": formatted_vars.get("genre", "뮤지컬"),
                "region": formatted_vars.get("region", "서울특별시"),
                "start_date_numeric": formatted_vars.get("start_date_numeric", 1.0),
                "capacity": formatted_vars.get("capacity", 502000.5),
                "star_power": formatted_vars.get("star_power", 280.0),
                "ticket_price": formatted_vars.get("ticket_price", 40439.5),
                "marketing_budget": formatted_vars.get("marketing_budget", 8098512.5),
                "sns_mention_count": formatted_vars.get("sns_mention_count", 38.0)
            }
            return defaults
        
        elif analysis_type == "accumulated_sales_selling":
            defaults = {
                "genre": formatted_vars.get("genre", "뮤지컬"),
                "region": formatted_vars.get("region", "서울특별시"),
                "start_date_numeric": formatted_vars.get("start_date_numeric", 1.0),
                "capacity": formatted_vars.get("capacity", 502000.5),
                "star_power": formatted_vars.get("star_power", 280.0),
                "ticket_price": formatted_vars.get("ticket_price", 40439.5),
                "marketing_budget": formatted_vars.get("marketing_budget", 8098512.5),
                "sns_mention_count": formatted_vars.get("sns_mention_count", 38.0),
                "daily_sales": formatted_vars.get("daily_sales", 2.0),
                "booking_rate": formatted_vars.get("booking_rate", 0.7),
                "ad_exposure": formatted_vars.get("ad_exposure", 303284.5),
                "sns_mention_daily": formatted_vars.get("sns_mention_daily", 38.0)
            }
            return defaults
        
        elif analysis_type == "roi_bep_planning" or analysis_type == "roi_bep_selling":
            defaults = {
                "production_cost": formatted_vars.get("production_cost", 570111934.0),
                "marketing_budget": formatted_vars.get("marketing_budget", 8098512.5),
                "ticket_price": formatted_vars.get("ticket_price", 40349.5),
                "capacity": formatted_vars.get("capacity", 280.0),
                "variable_cost_rate": formatted_vars.get("variable_cost_rate", 0.17755),
                "accumulated_sales": formatted_vars.get("accumulated_sales", 105.0)
            }
            return defaults
        
        elif analysis_type == "ticket_risk_selling":
            defaults = {
                "genre": formatted_vars.get("genre", "뮤지컬"),
                "region": formatted_vars.get("region", "서울특별시"),
                "start_date_numeric": formatted_vars.get("start_date_numeric", 1.0),
                "capacity": formatted_vars.get("capacity", 280.0),
                "star_power": formatted_vars.get("star_power", 1.0),
                "daily_sales": formatted_vars.get("daily_sales", 2.0),
                "accumulated_sales": formatted_vars.get("accumulated_sales", 105.0),
                "ad_exposure": formatted_vars.get("ad_exposure", 303284.5),
                "sns_mention_daily": formatted_vars.get("sns_mention_daily", 0.0),
                "promo_event_flag": formatted_vars.get("promo_event_flag", 0)
            }
            return defaults
        
        return formatted_vars
        
    
    # ML API 호출 함수
    async def _call_ml_api(self, analysis_type, formatted_vars):
        """ML API 내부 직접 호출"""
        try:
            # ML 모듈에서 함수 직접 임포트
            from backend.ModelPredictionModule.analysis_module import (
                predict_acc_sales_planning,
                predict_acc_sales_selling,
                predict_roi_bep_planning,
                predict_roi_bep_selling,
                predict_ticket_risk
            )
            
            # 단일 객체를 리스트로 포장
            input_data = [formatted_vars]
            
            # 직접 함수 호출
            if analysis_type == "accumulated_sales_planning":
                preds = predict_acc_sales_planning(input_data)
                return {"predictions": preds}
            elif analysis_type == "roi_bep_planning":
                preds = predict_roi_bep_planning(input_data)
                return {"predictions": preds}
            elif analysis_type == "accumulated_sales_selling":
                preds = predict_acc_sales_selling(input_data)
                return {"predictions": preds}
            elif analysis_type == "roi_bep_selling":
                preds = predict_roi_bep_selling(input_data)
                return {"predictions": preds}
            elif analysis_type == "ticket_risk_selling":
                preds = predict_ticket_risk(input_data)
                return {"risk_labels": preds}
            else:
                return self._get_fallback_response(analysis_type)
        except Exception as e:
            logger.error(f"직접 함수 호출 오류: {str(e)}")
            return self._get_fallback_response(analysis_type)
    
    # 분석 결과 해석 함수
    def _interpret_analysis_results(self, analysis_type, results):
        """분석 결과를 사용자 친화적인 텍스트로 변환"""
        try:
            if "error" in results:
                return f"분석 중 오류가 발생했습니다: {results['error']}"
            
            # 중첩된 predictions 구조 처리
            if "predictions" in results and isinstance(results["predictions"], dict):
                nested_results = results["predictions"]
                
                if analysis_type == "accumulated_sales_planning" or analysis_type == "accumulated_sales_selling":
                    # 중첩된 predictions 배열에서 첫 번째 값 추출
                    predictions_array = nested_results.get("predictions", [0])
                    value = predictions_array[0] if len(predictions_array) > 0 else 0
                    return f"🎭 예상 관객 수: 약 {int(value):,}명\n"
                    
                elif analysis_type == "roi_bep_planning" or analysis_type == "roi_bep_selling":
                    # 중첩된 predictions 배열의 배열에서 값 추출
                    predictions_array = nested_results.get("predictions", [[0, 0]])
                    value = predictions_array[0] if len(predictions_array) > 0 else [0, 0]
                    
                    roi = value[0] if len(value) > 0 else 0
                    bep = value[1] if len(value) > 1 else 0
                    
                    roi_percentage = roi * 100  # 비율을 퍼센트로 변환 (필요한 경우)
                    
                    roi_text = f"📈 예상 ROI(투자수익률): {roi_percentage:.2f}%\n"
                    bep_text = f"⚖️ 손익분기점(BEP): 약 {int(bep):,}명의 관객\n"
                    
                    return roi_text + bep_text
            
            # 기존 비중첩 구조 처리 (이전 구조와의 호환성 유지)
            elif "predictions" in results and isinstance(results["predictions"], list):
                if analysis_type == "accumulated_sales_planning" or analysis_type == "accumulated_sales_selling":
                    value = results.get("predictions", [0])[0]
                    return f"🎭 예상 관객 수: 약 {int(value):,}명\n"
                    
                elif analysis_type == "roi_bep_planning" or analysis_type == "roi_bep_selling":
                    value = results.get("predictions", [0, 0])
                    roi = value[0]
                    bep = value[1] if len(value) > 1 else 0
                    
                    roi_text = f"📈 예상 ROI(투자수익률): {roi:.2f}%\n"
                    bep_text = f"⚖️ 손익분기점(BEP): 약 {int(bep):,}명의 관객\n"
                    
                    return roi_text + bep_text
                    
            elif "risk_labels" in results:
                risk_label = results.get("risk_labels", [0])[0]
                risk_level = "낮음" if risk_label == 0 else "높음"
                risk_text = f"⚠️ 티켓 판매 위험도: {risk_level}\n"
                
                if risk_label == 1:
                    advice = "추가 마케팅 활동이나 프로모션을 고려해보세요."
                else:
                    advice = "현재 판매 추세가 양호합니다."
                    
                return risk_text + advice
                
            return "분석 결과를 해석할 수 없습니다."
            
        except Exception as e:
            logger.error(f"결과 해석 오류: {str(e)}", exc_info=True)
            return f"결과 해석 중 오류 발생: {str(e)}"
    
    # 기존 handle_user_input 함수 확장
    async def handle_user_input(self, user_input, history):
        if not isinstance(history, list):
            history = []

        # 1. 사용자 의도 분류: 수집 / 검색 / 혼합
        intent = self.classifier.classify_intent(user_input)
        stage = self.detector.detect_stage(user_input)
        
        logger.debug(f"사용자 입력: '{user_input}'")
        logger.debug(f"감지된 의도: {intent}")
        logger.debug(f"감지된 단계: {stage}")
        
        reply_parts = []
        analysis_results = {}

        # 2-1. JSON 변수 수집
        if intent in ["수집", "혼합"]:
            extracted = self.extractor.extract_variables(user_input, fallback_key=self.last_asked_key)
            logger.debug(f"추출된 변수: {extracted}")
            
            for key, val in extracted.items():
                if val is not None:
                    self.collected_vars[key] = val

        # 2-2. 분석 요청 감지 및 처리
        is_analysis_request = self._detect_analysis_request(user_input)
        logger.debug(f"분석 요청 감지: {is_analysis_request}")
        
        if is_analysis_request:
            analysis_types = self._determine_analysis_type(user_input, stage)
            logger.debug(f"결정된 분석 유형: {analysis_types}")
            
            # 분석 결과 모음
            analysis_results_text = []
            
            for analysis_type in analysis_types:
                formatted_vars = self._format_variables_for_ml_api(analysis_type)
                logger.debug(f"API 호출 전 변수: {formatted_vars}")
                
                api_result = await self._call_ml_api(analysis_type, formatted_vars)
                logger.debug(f"API 응답: {api_result}")
                
                result_text = self._interpret_analysis_results(analysis_type, api_result)
                logger.debug(f"해석된 결과: {result_text}")
                
                analysis_results_text.append(result_text)
                analysis_results[analysis_type] = api_result
            
            # 분석 결과 추가
            if analysis_results_text:
                analysis_text = "## 📊 분석 결과\n\n" + "\n".join(analysis_results_text)
                logger.debug(f"추가될 분석 결과: {analysis_text}")
                reply_parts.append(analysis_text)
            else:
                logger.warning("분석 결과가 비어있음")

        # 2-3. 추가 유도 질문 생성
        next_question, next_key = self.prompter.generate(self.collected_vars, user_input, stage)
        if next_key:
            self.last_asked_key = next_key
        reply_parts.append(next_question)

        # 3. AI 문서 검색
        if intent in ["검색", "혼합"]:
            summary = self.search.query(user_input)
            reply_parts.append("📖 관련 문서 요약:\n\n" + summary)

        # 4. 응답 및 상태 반환
        full_reply = "\n\n".join(reply_parts)
        history.append((user_input, full_reply))
        
        logger.debug(f"최종 응답 구성 요소: {reply_parts}")
        logger.debug(f"현재 수집된 변수: {self.collected_vars}")

        return {
            "chat_history": history,
            "response_text": full_reply,
            "structured_data": self.collected_vars,
            "analysis_results": analysis_results,
            "intent": intent,
            "stage": stage,
        }
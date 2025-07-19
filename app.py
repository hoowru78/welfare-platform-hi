from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import uuid
import hashlib
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import json
import re

app = Flask(__name__)
CORS(app)

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///welfare.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# 암호화 키 설정
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY', Fernet.generate_key())
cipher_suite = Fernet(ENCRYPTION_KEY)

db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_key = db.Column(db.String(50), unique=True, nullable=False)
    encrypted_name = db.Column(db.Text, nullable=False)
    encrypted_birth_date = db.Column(db.Text, nullable=False)
    encrypted_address = db.Column(db.Text, nullable=False)
    district_code = db.Column(db.String(10), nullable=False)
    age_group = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, name, birth_date, address, district_code):
        self.user_key = self.generate_user_key()
        self.encrypted_name = cipher_suite.encrypt(name.encode()).decode()
        self.encrypted_birth_date = cipher_suite.encrypt(birth_date.encode()).decode()
        self.encrypted_address = cipher_suite.encrypt(address.encode()).decode()
        self.district_code = district_code
        self.age_group = self.calculate_age_group(birth_date)
        self.expires_at = datetime.utcnow() + timedelta(days=30)

    def generate_user_key(self):
        """사용자 조회용 키 생성"""
        return hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:12].upper()

    def calculate_age_group(self, birth_date):
        """생년월일로부터 연령대 계산"""
        try:
            birth_year = int(birth_date[:4])
            current_year = datetime.now().year
            age = current_year - birth_year
            
            if age >= 80:
                return "80+"
            elif age >= 75:
                return "75-79"
            elif age >= 70:
                return "70-74"
            elif age >= 65:
                return "65-69"
            else:
                return "60-64"
        except:
            return "65-69"

    def get_decrypted_name(self):
        return cipher_suite.decrypt(self.encrypted_name.encode()).decode()

class SurveySession(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    current_step = db.Column(db.Integer, default=1)
    total_steps = db.Column(db.Integer, default=4)
    progress_percentage = db.Column(db.Integer, default=0)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    completion_time = db.Column(db.DateTime)
    session_status = db.Column(db.String(20), default='in_progress')
    temporary_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SurveyResponse(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = db.Column(db.String(36), db.ForeignKey('survey_session.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.String(36), nullable=False)
    selected_options = db.Column(db.Text, nullable=False)
    response_score = db.Column(db.Integer, default=0)
    response_time = db.Column(db.DateTime, default=datetime.utcnow)

class WelfareService(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category_id = db.Column(db.Integer, nullable=False)
    service_name = db.Column(db.String(100), nullable=False)
    service_description = db.Column(db.Text, nullable=False)
    benefit_amount = db.Column(db.String(50))
    benefit_type = db.Column(db.String(30))
    application_method = db.Column(db.Text)
    required_documents = db.Column(db.Text)
    contact_info = db.Column(db.Text)
    application_url = db.Column(db.String(255))
    service_duration = db.Column(db.String(50))
    renewal_required = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Recommendation(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.String(36), db.ForeignKey('survey_session.id'), nullable=False)
    recommended_services = db.Column(db.Text, nullable=False)
    recommendation_reason = db.Column(db.Text)
    ai_confidence_score = db.Column(db.Float)
    generation_method = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_viewed = db.Column(db.Boolean, default=False)

# 설문 질문 데이터 (하드코딩으로 시작)
SURVEY_QUESTIONS = {
    1: {  # 건강 상태
        "category": "건강 상태",
        "questions": [
            {
                "id": "health_01",
                "text": "현재 건강 상태는 어떻습니까?",
                "type": "single_choice",
                "options": [
                    {"value": "very_good", "text": "매우 좋음", "score": 10},
                    {"value": "good", "text": "좋음", "score": 20},
                    {"value": "normal", "text": "보통", "score": 40},
                    {"value": "bad", "text": "나쁨", "score": 70},
                    {"value": "very_bad", "text": "매우 나쁨", "score": 100}
                ]
            },
            {
                "id": "health_02",
                "text": "정기적으로 복용하는 약이 있으십니까?",
                "type": "single_choice",
                "options": [
                    {"value": "none", "text": "없음", "score": 10},
                    {"value": "one_two", "text": "1-2가지", "score": 30},
                    {"value": "three_five", "text": "3-5가지", "score": 60},
                    {"value": "many", "text": "6가지 이상", "score": 100}
                ]
            },
            {
                "id": "health_03",
                "text": "병원을 얼마나 자주 방문하십니까?",
                "type": "single_choice",
                "options": [
                    {"value": "rarely", "text": "거의 안 감", "score": 10},
                    {"value": "sometimes", "text": "가끔 (연 1-2회)", "score": 20},
                    {"value": "regular", "text": "정기적으로 (월 1-2회)", "score": 50},
                    {"value": "frequent", "text": "자주 (주 1회 이상)", "score": 80}
                ]
            },
            {
                "id": "health_04",
                "text": "일상생활에서 도움이 필요한 일이 있습니까?",
                "type": "multiple_choice",
                "options": [
                    {"value": "none", "text": "도움 필요 없음", "score": 0},
                    {"value": "walking", "text": "걷기/이동", "score": 30},
                    {"value": "housework", "text": "집안일", "score": 25},
                    {"value": "shopping", "text": "장보기", "score": 20},
                    {"value": "medical", "text": "병원 방문", "score": 35},
                    {"value": "bath", "text": "목욕/세면", "score": 40}
                ]
            }
        ]
    },
    2: {  # 생활 환경
        "category": "생활 환경",
        "questions": [
            {
                "id": "living_01",
                "text": "현재 거주 형태는 어떻게 되십니까?",
                "type": "single_choice",
                "options": [
                    {"value": "own", "text": "자가 (내 집)", "score": 10},
                    {"value": "rent", "text": "임대 (전세/월세)", "score": 30},
                    {"value": "family", "text": "가족과 함께 거주", "score": 15},
                    {"value": "facility", "text": "시설 거주", "score": 50}
                ]
            },
            {
                "id": "living_02",
                "text": "함께 거주하는 가족이 있습니까?",
                "type": "single_choice",
                "options": [
                    {"value": "alone", "text": "혼자 거주", "score": 60},
                    {"value": "spouse", "text": "배우자와 함께", "score": 20},
                    {"value": "family", "text": "자녀/가족과 함께", "score": 10},
                    {"value": "others", "text": "기타 (친구, 지인 등)", "score": 40}
                ]
            },
            {
                "id": "living_03",
                "text": "주거 환경에서 불편한 점이 있습니까?",
                "type": "multiple_choice",
                "options": [
                    {"value": "none", "text": "불편함 없음", "score": 0},
                    {"value": "stairs", "text": "계단/턱", "score": 30},
                    {"value": "cold", "text": "추위/난방", "score": 25},
                    {"value": "repair", "text": "수리 필요", "score": 35},
                    {"value": "safety", "text": "안전 문제", "score": 40},
                    {"value": "isolation", "text": "고립감", "score": 50}
                ]
            }
        ]
    },
    3: {  # 경제적 상황
        "category": "경제적 상황",
        "questions": [
            {
                "id": "economic_01",
                "text": "현재 주요 수입원은 무엇입니까?",
                "type": "multiple_choice",
                "options": [
                    {"value": "pension", "text": "연금 (국민연금, 기초연금)", "score": 30},
                    {"value": "work", "text": "근로 소득", "score": 10},
                    {"value": "family", "text": "가족 지원", "score": 20},
                    {"value": "welfare", "text": "복지 급여", "score": 60},
                    {"value": "savings", "text": "저축/적금", "score": 15},
                    {"value": "none", "text": "수입 없음", "score": 100}
                ]
            },
            {
                "id": "economic_02",
                "text": "의료비 부담은 어느 정도입니까?",
                "type": "single_choice",
                "options": [
                    {"value": "low", "text": "부담 없음", "score": 10},
                    {"value": "moderate", "text": "조금 부담", "score": 30},
                    {"value": "high", "text": "많이 부담", "score": 70},
                    {"value": "very_high", "text": "매우 부담", "score": 100}
                ]
            },
            {
                "id": "economic_03",
                "text": "생활비는 충분합니까?",
                "type": "single_choice",
                "options": [
                    {"value": "sufficient", "text": "충분함", "score": 10},
                    {"value": "adequate", "text": "적당함", "score": 30},
                    {"value": "tight", "text": "부족함", "score": 70},
                    {"value": "insufficient", "text": "매우 부족함", "score": 100}
                ]
            }
        ]
    },
    4: {  # 사회적 관계
        "category": "사회적 관계",
        "questions": [
            {
                "id": "social_01",
                "text": "가족과 얼마나 자주 연락하십니까?",
                "type": "single_choice",
                "options": [
                    {"value": "daily", "text": "매일", "score": 10},
                    {"value": "weekly", "text": "주 1-2회", "score": 20},
                    {"value": "monthly", "text": "월 1-2회", "score": 40},
                    {"value": "rarely", "text": "거의 안 함", "score": 80}
                ]
            },
            {
                "id": "social_02",
                "text": "친구나 이웃과의 관계는 어떻습니까?",
                "type": "single_choice",
                "options": [
                    {"value": "very_good", "text": "매우 좋음", "score": 10},
                    {"value": "good", "text": "좋음", "score": 20},
                    {"value": "normal", "text": "보통", "score": 40},
                    {"value": "limited", "text": "제한적", "score": 70},
                    {"value": "none", "text": "거의 없음", "score": 100}
                ]
            },
            {
                "id": "social_03",
                "text": "사회 활동에 참여하고 계십니까?",
                "type": "multiple_choice",
                "options": [
                    {"value": "none", "text": "참여 안 함", "score": 60},
                    {"value": "senior_center", "text": "경로당", "score": 10},
                    {"value": "religious", "text": "종교 활동", "score": 10},
                    {"value": "volunteer", "text": "자원봉사", "score": 5},
                    {"value": "hobby", "text": "취미 활동", "score": 10},
                    {"value": "exercise", "text": "운동/체육", "score": 5}
                ]
            }
        ]
    }
}

# API 엔드포인트들
@app.route('/api/health', methods=['GET'])
def health_check():
    """서버 상태 확인"""
    return jsonify({"status": "healthy", "message": "남해군 복지 추천 시스템 서버가 정상 작동 중입니다."})

@app.route('/api/users', methods=['POST'])
def create_user():
    """사용자 정보 등록"""
    try:
        data = request.get_json()
        
        # 필수 필드 검증
        required_fields = ['name', 'birth_date', 'address', 'district_code']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} 필드가 필요합니다."}), 400
        
        # 생년월일 형식 검증
        birth_date = data['birth_date']
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', birth_date):
            return jsonify({"error": "생년월일은 YYYY-MM-DD 형식이어야 합니다."}), 400
        
        # 새 사용자 생성
        user = User(
            name=data['name'],
            birth_date=birth_date,
            address=data['address'],
            district_code=data['district_code']
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "user_id": user.id,
            "user_key": user.user_key,
            "age_group": user.age_group,
            "message": "사용자 정보가 성공적으로 등록되었습니다."
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/survey/questions', methods=['GET'])
def get_survey_questions():
    """설문 질문 조회"""
    step = request.args.get('step', 1, type=int)
    
    if step not in SURVEY_QUESTIONS:
        return jsonify({"error": "유효하지 않은 단계입니다."}), 400
    
    return jsonify({
        "step": step,
        "total_steps": len(SURVEY_QUESTIONS),
        "category": SURVEY_QUESTIONS[step]["category"],
        "questions": SURVEY_QUESTIONS[step]["questions"]
    })

@app.route('/api/survey/start', methods=['POST'])
def start_survey():
    """설문 시작"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({"error": "user_id가 필요합니다."}), 400
        
        # 사용자 존재 확인
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "사용자를 찾을 수 없습니다."}), 404
        
        # 새 설문 세션 생성
        session = SurveySession(
            user_id=user_id,
            total_steps=len(SURVEY_QUESTIONS)
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "session_id": session.id,
            "current_step": session.current_step,
            "total_steps": session.total_steps
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/survey/answer', methods=['POST'])
def submit_survey_answer():
    """설문 응답 제출"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        answers = data.get('answers', [])
        
        if not session_id or not answers:
            return jsonify({"error": "session_id와 answers가 필요합니다."}), 400
        
        # 세션 확인
        session = SurveySession.query.get(session_id)
        if not session:
            return jsonify({"error": "설문 세션을 찾을 수 없습니다."}), 404
        
        # 응답 저장
        for answer in answers:
            response = SurveyResponse(
                session_id=session_id,
                user_id=session.user_id,
                question_id=answer['question_id'],
                selected_options=json.dumps(answer['selected_options']),
                response_score=answer.get('score', 0)
            )
            db.session.add(response)
        
        # 세션 업데이트
        session.current_step += 1
        session.progress_percentage = (session.current_step / session.total_steps) * 100
        session.last_activity = datetime.utcnow()
        
        if session.current_step > session.total_steps:
            session.session_status = 'completed'
            session.completion_time = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "current_step": session.current_step,
            "progress_percentage": session.progress_percentage,
            "is_completed": session.session_status == 'completed'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/results/<user_key>')
def get_results(user_key):
    """결과 조회"""
    try:
        # 사용자 확인
        user = User.query.filter_by(user_key=user_key).first()
        if not user:
            return jsonify({"error": "사용자를 찾을 수 없습니다."}), 404
        
        # 가장 최근 완료된 설문 찾기
        latest_session = SurveySession.query.filter_by(
            user_id=user.id,
            session_status='completed'
        ).order_by(SurveySession.completion_time.desc()).first()
        
        if not latest_session:
            return jsonify({"error": "완료된 설문이 없습니다."}), 404
        
        # 추천 결과 조회
        recommendation = Recommendation.query.filter_by(
            user_id=user.id,
            session_id=latest_session.id
        ).first()
        
        if not recommendation:
            # 추천 결과가 없으면 생성
            recommendation = generate_recommendation(user.id, latest_session.id)
        
        return jsonify({
            "user_name": user.get_decrypted_name(),
            "completion_time": latest_session.completion_time.isoformat(),
            "recommendations": json.loads(recommendation.recommended_services),
            "recommendation_reason": recommendation.recommendation_reason,
            "confidence_score": recommendation.ai_confidence_score
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_recommendation(user_id, session_id):
    """AI 기반 복지 추천 생성"""
    try:
        # 사용자 정보 조회
        user = User.query.get(user_id)
        
        # 설문 응답 조회
        responses = SurveyResponse.query.filter_by(
            user_id=user_id,
            session_id=session_id
        ).all()
        
        # 점수 계산
        health_score = 0
        living_score = 0
        economic_score = 0
        social_score = 0
        
        for response in responses:
            question_id = response.question_id
            if question_id.startswith('health_'):
                health_score += response.response_score
            elif question_id.startswith('living_'):
                living_score += response.response_score
            elif question_id.startswith('economic_'):
                economic_score += response.response_score
            elif question_id.startswith('social_'):
                social_score += response.response_score
        
        # 추천 로직 (Rule-based)
        recommended_services = []
        
        # 건강 관련 추천
        if health_score > 100:
            recommended_services.extend([
                {
                    "id": "health_medical_support",
                    "name": "노인 의료비 지원 서비스",
                    "category": "건강의료",
                    "description": "65세 이상 어르신의 의료비 부담을 줄여드리는 서비스입니다. 월 최대 30만원까지 지원받으실 수 있습니다.",
                    "benefit_amount": "월 최대 30만원",
                    "benefit_type": "의료비 지원",
                    "priority": 1,
                    "match_score": min(100, health_score)
                },
                {
                    "id": "namhae_customized_care",
                    "name": "남해군 노인맞춤돌봄서비스",
                    "category": "생활지원",
                    "description": "일상생활이 어려운 취약 노인에게 돌봄서비스(방문·전화·생활교육 등)를 제공하여 노후생활 안정과 건강 유지를 지원합니다.",
                    "benefit_amount": "무료",
                    "benefit_type": "돌봄 서비스",
                    "priority": 2,
                    "match_score": min(100, health_score + living_score)
                }
            ])
        
        # 경제 관련 추천
        if economic_score > 80:
            recommended_services.extend([
                {
                    "id": "basic_pension",
                    "name": "기초연금",
                    "category": "경제지원",
                    "description": "65세 이상 어르신에게 안정적인 소득기반을 제공하는 연금입니다. 소득 수준에 따라 차등 지급됩니다.",
                    "benefit_amount": "월 최대 342,510원",
                    "benefit_type": "현금 지원",
                    "priority": 1,
                    "match_score": min(100, economic_score)
                },
                {
                    "id": "basic_livelihood",
                    "name": "생계급여 (기초생활보장)",
                    "category": "경제지원",
                    "description": "생계가 어려운 어르신에게 의복, 음식물 및 연료비와 그 밖에 일상생활에 기본적으로 필요한 금품을 지급합니다.",
                    "benefit_amount": "가구별 차등 지급",
                    "benefit_type": "현금 지원",
                    "priority": 2,
                    "match_score": min(100, economic_score)
                }
            ])
        
        # 사회 관련 추천
        if social_score > 60:
            recommended_services.extend([
                {
                    "id": "senior_jobs",
                    "name": "노인일자리 및 사회활동 지원사업",
                    "category": "사회참여",
                    "description": "노인이 일자리와 사회활동을 통하여 활동적이고 생산적인 노후생활을 영위할 수 있도록 지원합니다.",
                    "benefit_amount": "활동비 지급",
                    "benefit_type": "일자리 지원",
                    "priority": 3,
                    "match_score": min(100, social_score)
                },
                {
                    "id": "namhae_dementia_prevention",
                    "name": "남해군 치매 예방 교실",
                    "category": "건강의료",
                    "description": "치매 예방을 위한 교육과 다양한 활동을 제공하는 프로그램입니다.",
                    "benefit_amount": "무료",
                    "benefit_type": "교육 프로그램",
                    "priority": 4,
                    "match_score": min(100, social_score + health_score)
                }
            ])
        
        # 주거 관련 추천
        if living_score > 70:
            recommended_services.append({
                "id": "senior_housing",
                "name": "노인주거복지시설",
                "category": "주거지원",
                "description": "노인에게 주거시설과 생활에 필요한 편의를 제공하는 시설입니다.",
                "benefit_amount": "소득 수준별 차등",
                "benefit_type": "주거 지원",
                "priority": 5,
                "match_score": min(100, living_score)
            })
        
        # 우선순위 정렬
        recommended_services.sort(key=lambda x: (-x['match_score'], x['priority']))
        
        # 상위 5개만 선택
        top_recommendations = recommended_services[:5]
        
        # 추천 사유 생성
        reason = f"설문 결과 분석: 건강({health_score}점), 생활({living_score}점), 경제({economic_score}점), 사회({social_score}점)"
        
        # 추천 결과 저장
        recommendation = Recommendation(
            user_id=user_id,
            session_id=session_id,
            recommended_services=json.dumps(top_recommendations),
            recommendation_reason=reason,
            ai_confidence_score=85.0,
            generation_method="rule_based"
        )
        
        db.session.add(recommendation)
        db.session.commit()
        
        return recommendation
        
    except Exception as e:
        db.session.rollback()
        raise e

# 웹페이지 라우트들
@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/survey')
def survey():
    """설문조사 페이지"""
    return render_template('survey.html')

@app.route('/results')
def results():
    """결과 페이지"""
    return render_template('results.html')

# 데이터베이스 초기화 함수
def create_tables():
    """데이터베이스 테이블 생성 및 초기 데이터 설정"""
    db.create_all()
    
    # 복지 서비스 데이터 초기화
    if WelfareService.query.count() == 0:
        init_welfare_services()

def init_welfare_services():
    """복지 서비스 초기 데이터 입력"""
    services = [
        {
            "category_id": 1,
            "service_name": "기초연금",
            "service_description": "65세 이상 어르신에게 안정적인 소득기반을 제공하는 연금입니다.",
            "benefit_amount": "월 최대 342,510원",
            "benefit_type": "현금 지원",
            "application_method": "읍면동 행정복지센터 방문 또는 온라인 신청",
            "required_documents": "신분증, 기초연금 신청서, 소득재산 신고서",
            "contact_info": "국민연금공단 콜센터 1355",
            "application_url": "https://www.bokjiro.go.kr"
        },
        {
            "category_id": 2,
            "service_name": "남해군 노인맞춤돌봄서비스",
            "service_description": "일상생활이 어려운 취약 노인에게 돌봄서비스를 제공합니다.",
            "benefit_amount": "무료",
            "benefit_type": "돌봄 서비스",
            "application_method": "주소지 관할 읍·면 행정복지센터 방문 또는 전화 상담",
            "required_documents": "신분증, 소득확인서류",
            "contact_info": "남해군청 노인복지과 055-860-8300",
            "service_duration": "연중 상시"
        },
        {
            "category_id": 1,
            "service_name": "노인 의료비 지원",
            "service_description": "노인성 질환 치료비 및 의료비를 지원합니다.",
            "benefit_amount": "질환별 차등 지원",
            "benefit_type": "의료비 지원",
            "application_method": "관할 보건소 방문 신청",
            "required_documents": "의료진단서, 소득확인서류",
            "contact_info": "남해군 보건소 055-860-8000"
        }
    ]
    
    for service_data in services:
        service = WelfareService(**service_data)
        db.session.add(service)
    
    db.session.commit()

# 애플리케이션 초기화
def initialize_app():
    """앱 초기화 및 데이터베이스 설정"""
    with app.app_context():
        create_tables()

# Render 배포용 초기화
try:
    initialize_app()
except Exception as e:
    print(f"초기화 중 오류 발생: {e}")

if __name__ == '__main__':
    # 로컬 개발 환경
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 
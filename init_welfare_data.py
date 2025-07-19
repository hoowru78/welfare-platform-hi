#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
남해군 노인 복지 추천 시스템 - 복지 데이터 초기화 스크립트
"""

import sys
import os
import json
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 앱 초기화
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///welfare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 모델 정의 (app.py와 동일)
class WelfareService(db.Model):
    id = db.Column(db.String(36), primary_key=True)
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

# 복지 서비스 데이터 (복지 자료 파일 기반)
WELFARE_SERVICES = [
    # 전국 복지 서비스
    {
        "id": "basic_pension",
        "category_id": 3,  # 경제지원
        "service_name": "기초연금",
        "service_description": "65세 이상 어르신에게 안정적인 소득기반을 제공하는 연금입니다. 소득인정액이 선정기준 이하인 경우 지급됩니다.",
        "benefit_amount": "월 최대 342,510원 (저소득층 300,000원)",
        "benefit_type": "현금 지원",
        "application_method": "읍·면·동 행정복지센터 방문 또는 온라인 신청 (복지로 www.bokjiro.go.kr)",
        "required_documents": "기초연금 신청서, 소득재산 신고서, 신분증, 통장사본",
        "contact_info": "국민연금공단 콜센터 1355, 남해군청 복지정책과 055-860-8300",
        "application_url": "https://www.bokjiro.go.kr",
        "service_duration": "매월 25일 지급",
        "renewal_required": False
    },
    
    {
        "id": "senior_jobs",
        "category_id": 4,  # 사회참여
        "service_name": "노인일자리 및 사회활동 지원사업",
        "service_description": "65세 이상 어르신이 일자리와 사회활동을 통해 활동적이고 생산적인 노후생활을 영위할 수 있도록 지원합니다.",
        "benefit_amount": "활동비 월 최대 71만원 (사업 유형별 차등)",
        "benefit_type": "일자리 지원",
        "application_method": "시·군·구 또는 수행기관(노인복지관, 시니어클럽 등)에 관련서류 제출",
        "required_documents": "참여신청서, 개인정보 수집 동의서, 관련 자격증(해당자)",
        "contact_info": "남해군청 노인복지과 055-860-8300",
        "service_duration": "연중",
        "renewal_required": True
    },
    
    {
        "id": "senior_housing_welfare",
        "category_id": 5,  # 주거지원
        "service_name": "노인주거복지시설",
        "service_description": "양로시설, 노인공동생활가정, 노인복지주택 등 노인에게 주거시설과 생활편의를 제공합니다.",
        "benefit_amount": "무료/실비/유료 (소득수준별)",
        "benefit_type": "주거 지원",
        "application_method": "시·군·구 또는 해당 시설에 입소신청서 제출",
        "required_documents": "입소신청서, 건강진단서, 소득증명서, 가족관계증명서",
        "contact_info": "남해군청 복지정책과 055-860-8300",
        "service_duration": "입소 기간 중",
        "renewal_required": False
    },
    
    {
        "id": "elderly_medical_support",
        "category_id": 1,  # 건강의료
        "service_name": "노인성 질환 의료비 지원",
        "service_description": "60세 이상 노인의 안질환, 무릎관절증, 치아건강(임플란트, 틀니) 등 의료비를 지원합니다.",
        "benefit_amount": "질환별 차등 지원 (수술비, 치료비 본인부담금 전액 또는 일부)",
        "benefit_type": "의료비 지원",
        "application_method": "관할 보건소 방문 신청",
        "required_documents": "의료진단서, 소득확인서류, 신분증, 의료비 영수증",
        "contact_info": "남해군 보건소 055-860-8000",
        "service_duration": "지원 결정 후 1년",
        "renewal_required": True
    },
    
    {
        "id": "dementia_screening",
        "category_id": 1,  # 건강의료
        "service_name": "치매검진 지원",
        "service_description": "60세 이상 노인을 대상으로 치매 선별검사 및 진단·감별검사를 지원합니다.",
        "benefit_amount": "선별검사 무료, 진단검사 8만원 한도",
        "benefit_type": "의료비 지원",
        "application_method": "보건소 또는 치매안심센터 방문",
        "required_documents": "신분증, 건강보험증",
        "contact_info": "남해군 치매안심센터 055-860-8000",
        "service_duration": "연 1회",
        "renewal_required": False
    },
    
    {
        "id": "basic_livelihood",
        "category_id": 3,  # 경제지원
        "service_name": "생계급여 (기초생활보장)",
        "service_description": "생계가 곤란한 수급자에게 의복, 음식물, 연료비 등 기본적인 생활비를 지원합니다.",
        "benefit_amount": "가구별 차등 지급 (중위소득 32% 기준)",
        "benefit_type": "현금 지원",
        "application_method": "거주지 관할 읍·면·동 행정복지센터 방문 신청",
        "required_documents": "신청서, 소득재산 신고서, 금융정보 제공동의서",
        "contact_info": "남해군청 복지정책과 055-860-8300",
        "service_duration": "매월 20일 지급",
        "renewal_required": False
    },
    
    {
        "id": "tax_deduction",
        "category_id": 3,  # 경제지원
        "service_name": "세금 공제 혜택",
        "service_description": "부양가족 기본공제, 경로우대공제, 비과세종합저축 등 세금 혜택을 제공합니다.",
        "benefit_amount": "기본공제 150만원, 경로우대공제 100만원 등",
        "benefit_type": "세금 감면",
        "application_method": "연말정산 또는 종합소득세 신고 시 적용",
        "required_documents": "소득세 신고서, 부양가족 증명서류",
        "contact_info": "국세청 126, 남해세무서 055-860-7000",
        "service_duration": "연간",
        "renewal_required": True
    },
    
    # 남해군 특화 복지 서비스
    {
        "id": "namhae_customized_care",
        "category_id": 2,  # 생활지원
        "service_name": "남해군 노인맞춤돌봄서비스",
        "service_description": "일상생활이 어려운 취약 노인에게 돌봄서비스(방문·전화·생활교육 등)를 제공하여 노후생활 안정과 건강 유지를 지원합니다.",
        "benefit_amount": "무료 (중점돌봄군 월 40시간, 일반돌봄군 월 16시간)",
        "benefit_type": "돌봄 서비스",
        "application_method": "주소지 관할 읍·면 행정복지센터 방문 또는 전화 상담",
        "required_documents": "신분증, 소득확인서류, 건강상태 확인서(해당시)",
        "contact_info": "남해군청 노인복지과 055-860-8300",
        "service_duration": "연중 상시",
        "renewal_required": True
    },
    
    {
        "id": "namhae_dementia_prevention",
        "category_id": 1,  # 건강의료
        "service_name": "남해군 치매 예방 교실",
        "service_description": "치매환자 및 치매고위험군을 제외한 일반 어르신을 대상으로 경로당, 복지관 등을 순회하며 치매 예방 교육과 활동을 제공합니다.",
        "benefit_amount": "무료",
        "benefit_type": "교육 프로그램",
        "application_method": "읍·면 행정복지센터 또는 보건소 방문/전화 신청",
        "required_documents": "신분증, 기초 인지검사 결과",
        "contact_info": "남해군 보건소 055-860-8000",
        "service_duration": "주 1~2회 프로그램",
        "renewal_required": False
    },
    
    {
        "id": "namhae_dementia_shelter",
        "category_id": 1,  # 건강의료
        "service_name": "남해군 치매 환자 쉼터",
        "service_description": "치매 진단을 받은 어르신 중 장기요양 서비스를 받지 않는 대상자를 위한 전문 인지건강프로그램과 일시 보호 서비스를 제공합니다.",
        "benefit_amount": "무료 (주 2회, 하루 3시간)",
        "benefit_type": "치료 프로그램",
        "application_method": "치매안심센터 방문 또는 전화 상담",
        "required_documents": "치매진단서, 신분증, 가족관계서류",
        "contact_info": "남해군 치매안심센터 055-860-8000",
        "service_duration": "주 2회 이용",
        "renewal_required": True
    },
    
    {
        "id": "gyeongnam_brain_health",
        "category_id": 1,  # 건강의료
        "service_name": "경상남도 노인 두뇌 건강 지원 서비스",
        "service_description": "만 65세 이상 어르신의 두뇌활동 촉진과 인지기능 퇴화 예방을 위한 두뇌활동교육 및 체험힐링 서비스를 제공합니다.",
        "benefit_amount": "월 이용료 160,000원 중 본인부담 16,000원 (정부지원 144,000원)",
        "benefit_type": "인지 재활 서비스",
        "application_method": "주소지 읍·면 행정복지센터 방문 또는 전화 상담",
        "required_documents": "신분증, 건강보험료 납부확인서, 소득증명서",
        "contact_info": "남해군청 노인복지과 055-860-8300",
        "service_duration": "12개월",
        "renewal_required": False
    }
]

# 복지 카테고리 정의
WELFARE_CATEGORIES = {
    1: "건강의료",
    2: "생활지원", 
    3: "경제지원",
    4: "사회참여",
    5: "주거지원"
}

def init_welfare_database():
    """복지 데이터베이스 초기화"""
    
    with app.app_context():
        try:
            # 테이블 생성
            db.create_all()
            print("✅ 데이터베이스 테이블 생성 완료")
            
            # 기존 데이터 삭제
            WelfareService.query.delete()
            db.session.commit()
            print("✅ 기존 복지 데이터 삭제 완료")
            
            # 새로운 복지 서비스 데이터 추가
            added_count = 0
            for service_data in WELFARE_SERVICES:
                service = WelfareService(**service_data)
                db.session.add(service)
                added_count += 1
                
                print(f"📋 추가됨: {service_data['service_name']}")
            
            # 변경사항 커밋
            db.session.commit()
            print(f"\n✅ 총 {added_count}개의 복지 서비스 데이터가 추가되었습니다.")
            
            # 데이터 검증
            verify_data()
            
        except Exception as e:
            print(f"❌ 데이터베이스 초기화 중 오류 발생: {str(e)}")
            db.session.rollback()
            return False
    
    return True

def verify_data():
    """데이터 검증"""
    print("\n🔍 데이터 검증 시작...")
    
    # 카테고리별 통계
    category_stats = {}
    for category_id, category_name in WELFARE_CATEGORIES.items():
        count = WelfareService.query.filter_by(category_id=category_id).count()
        category_stats[category_name] = count
        print(f"   {category_name}: {count}개")
    
    # 전체 통계
    total_count = WelfareService.query.count()
    active_count = WelfareService.query.filter_by(is_active=True).count()
    
    print(f"\n📊 데이터 통계:")
    print(f"   전체 복지 서비스: {total_count}개")
    print(f"   활성 서비스: {active_count}개")
    print(f"   비활성 서비스: {total_count - active_count}개")
    
    # 필수 필드 검증
    print(f"\n✅ 필수 필드 검증:")
    services_with_missing_fields = []
    
    for service in WelfareService.query.all():
        missing_fields = []
        if not service.service_name:
            missing_fields.append("service_name")
        if not service.service_description:
            missing_fields.append("service_description")
        if not service.benefit_amount:
            missing_fields.append("benefit_amount")
        if not service.contact_info:
            missing_fields.append("contact_info")
        
        if missing_fields:
            services_with_missing_fields.append({
                "service": service.service_name,
                "missing": missing_fields
            })
    
    if services_with_missing_fields:
        print(f"   ⚠️  {len(services_with_missing_fields)}개 서비스에 누락된 필드가 있습니다:")
        for item in services_with_missing_fields:
            print(f"      - {item['service']}: {', '.join(item['missing'])}")
    else:
        print("   ✅ 모든 서비스가 필수 필드를 포함하고 있습니다.")

def export_welfare_data():
    """복지 데이터를 JSON 파일로 내보내기"""
    print("\n📤 복지 데이터 내보내기...")
    
    try:
        services = WelfareService.query.all()
        export_data = []
        
        for service in services:
            service_dict = {
                "id": service.id,
                "category_id": service.category_id,
                "category_name": WELFARE_CATEGORIES.get(service.category_id, "기타"),
                "service_name": service.service_name,
                "service_description": service.service_description,
                "benefit_amount": service.benefit_amount,
                "benefit_type": service.benefit_type,
                "application_method": service.application_method,
                "required_documents": service.required_documents,
                "contact_info": service.contact_info,
                "application_url": service.application_url,
                "service_duration": service.service_duration,
                "renewal_required": service.renewal_required,
                "is_active": service.is_active,
                "created_at": service.created_at.isoformat() if service.created_at else None
            }
            export_data.append(service_dict)
        
        # JSON 파일로 저장
        with open('welfare_services.json', 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {len(export_data)}개 복지 서비스 데이터가 'welfare_services.json'에 저장되었습니다.")
        
    except Exception as e:
        print(f"❌ 데이터 내보내기 중 오류 발생: {str(e)}")

def show_menu():
    """메인 메뉴 표시"""
    print("\n" + "="*50)
    print("🏛️  남해군 노인 복지 추천 시스템 - 데이터 관리")
    print("="*50)
    print("1. 복지 데이터베이스 초기화")
    print("2. 복지 데이터 검증")
    print("3. 복지 데이터 JSON 내보내기")
    print("4. 복지 서비스 목록 조회")
    print("5. 종료")
    print("="*50)

def show_welfare_list():
    """복지 서비스 목록 조회"""
    print("\n📋 복지 서비스 목록:")
    print("-" * 60)
    
    for category_id, category_name in WELFARE_CATEGORIES.items():
        services = WelfareService.query.filter_by(category_id=category_id).all()
        
        if services:
            print(f"\n🏷️  {category_name} ({len(services)}개)")
            for i, service in enumerate(services, 1):
                status = "✅" if service.is_active else "❌"
                print(f"   {i}. {status} {service.service_name}")
                print(f"      💰 {service.benefit_amount}")
                print(f"      📞 {service.contact_info}")
                print()

def main():
    """메인 함수"""
    print("🚀 남해군 노인 복지 추천 시스템 데이터 관리 도구")
    print("복지 자료를 기반으로 데이터베이스를 초기화합니다.")
    
    while True:
        show_menu()
        choice = input("\n선택하세요 (1-5): ").strip()
        
        if choice == '1':
            print("\n📊 복지 데이터베이스 초기화를 시작합니다...")
            if init_welfare_database():
                print("✅ 복지 데이터베이스 초기화가 완료되었습니다!")
            else:
                print("❌ 복지 데이터베이스 초기화에 실패했습니다.")
        
        elif choice == '2':
            print("\n🔍 복지 데이터 검증을 시작합니다...")
            with app.app_context():
                verify_data()
        
        elif choice == '3':
            print("\n📤 복지 데이터 JSON 내보내기를 시작합니다...")
            with app.app_context():
                export_welfare_data()
        
        elif choice == '4':
            print("\n📋 복지 서비스 목록을 조회합니다...")
            with app.app_context():
                show_welfare_list()
        
        elif choice == '5':
            print("\n👋 프로그램을 종료합니다.")
            break
        
        else:
            print("\n❌ 잘못된 선택입니다. 1-5 중에서 선택해주세요.")
        
        input("\n계속하려면 Enter를 누르세요...")

if __name__ == "__main__":
    main() 
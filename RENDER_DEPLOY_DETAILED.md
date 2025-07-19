# 🌍 Render 배포 - 상세 가이드

## 📍 현재 상황
- **파일 위치**: `C:\Users\pc\welfare-platform`
- **총 파일**: 웹사이트 완성 (app.py, templates, static 등)
- **목표**: 전세계에서 접속 가능한 웹사이트 배포

---

## 🔥 2단계: Render 배포 (상세 과정)

### **Step 1: Render 사이트 접속**
1. 브라우저에서 **https://render.com** 접속
2. 우측 상단 **"Get Started for Free"** 클릭
3. **"Sign up with GitHub"** 선택 (GitHub 계정으로 가입)

### **Step 2: 새 웹서비스 생성**
1. 로그인 후 대시보드에서 **"New +"** 버튼 클릭
2. 드롭다운 메뉴에서 **"Web Service"** 선택
3. **"Build and deploy from a Git repository"** 선택

### **Step 3: GitHub 저장소 연결**
1. **"Connect account"** 클릭하여 GitHub 계정 연결
2. 저장소 목록에서 **"welfare-namhae-website"** 찾기
3. 해당 저장소 옆의 **"Connect"** 버튼 클릭

### **Step 4: 배포 설정 (중요!)**

#### 📋 기본 설정
```
Name: welfare-namhae
Region: Oregon (US West) 또는 Singapore (아시아 가까움)
Branch: main
Root Directory: (비워둠)
Runtime: Python 3
```

#### 🔧 빌드 설정
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
```

#### 🌐 환경 변수 설정
**"Advanced" 섹션 클릭 후 환경 변수 추가:**

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | `welfare-namhae-secret-2024` |
| `PORT` | `10000` |
| `DATABASE_URL` | `sqlite:///welfare.db` |
| `PYTHONPATH` | `/opt/render/project/src` |

### **Step 5: 플랜 선택**
- **Free Plan** 선택 (월 750시간, SSL 인증서 포함)
- **Custom Domain** (선택사항): 나중에 도메인 연결 가능

### **Step 6: 배포 시작**
1. **"Create Web Service"** 클릭
2. 자동으로 배포 시작 (3-5분 소요)
3. 실시간 로그 확인 가능

### **Step 7: 배포 완료 확인**

#### ✅ 성공 시 표시되는 것들:
- **상태**: "Live" (초록색)
- **URL**: `https://welfare-namhae.onrender.com`
- **SSL**: 자동 활성화 (🔒 표시)

#### 🔧 문제 해결
**빌드 실패 시:**
```bash
# 로그에서 확인할 내용
- Python 버전 호환성
- requirements.txt 패키지 설치 오류
- 포트 설정 문제
```

**시작 실패 시:**
```bash
# 확인할 설정
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
Port: 환경 변수에 PORT=10000 설정
```

---

## 🎯 배포 후 테스트

### **접속 테스트**
1. **PC에서**: `https://welfare-namhae.onrender.com`
2. **모바일에서**: 같은 URL로 접속
3. **해외에서**: VPN으로 다른 국가에서 테스트

### **기능 테스트**
- ✅ 메인 페이지 로딩
- ✅ 설문조사 4단계 진행
- ✅ AI 복지 추천 결과
- ✅ 음성 안내 기능
- ✅ 접근성 기능 (글자 크기, 고대비)

---

## 📱 모니터링 & 관리

### **Render 대시보드에서:**
- **실시간 방문자 수** 확인
- **서버 상태** 모니터링
- **로그** 실시간 확인
- **자동 재시작** 설정

### **성능 최적화:**
- **CDN**: 자동으로 전세계 배포
- **캐싱**: 정적 파일 자동 캐싱
- **압축**: gzip 자동 적용

---

## 🚀 고급 설정 (선택사항)

### **커스텀 도메인 연결**
1. 도메인 구매 (예: namhae-welfare.com)
2. Render에서 Custom Domain 설정
3. DNS 설정 변경

### **데이터베이스 업그레이드**
- **PostgreSQL**: 더 많은 사용자 지원
- **Redis**: 세션 관리 최적화

---

## 📞 지원 & 문제 해결

### **Render 지원:**
- **문서**: https://render.com/docs
- **커뮤니티**: Discord, 포럼
- **이메일 지원**: Free 플랜도 지원

### **일반적인 문제:**
1. **느린 로딩**: Free 플랜은 비활성 시 슬립 모드
2. **월 시간 초과**: 750시간 = 31일 * 24시간
3. **업로드 제한**: 100MB (현재 프로젝트는 < 1MB)

---

## 🎉 완료 후 결과

**🌐 전세계 접속 가능한 웹사이트:**
- **URL**: `https://welfare-namhae.onrender.com`
- **SSL 보안**: ✅ 자동 적용
- **모바일 최적화**: ✅ 반응형 디자인
- **접근성**: ✅ WCAG 2.1 AA 준수
- **AI 추천**: ✅ 개인 맞춤 복지 서비스

**📊 예상 성능:**
- **로딩 속도**: 1-3초
- **동시 사용자**: 100명+
- **가용성**: 99.9%
- **전세계 CDN**: 자동 적용 
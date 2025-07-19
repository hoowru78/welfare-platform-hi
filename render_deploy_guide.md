# 🌍 남해군 복지 추천 웹사이트 - Render 배포 가이드

## 1단계: GitHub에 코드 업로드

### 방법 A: GitHub Desktop 사용 (쉬움)
1. GitHub Desktop 다운로드: https://desktop.github.com
2. 새 저장소 생성: `welfare-namhae-website`
3. 이 폴더 전체를 드래그 앤 드롭
4. "Commit to main" → "Publish repository"

### 방법 B: 웹에서 직접 업로드
1. GitHub.com 접속 → "New repository"
2. 저장소 이름: `welfare-namhae-website`
3. "uploading an existing file" 클릭
4. 모든 파일을 드래그 앤 드롭

## 2단계: Render에서 배포

### 🔗 render.com 접속
1. https://render.com 접속
2. GitHub 계정으로 로그인
3. "New +" → "Web Service" 클릭

### ⚙️ 설정
```
Repository: welfare-namhae-website
Branch: main
Root Directory: (비워둠)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### 🌐 환경 변수 설정
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///welfare.db
```

## 3단계: 완료! 🎉

**배포 시간**: 약 3-5분
**무료 도메인**: `your-site-name.onrender.com`
**SSL 인증서**: 자동 생성
**전세계 접속**: 가능

## 📱 주요 기능
- ✅ 4단계 설문조사 시스템
- ✅ AI 기반 복지 추천
- ✅ 음성 안내 (접근성)
- ✅ 글자 크기 조절
- ✅ 고대비 모드
- ✅ 모바일 최적화
- ✅ 인쇄/저장 기능

## 🔧 문제 해결
- **빌드 실패**: requirements.txt 확인
- **시작 실패**: Procfile 확인
- **DB 오류**: 자동으로 SQLite 생성됨

---
**배포 후 접속 예시**: https://welfare-namhae.onrender.com 
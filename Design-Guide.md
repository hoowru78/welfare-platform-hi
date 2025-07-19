# Design Guide
## 남해군 노인 복지 추천 웹사이트 디자인 가이드

### 1. 디자인 시스템 개요

#### 1.1 디자인 철학
- **접근성 우선**: 모든 사용자가 쉽게 이용할 수 있는 유니버설 디자인
- **단순함**: 복잡한 요소를 제거하고 핵심 기능에 집중
- **친근함**: 고령층이 친숙하게 느낄 수 있는 따뜻한 디자인
- **신뢰성**: 공공 서비스답게 안정적이고 신뢰할 수 있는 디자인

#### 1.2 타겟 사용자 특성
- **연령**: 65세 이상 고령층
- **디지털 문해력**: 낮음 (기본적인 스마트폰 사용 가능)
- **신체적 특성**: 시각/청각 능력 저하 가능성
- **인지적 특성**: 복잡한 UI에 대한 이해도 제한

### 2. 색상 체계 (Color System)

#### 2.1 기본 색상 팔레트

**Primary Color (주색상)**
```css
/* 남해군 상징색 기반 신뢰감 있는 블루 */
--primary-50: #eff6ff;    /* bg-blue-50 */
--primary-100: #dbeafe;   /* bg-blue-100 */
--primary-200: #bfdbfe;   /* bg-blue-200 */
--primary-300: #93c5fd;   /* bg-blue-300 */
--primary-400: #60a5fa;   /* bg-blue-400 */
--primary-500: #265DAB;   /* bg-blue-500 - 메인 색상 */
--primary-600: #1e40af;   /* bg-blue-600 */
--primary-700: #1d4ed8;   /* bg-blue-700 */
--primary-800: #1e3a8a;   /* bg-blue-800 */
--primary-900: #1e1f3a;   /* bg-blue-900 */
```

**Secondary Color (보조색상)**
```css
/* 부드럽고 편안한 느낌의 연한 블루 */
--secondary-50: #f8fafc;   /* bg-slate-50 */
--secondary-100: #E9F0FA;  /* 커스텀 색상 */
--secondary-200: #e2e8f0;  /* bg-slate-200 */
--secondary-300: #cbd5e1;  /* bg-slate-300 */
--secondary-400: #94a3b8;  /* bg-slate-400 */
--secondary-500: #64748b;  /* bg-slate-500 */
--secondary-600: #475569;  /* bg-slate-600 */
--secondary-700: #334155;  /* bg-slate-700 */
--secondary-800: #1e293b;  /* bg-slate-800 */
--secondary-900: #0f172a;  /* bg-slate-900 */
```

**Accent Color (강조색상)**
```css
/* 따뜻하고 친근한 느낌의 노란색 */
--accent-50: #fefce8;     /* bg-yellow-50 */
--accent-100: #fef3c7;    /* bg-yellow-100 */
--accent-200: #fed7aa;    /* bg-yellow-200 */
--accent-300: #fdba74;    /* bg-yellow-300 */
--accent-400: #FFE66D;    /* 커스텀 색상 - 메인 강조 */
--accent-500: #f59e0b;    /* bg-yellow-500 */
--accent-600: #d97706;    /* bg-yellow-600 */
--accent-700: #b45309;    /* bg-yellow-700 */
--accent-800: #92400e;    /* bg-yellow-800 */
--accent-900: #78350f;    /* bg-yellow-900 */
```

**Neutral Color (중성색상)**
```css
/* 배경 및 텍스트용 중성색 */
--neutral-50: #F9F9F9;    /* 커스텀 색상 - 메인 배경 */
--neutral-100: #f3f4f6;   /* bg-gray-100 */
--neutral-200: #e5e7eb;   /* bg-gray-200 */
--neutral-300: #d1d5db;   /* bg-gray-300 */
--neutral-400: #9ca3af;   /* bg-gray-400 */
--neutral-500: #6b7280;   /* bg-gray-500 */
--neutral-600: #4A4A4A;   /* 커스텀 색상 - 메인 텍스트 */
--neutral-700: #374151;   /* bg-gray-700 */
--neutral-800: #1f2937;   /* bg-gray-800 */
--neutral-900: #111827;   /* bg-gray-900 */
```

#### 2.2 상태별 색상

**성공 (Success)**
```css
--success-50: #f0fdf4;    /* bg-green-50 */
--success-100: #dcfce7;   /* bg-green-100 */
--success-500: #10b981;   /* bg-green-500 */
--success-600: #059669;   /* bg-green-600 */
--success-700: #047857;   /* bg-green-700 */
```

**주의 (Warning)**
```css
--warning-50: #fffbeb;    /* bg-amber-50 */
--warning-100: #fef3c7;   /* bg-amber-100 */
--warning-500: #f59e0b;   /* bg-amber-500 */
--warning-600: #d97706;   /* bg-amber-600 */
--warning-700: #b45309;   /* bg-amber-700 */
```

**오류 (Error)**
```css
--error-50: #fef2f2;      /* bg-red-50 */
--error-100: #fee2e2;     /* bg-red-100 */
--error-500: #ef4444;     /* bg-red-500 */
--error-600: #dc2626;     /* bg-red-600 */
--error-700: #b91c1c;     /* bg-red-700 */
```

#### 2.3 고대비 모드 색상
```css
/* 고대비 모드용 색상 */
--high-contrast-bg: #000000;      /* 검은색 배경 */
--high-contrast-text: #ffffff;    /* 흰색 텍스트 */
--high-contrast-primary: #ffff00; /* 노란색 강조 */
--high-contrast-border: #ffffff;  /* 흰색 테두리 */
```

### 3. 타이포그래피 (Typography)

#### 3.1 폰트 체계
```css
/* 기본 폰트 패밀리 */
font-family: 'Noto Sans KR', 'Malgun Gothic', '맑은 고딕', 'Apple SD Gothic Neo', sans-serif;

/* 폰트 가중치 */
--font-light: 300;
--font-regular: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

#### 3.2 폰트 크기 계층
```css
/* 기본 폰트 크기 (18px) */
--text-xs: 0.75rem;     /* 12px */
--text-sm: 0.875rem;    /* 14px */
--text-base: 1.125rem;  /* 18px - 기본 크기 */
--text-lg: 1.25rem;     /* 20px */
--text-xl: 1.5rem;      /* 24px */
--text-2xl: 1.75rem;    /* 28px */
--text-3xl: 2rem;       /* 32px */
--text-4xl: 2.5rem;     /* 40px */
--text-5xl: 3rem;       /* 48px */
```

#### 3.3 글자 크기 조절 단계
```css
/* 기본 모드 */
.text-size-normal {
    font-size: 1.125rem;  /* 18px */
    line-height: 1.7;
}

/* 중간 크기 */
.text-size-medium {
    font-size: 1.375rem;  /* 22px */
    line-height: 1.6;
}

/* 큰 크기 */
.text-size-large {
    font-size: 1.5rem;    /* 24px */
    line-height: 1.5;
}
```

#### 3.4 줄 간격 (Line Height)
```css
--leading-none: 1;
--leading-tight: 1.25;
--leading-snug: 1.375;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
--leading-loose: 2;
```

### 4. 레이아웃 시스템

#### 4.1 그리드 시스템
```css
/* 컨테이너 */
.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

/* 그리드 */
.grid {
    display: grid;
    gap: 1rem;
}

.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
```

#### 4.2 플렉스 시스템
```css
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-row { flex-direction: row; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.items-center { align-items: center; }
.items-start { align-items: flex-start; }
```

#### 4.3 간격 시스템
```css
/* 패딩 */
.p-0 { padding: 0; }
.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-3 { padding: 0.75rem; }
.p-4 { padding: 1rem; }
.p-6 { padding: 1.5rem; }
.p-8 { padding: 2rem; }
.p-12 { padding: 3rem; }

/* 마진 */
.m-0 { margin: 0; }
.m-1 { margin: 0.25rem; }
.m-2 { margin: 0.5rem; }
.m-3 { margin: 0.75rem; }
.m-4 { margin: 1rem; }
.m-6 { margin: 1.5rem; }
.m-8 { margin: 2rem; }
.m-12 { margin: 3rem; }

/* 간격 */
.gap-1 { gap: 0.25rem; }
.gap-2 { gap: 0.5rem; }
.gap-3 { gap: 0.75rem; }
.gap-4 { gap: 1rem; }
.gap-6 { gap: 1.5rem; }
.gap-8 { gap: 2rem; }
```

### 5. 컴포넌트 디자인

#### 5.1 버튼 컴포넌트
```css
/* 기본 버튼 */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 44px;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 600;
    font-size: 1.125rem;
    line-height: 1.5;
    transition: all 0.2s;
    cursor: pointer;
    border: none;
    text-decoration: none;
}

/* 주요 버튼 */
.btn-primary {
    background-color: var(--primary-500);
    color: white;
}

.btn-primary:hover {
    background-color: var(--primary-600);
    transform: translateY(-1px);
}

.btn-primary:focus {
    outline: 2px solid var(--primary-300);
    outline-offset: 2px;
}

/* 보조 버튼 */
.btn-secondary {
    background-color: var(--secondary-100);
    color: var(--primary-600);
    border: 1px solid var(--secondary-300);
}

.btn-secondary:hover {
    background-color: var(--secondary-200);
    border-color: var(--secondary-400);
}

/* 큰 버튼 */
.btn-large {
    min-height: 56px;
    padding: 1rem 2rem;
    font-size: 1.25rem;
}

/* 전체 너비 버튼 */
.btn-full {
    width: 100%;
}
```

#### 5.2 카드 컴포넌트
```css
.card {
    background-color: white;
    border-radius: 0.75rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    border: 1px solid var(--neutral-200);
    overflow: hidden;
}

.card-header {
    padding: 1.5rem;
    border-bottom: 1px solid var(--neutral-200);
}

.card-body {
    padding: 1.5rem;
}

.card-footer {
    padding: 1.5rem;
    border-top: 1px solid var(--neutral-200);
    background-color: var(--neutral-50);
}
```

#### 5.3 폼 컴포넌트
```css
/* 입력 필드 */
.input {
    width: 100%;
    min-height: 48px;
    padding: 0.75rem 1rem;
    border: 2px solid var(--neutral-300);
    border-radius: 0.5rem;
    font-size: 1.125rem;
    line-height: 1.5;
    transition: border-color 0.2s;
}

.input:focus {
    outline: none;
    border-color: var(--primary-500);
    box-shadow: 0 0 0 3px rgba(37, 93, 171, 0.1);
}

/* 레이블 */
.label {
    display: block;
    margin-bottom: 0.5rem;
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--neutral-700);
}

/* 라디오 버튼 */
.radio-group {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.radio-item {
    display: flex;
    align-items: center;
    padding: 0.75rem;
    border: 2px solid var(--neutral-300);
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.2s;
}

.radio-item:hover {
    border-color: var(--primary-400);
    background-color: var(--primary-50);
}

.radio-item.selected {
    border-color: var(--primary-500);
    background-color: var(--primary-100);
}

.radio-input {
    width: 20px;
    height: 20px;
    margin-right: 0.75rem;
}
```

#### 5.4 진행 표시기
```css
.progress-bar {
    width: 100%;
    height: 8px;
    background-color: var(--neutral-200);
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background-color: var(--primary-500);
    transition: width 0.3s ease;
}

.step-indicator {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
}

.step {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
}

.step-number {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: var(--neutral-300);
    color: var(--neutral-600);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.step-number.active {
    background-color: var(--primary-500);
    color: white;
}

.step-number.completed {
    background-color: var(--success-500);
    color: white;
}

.step-title {
    font-size: 0.875rem;
    color: var(--neutral-600);
    text-align: center;
}
```

### 6. 페이지별 구성요소

#### 6.1 홈페이지 레이아웃
```html
<div class="min-h-screen bg-neutral-50">
    <!-- 헤더 -->
    <header class="bg-white shadow-sm border-b border-neutral-200">
        <div class="container mx-auto px-4 py-4">
            <div class="flex justify-between items-center">
                <div class="flex items-center gap-3">
                    <img src="/logo.png" alt="남해군 로고" class="h-12 w-12">
                    <h1 class="text-2xl font-bold text-neutral-800">
                        남해군 노인 복지 추천
                    </h1>
                </div>
                <div class="flex items-center gap-2">
                    <button class="btn-accessibility">가</button>
                    <button class="btn-accessibility">🔊</button>
                    <button class="btn-accessibility">🌓</button>
                </div>
            </div>
        </div>
    </header>

    <!-- 메인 콘텐츠 -->
    <main class="container mx-auto px-4 py-8">
        <div class="max-w-4xl mx-auto">
            <!-- 서비스 소개 -->
            <section class="text-center mb-12">
                <h2 class="text-4xl font-bold text-neutral-800 mb-4">
                    어르신 맞춤형 복지 혜택을 찾아드려요
                </h2>
                <p class="text-xl text-neutral-600 leading-relaxed">
                    간단한 설문을 통해 어르신께 가장 적합한 복지 혜택을 추천해드립니다
                </p>
            </section>

            <!-- 이용 방법 -->
            <section class="mb-12">
                <h3 class="text-2xl font-bold text-center mb-8">이용 방법</h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="card text-center">
                        <div class="card-body">
                            <div class="text-4xl mb-4">📝</div>
                            <h4 class="text-xl font-semibold mb-2">1. 설문 작성</h4>
                            <p class="text-neutral-600">건강, 생활, 경제 상황에 대한 간단한 질문에 답하세요</p>
                        </div>
                    </div>
                    <div class="card text-center">
                        <div class="card-body">
                            <div class="text-4xl mb-4">🤖</div>
                            <h4 class="text-xl font-semibold mb-2">2. AI 분석</h4>
                            <p class="text-neutral-600">인공지능이 어르신의 상황을 분석해 맞춤형 복지를 찾아드려요</p>
                        </div>
                    </div>
                    <div class="card text-center">
                        <div class="card-body">
                            <div class="text-4xl mb-4">🎯</div>
                            <h4 class="text-xl font-semibold mb-2">3. 추천 결과</h4>
                            <p class="text-neutral-600">신청 가능한 복지 혜택과 신청 방법을 안내해드려요</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 시작하기 버튼 -->
            <section class="text-center mb-8">
                <button class="btn btn-primary btn-large">
                    <span class="text-2xl mr-2">▶️</span>
                    설문 시작하기
                </button>
            </section>

            <!-- 기존 결과 조회 -->
            <section class="text-center">
                <a href="/lookup" class="text-primary-600 hover:text-primary-700 text-lg">
                    기존 결과 조회하기 →
                </a>
            </section>
        </div>
    </main>

    <!-- 푸터 -->
    <footer class="bg-neutral-800 text-white mt-16">
        <div class="container mx-auto px-4 py-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div>
                    <h4 class="text-lg font-semibold mb-4">남해군청</h4>
                    <p class="text-neutral-300">경상남도 남해군 남해읍 홍현길 35</p>
                    <p class="text-neutral-300">전화: 055-860-8000</p>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">문의 및 도움</h4>
                    <p class="text-neutral-300">복지정책과: 055-860-8300</p>
                    <p class="text-neutral-300">기술지원: 055-860-8100</p>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">이용 안내</h4>
                    <a href="/help" class="text-neutral-300 hover:text-white block">사용 방법</a>
                    <a href="/privacy" class="text-neutral-300 hover:text-white block">개인정보 처리방침</a>
                </div>
            </div>
        </div>
    </footer>
</div>
```

#### 6.2 설문 페이지 레이아웃
```html
<div class="min-h-screen bg-neutral-50">
    <!-- 진행 표시기 -->
    <div class="bg-white shadow-sm border-b border-neutral-200">
        <div class="container mx-auto px-4 py-6">
            <div class="step-indicator">
                <div class="step">
                    <div class="step-number completed">1</div>
                    <div class="step-title">건강 상태</div>
                </div>
                <div class="step">
                    <div class="step-number active">2</div>
                    <div class="step-title">생활 환경</div>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <div class="step-title">경제 상황</div>
                </div>
                <div class="step">
                    <div class="step-number">4</div>
                    <div class="step-title">사회 관계</div>
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 50%"></div>
            </div>
        </div>
    </div>

    <!-- 설문 콘텐츠 -->
    <main class="container mx-auto px-4 py-8">
        <div class="max-w-3xl mx-auto">
            <div class="card">
                <div class="card-header">
                    <h2 class="text-2xl font-bold text-neutral-800">생활 환경에 대해 알려주세요</h2>
                    <p class="text-neutral-600 mt-2">어르신의 현재 생활 환경을 파악하여 적절한 복지 혜택을 추천해드립니다</p>
                </div>
                <div class="card-body">
                    <div class="space-y-8">
                        <!-- 질문 1 -->
                        <div class="question-group">
                            <label class="label flex items-center gap-2">
                                현재 거주 형태는 어떻게 되나요?
                                <button class="btn-voice" aria-label="음성 안내">🔊</button>
                            </label>
                            <div class="radio-group">
                                <label class="radio-item">
                                    <input type="radio" name="housing" value="own" class="radio-input">
                                    <span>자가 (내 집)</span>
                                </label>
                                <label class="radio-item">
                                    <input type="radio" name="housing" value="rent" class="radio-input">
                                    <span>임대 (전세/월세)</span>
                                </label>
                                <label class="radio-item">
                                    <input type="radio" name="housing" value="family" class="radio-input">
                                    <span>가족과 함께 거주</span>
                                </label>
                                <label class="radio-item">
                                    <input type="radio" name="housing" value="facility" class="radio-input">
                                    <span>시설 거주</span>
                                </label>
                            </div>
                        </div>

                        <!-- 질문 2 -->
                        <div class="question-group">
                            <label class="label flex items-center gap-2">
                                혼자 거주하고 계신가요?
                                <button class="btn-voice" aria-label="음성 안내">🔊</button>
                            </label>
                            <div class="radio-group">
                                <label class="radio-item">
                                    <input type="radio" name="living_alone" value="alone" class="radio-input">
                                    <span>혼자 거주</span>
                                </label>
                                <label class="radio-item">
                                    <input type="radio" name="living_alone" value="spouse" class="radio-input">
                                    <span>배우자와 함께</span>
                                </label>
                                <label class="radio-item">
                                    <input type="radio" name="living_alone" value="family" class="radio-input">
                                    <span>가족과 함께</span>
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- 하단 고정 버튼 -->
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-neutral-200 p-4 shadow-lg">
        <div class="container mx-auto max-w-3xl">
            <div class="flex justify-between gap-4">
                <button class="btn btn-secondary flex-1">
                    ← 이전 단계
                </button>
                <button class="btn btn-primary flex-1">
                    다음 단계 →
                </button>
            </div>
        </div>
    </div>
</div>
```

#### 6.3 결과 페이지 레이아웃
```html
<div class="min-h-screen bg-neutral-50">
    <!-- 결과 헤더 -->
    <div class="bg-gradient-to-r from-primary-500 to-primary-600 text-white">
        <div class="container mx-auto px-4 py-12">
            <div class="text-center">
                <div class="text-6xl mb-4">🎉</div>
                <h1 class="text-3xl font-bold mb-2">복지 혜택 추천 결과</h1>
                <p class="text-primary-100 text-lg">어르신께 맞는 3가지 복지 혜택을 찾았습니다</p>
            </div>
        </div>
    </div>

    <!-- 추천 결과 -->
    <main class="container mx-auto px-4 py-8">
        <div class="max-w-4xl mx-auto">
            <!-- 추천 카드 목록 -->
            <div class="space-y-6">
                <!-- 추천 카드 1 -->
                <div class="card border-l-4 border-l-primary-500">
                    <div class="card-body">
                        <div class="flex items-start justify-between">
                            <div class="flex-1">
                                <div class="flex items-center gap-2 mb-3">
                                    <span class="bg-primary-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                                        1순위
                                    </span>
                                    <span class="bg-success-100 text-success-800 px-3 py-1 rounded-full text-sm font-semibold">
                                        의료비 지원
                                    </span>
                                </div>
                                <h3 class="text-xl font-bold text-neutral-800 mb-2">
                                    노인 의료비 지원 서비스
                                </h3>
                                <p class="text-neutral-600 mb-4">
                                    65세 이상 어르신의 의료비 부담을 줄여드리는 서비스입니다. 
                                    월 최대 30만원까지 지원받으실 수 있습니다.
                                </p>
                                <div class="flex items-center gap-4 text-sm text-neutral-500">
                                    <span>💰 월 최대 30만원</span>
                                    <span>📅 연중 신청 가능</span>
                                    <span>🏥 모든 의료기관 적용</span>
                                </div>
                            </div>
                            <div class="ml-4">
                                <div class="text-4xl">🏥</div>
                            </div>
                        </div>
                        <div class="mt-6 flex gap-3">
                            <button class="btn btn-primary">
                                신청 방법 보기
                            </button>
                            <button class="btn btn-secondary">
                                상세 정보
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 추천 카드 2 -->
                <div class="card border-l-4 border-l-accent-400">
                    <div class="card-body">
                        <div class="flex items-start justify-between">
                            <div class="flex-1">
                                <div class="flex items-center gap-2 mb-3">
                                    <span class="bg-accent-400 text-neutral-800 px-3 py-1 rounded-full text-sm font-semibold">
                                        2순위
                                    </span>
                                    <span class="bg-warning-100 text-warning-800 px-3 py-1 rounded-full text-sm font-semibold">
                                        생활 지원
                                    </span>
                                </div>
                                <h3 class="text-xl font-bold text-neutral-800 mb-2">
                                    재가 돌봄 서비스
                                </h3>
                                <p class="text-neutral-600 mb-4">
                                    일상생활 지원이 필요한 어르신을 위한 방문 돌봄 서비스입니다. 
                                    전문 돌봄 인력이 정기적으로 방문하여 도움을 드립니다.
                                </p>
                                <div class="flex items-center gap-4 text-sm text-neutral-500">
                                    <span>🏠 주 2회 방문</span>
                                    <span>👥 전문 돌봄 인력</span>
                                    <span>🆓 무료 서비스</span>
                                </div>
                            </div>
                            <div class="ml-4">
                                <div class="text-4xl">🏠</div>
                            </div>
                        </div>
                        <div class="mt-6 flex gap-3">
                            <button class="btn btn-primary">
                                신청 방법 보기
                            </button>
                            <button class="btn btn-secondary">
                                상세 정보
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 추천 카드 3 -->
                <div class="card border-l-4 border-l-success-500">
                    <div class="card-body">
                        <div class="flex items-start justify-between">
                            <div class="flex-1">
                                <div class="flex items-center gap-2 mb-3">
                                    <span class="bg-success-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                                        3순위
                                    </span>
                                    <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
                                        사회 참여
                                    </span>
                                </div>
                                <h3 class="text-xl font-bold text-neutral-800 mb-2">
                                    경로당 프로그램
                                </h3>
                                <p class="text-neutral-600 mb-4">
                                    지역 경로당에서 진행하는 다양한 문화 활동과 건강 프로그램에 참여하실 수 있습니다.
                                </p>
                                <div class="flex items-center gap-4 text-sm text-neutral-500">
                                    <span>🎨 문화 활동</span>
                                    <span>💪 건강 프로그램</span>
                                    <span>👥 사회 참여</span>
                                </div>
                            </div>
                            <div class="ml-4">
                                <div class="text-4xl">🎭</div>
                            </div>
                        </div>
                        <div class="mt-6 flex gap-3">
                            <button class="btn btn-primary">
                                신청 방법 보기
                            </button>
                            <button class="btn btn-secondary">
                                상세 정보
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 하단 액션 -->
            <div class="mt-12 bg-white rounded-lg p-6 shadow-sm">
                <div class="text-center">
                    <h3 class="text-lg font-semibold mb-4">결과를 저장하고 나중에 확인하세요</h3>
                    <div class="flex justify-center gap-4">
                        <button class="btn btn-primary">
                            📱 결과 저장하기
                        </button>
                        <button class="btn btn-secondary">
                            🔄 다시 설문하기
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </main>
</div>
```

### 7. 상호작용 패턴

#### 7.1 버튼 상호작용
```css
/* 버튼 호버 효과 */
.btn {
    transition: all 0.2s ease;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn:active {
    transform: translateY(0);
}

/* 포커스 상태 */
.btn:focus {
    outline: 2px solid var(--primary-300);
    outline-offset: 2px;
}
```

#### 7.2 카드 상호작용
```css
.card {
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.card-interactive {
    cursor: pointer;
}

.card-interactive:hover {
    border-color: var(--primary-300);
}
```

#### 7.3 로딩 상태
```css
.loading {
    position: relative;
    opacity: 0.7;
    pointer-events: none;
}

.loading::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 24px;
    height: 24px;
    border: 2px solid var(--primary-200);
    border-top: 2px solid var(--primary-500);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    transform: translate(-50%, -50%);
}

@keyframes spin {
    0% { transform: translate(-50%, -50%) rotate(0deg); }
    100% { transform: translate(-50%, -50%) rotate(360deg); }
}
```

### 8. 반응형 디자인

#### 8.1 브레이크포인트
```css
/* Mobile First 접근 */
@media (min-width: 768px) {
    /* 태블릿 */
    .container {
        padding: 0 2rem;
    }
    
    .grid-cols-md-2 {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    
    .text-md-left {
        text-align: left;
    }
}

@media (min-width: 1024px) {
    /* 데스크톱 */
    .container {
        padding: 0 3rem;
    }
    
    .grid-cols-lg-3 {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
    
    .flex-lg-row {
        flex-direction: row;
    }
}

@media (min-width: 1280px) {
    /* 대형 화면 */
    .container {
        max-width: 1200px;
    }
}
```

#### 8.2 모바일 최적화
```css
/* 모바일 터치 타겟 */
@media (max-width: 767px) {
    .btn {
        min-height: 48px;
        padding: 0.875rem 1.5rem;
    }
    
    .radio-item {
        min-height: 56px;
        padding: 1rem;
    }
    
    .card-body {
        padding: 1rem;
    }
    
    /* 모바일 타이포그래피 */
    .text-4xl {
        font-size: 2rem;
    }
    
    .text-3xl {
        font-size: 1.75rem;
    }
}
```

### 9. 접근성 준수사항

#### 9.1 키보드 내비게이션
```css
/* 포커스 표시 */
*:focus {
    outline: 2px solid var(--primary-500);
    outline-offset: 2px;
}

/* Skip link */
.skip-link {
    position: absolute;
    left: -9999px;
    top: -9999px;
    z-index: 999;
    padding: 0.5rem 1rem;
    background: var(--primary-500);
    color: white;
    text-decoration: none;
}

.skip-link:focus {
    left: 0;
    top: 0;
}

/* 포커스 트랩 */
.modal {
    isolation: isolate;
}
```

#### 9.2 스크린 리더 지원
```css
/* 스크린 리더 전용 텍스트 */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* 고대비 모드 */
@media (prefers-contrast: high) {
    .btn-primary {
        background-color: #000000;
        color: #ffffff;
        border: 2px solid #ffffff;
    }
    
    .card {
        border: 2px solid #000000;
    }
}
```

#### 9.3 색상 및 대비
```css
/* 색상 대비 확인 */
.text-primary { color: var(--primary-600); } /* 4.5:1 대비 */
.text-secondary { color: var(--neutral-600); } /* 4.5:1 대비 */
.text-muted { color: var(--neutral-500); } /* 4.5:1 대비 */

/* 링크 색상 */
a {
    color: var(--primary-600);
    text-decoration: underline;
}

a:hover {
    color: var(--primary-700);
}

a:visited {
    color: var(--primary-800);
}
```

### 10. 애니메이션 및 전환

#### 10.1 기본 전환 효과
```css
/* 페이지 전환 */
.page-transition {
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.3s ease;
}

.page-transition.active {
    opacity: 1;
    transform: translateY(0);
}

/* 스크롤 애니메이션 */
.fade-in {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.6s ease;
}

.fade-in.visible {
    opacity: 1;
    transform: translateY(0);
}
```

#### 10.2 접근성 고려 애니메이션
```css
/* 움직임 감소 설정 */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

---

**문서 작성일**: 2024년 1월  
**문서 버전**: v1.0  
**작성자**: 남해군 복지 추천 시스템 개발팀 
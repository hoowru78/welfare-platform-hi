// 전역 변수
let currentUser = null;
let currentSession = null;
let currentStep = 1;
let fontSizeLevel = 1; // 1: normal, 2: medium, 3: large
let isVoiceEnabled = false;
let isHighContrast = false;
let speechSynthesis = window.speechSynthesis;

// API 기본 URL - 환경에 따라 자동 설정
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:5000/api'
    : `${window.location.protocol}//${window.location.host}/api`;

// DOM 요소들
const userInfoModal = document.getElementById('user-info-modal');
const lookupModal = document.getElementById('lookup-modal');
const startSurveyBtn = document.getElementById('start-survey-btn');
const lookupResultsBtn = document.getElementById('lookup-results-btn');
const userInfoForm = document.getElementById('user-info-form');
const lookupForm = document.getElementById('lookup-form');
const cancelBtn = document.getElementById('cancel-btn');
const lookupCancelBtn = document.getElementById('lookup-cancel-btn');
const fontSizeBtn = document.getElementById('font-size-btn');
const voiceToggleBtn = document.getElementById('voice-toggle-btn');
const highContrastBtn = document.getElementById('high-contrast-btn');
const floatingVoiceBtn = document.getElementById('floating-voice-btn');
const mainBody = document.getElementById('main-body');

// 초기화
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    loadUserPreferences();
    
    // 페이지 로드 시 음성 안내
    if (isVoiceEnabled) {
        speak('남해군 노인 복지 추천 서비스에 오신 것을 환영합니다.');
    }
});

// 이벤트 리스너 초기화
function initializeEventListeners() {
    // 설문 시작 버튼
    startSurveyBtn.addEventListener('click', function() {
        showUserInfoModal();
    });
    
    // 결과 조회 버튼
    lookupResultsBtn.addEventListener('click', function() {
        showLookupModal();
    });
    
    // 사용자 정보 폼 제출
    userInfoForm.addEventListener('submit', function(e) {
        e.preventDefault();
        handleUserInfoSubmit();
    });
    
    // 결과 조회 폼 제출
    lookupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        handleLookupSubmit();
    });
    
    // 모달 닫기
    cancelBtn.addEventListener('click', hideUserInfoModal);
    lookupCancelBtn.addEventListener('click', hideLookupModal);
    
    // 접근성 버튼들
    fontSizeBtn.addEventListener('click', toggleFontSize);
    voiceToggleBtn.addEventListener('click', toggleVoice);
    highContrastBtn.addEventListener('click', toggleHighContrast);
    floatingVoiceBtn.addEventListener('click', toggleVoice);
    
    // 모달 배경 클릭 시 닫기
    userInfoModal.addEventListener('click', function(e) {
        if (e.target === userInfoModal) {
            hideUserInfoModal();
        }
    });
    
    lookupModal.addEventListener('click', function(e) {
        if (e.target === lookupModal) {
            hideLookupModal();
        }
    });
    
    // 키보드 접근성
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            hideUserInfoModal();
            hideLookupModal();
        }
    });
}

// 사용자 정보 모달 표시
function showUserInfoModal() {
    userInfoModal.classList.remove('hidden');
    document.getElementById('user-name').focus();
    
    if (isVoiceEnabled) {
        speak('기본 정보를 입력해주세요.');
    }
}

// 사용자 정보 모달 숨기기
function hideUserInfoModal() {
    userInfoModal.classList.add('hidden');
}

// 결과 조회 모달 표시
function showLookupModal() {
    lookupModal.classList.remove('hidden');
    document.getElementById('lookup-key').focus();
    
    if (isVoiceEnabled) {
        speak('조회 키를 입력해주세요.');
    }
}

// 결과 조회 모달 숨기기
function hideLookupModal() {
    lookupModal.classList.add('hidden');
}

// 사용자 정보 제출 처리
async function handleUserInfoSubmit() {
    const name = document.getElementById('user-name').value;
    const birthDate = document.getElementById('user-birth').value;
    const district = document.getElementById('user-district').value;
    const privacyAgree = document.getElementById('privacy-agree').checked;
    
    if (!name || !birthDate || !district || !privacyAgree) {
        alert('모든 필드를 입력하고 개인정보 수집에 동의해주세요.');
        return;
    }
    
    // 나이 확인 (65세 이상)
    const birth = new Date(birthDate);
    const today = new Date();
    const age = today.getFullYear() - birth.getFullYear();
    
    if (age < 65) {
        alert('이 서비스는 65세 이상 어르신을 대상으로 합니다.');
        return;
    }
    
    try {
        showLoading('사용자 정보를 등록하고 있습니다...');
        
        const response = await fetch(`${API_BASE_URL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                birth_date: birthDate,
                address: `남해군 ${district}`,
                district_code: district
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentUser = data;
            hideUserInfoModal();
            
            // 설문 시작
            await startSurvey();
            
            if (isVoiceEnabled) {
                speak('설문을 시작합니다.');
            }
        } else {
            alert('사용자 등록에 실패했습니다: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('서버 연결에 실패했습니다.');
    } finally {
        hideLoading();
    }
}

// 결과 조회 처리
async function handleLookupSubmit() {
    const lookupKey = document.getElementById('lookup-key').value;
    
    if (!lookupKey) {
        alert('조회 키를 입력해주세요.');
        return;
    }
    
    try {
        showLoading('결과를 조회하고 있습니다...');
        
        const response = await fetch(`${API_BASE_URL}/results/${lookupKey}`);
        const data = await response.json();
        
        if (response.ok) {
            hideLookupModal();
            showResults(data);
            
            if (isVoiceEnabled) {
                speak('결과를 조회했습니다.');
            }
        } else {
            alert('결과 조회에 실패했습니다: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('서버 연결에 실패했습니다.');
    } finally {
        hideLoading();
    }
}

// 설문 시작
async function startSurvey() {
    try {
        const response = await fetch(`${API_BASE_URL}/survey/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUser.user_id
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentSession = data;
            currentStep = 1;
            
            // 설문 페이지로 이동
            window.location.href = 'survey.html';
        } else {
            alert('설문 시작에 실패했습니다: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('서버 연결에 실패했습니다.');
    }
}

// 결과 표시
function showResults(data) {
    // 결과 페이지로 이동 (localStorage에 데이터 저장)
    localStorage.setItem('resultData', JSON.stringify(data));
    window.location.href = 'results.html';
}

// 글자 크기 조절
function toggleFontSize() {
    fontSizeLevel = (fontSizeLevel % 3) + 1;
    
    const body = document.body;
    
    // 기존 크기 클래스 제거
    body.classList.remove('text-size-normal', 'text-size-medium', 'text-size-large');
    
    // 새 크기 클래스 추가
    switch (fontSizeLevel) {
        case 1:
            body.classList.add('text-size-normal');
            break;
        case 2:
            body.classList.add('text-size-medium');
            break;
        case 3:
            body.classList.add('text-size-large');
            break;
    }
    
    // 상태 저장
    localStorage.setItem('fontSizeLevel', fontSizeLevel);
    
    if (isVoiceEnabled) {
        speak(`글자 크기를 ${fontSizeLevel}단계로 조절했습니다.`);
    }
}

// 음성 안내 토글
function toggleVoice() {
    isVoiceEnabled = !isVoiceEnabled;
    
    // 버튼 상태 업데이트
    if (isVoiceEnabled) {
        voiceToggleBtn.classList.add('bg-blue-100', 'border-blue-500');
        floatingVoiceBtn.classList.add('bg-blue-700');
        speak('음성 안내가 켜졌습니다.');
    } else {
        voiceToggleBtn.classList.remove('bg-blue-100', 'border-blue-500');
        floatingVoiceBtn.classList.remove('bg-blue-700');
        
        // 진행 중인 음성 중지
        if (speechSynthesis.speaking) {
            speechSynthesis.cancel();
        }
    }
    
    // 상태 저장
    localStorage.setItem('isVoiceEnabled', isVoiceEnabled);
}

// 고대비 모드 토글
function toggleHighContrast() {
    isHighContrast = !isHighContrast;
    
    if (isHighContrast) {
        mainBody.classList.add('high-contrast');
        highContrastBtn.classList.add('bg-yellow-400', 'border-yellow-600');
    } else {
        mainBody.classList.remove('high-contrast');
        highContrastBtn.classList.remove('bg-yellow-400', 'border-yellow-600');
    }
    
    // 상태 저장
    localStorage.setItem('isHighContrast', isHighContrast);
    
    if (isVoiceEnabled) {
        speak(`고대비 모드가 ${isHighContrast ? '켜졌습니다' : '꺼졌습니다'}.`);
    }
}

// 음성 출력
function speak(text) {
    if (!isVoiceEnabled || !speechSynthesis) return;
    
    // 진행 중인 음성 중지
    if (speechSynthesis.speaking) {
        speechSynthesis.cancel();
    }
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ko-KR';
    utterance.rate = 0.8;
    utterance.pitch = 1;
    
    speechSynthesis.speak(utterance);
}

// 사용자 설정 로드
function loadUserPreferences() {
    // 글자 크기
    const savedFontSize = localStorage.getItem('fontSizeLevel');
    if (savedFontSize) {
        fontSizeLevel = parseInt(savedFontSize);
        
        const body = document.body;
        body.classList.remove('text-size-normal', 'text-size-medium', 'text-size-large');
        
        switch (fontSizeLevel) {
            case 1:
                body.classList.add('text-size-normal');
                break;
            case 2:
                body.classList.add('text-size-medium');
                break;
            case 3:
                body.classList.add('text-size-large');
                break;
        }
    }
    
    // 음성 안내
    const savedVoice = localStorage.getItem('isVoiceEnabled');
    if (savedVoice === 'true') {
        isVoiceEnabled = true;
        voiceToggleBtn.classList.add('bg-blue-100', 'border-blue-500');
        floatingVoiceBtn.classList.add('bg-blue-700');
    }
    
    // 고대비 모드
    const savedHighContrast = localStorage.getItem('isHighContrast');
    if (savedHighContrast === 'true') {
        isHighContrast = true;
        mainBody.classList.add('high-contrast');
        highContrastBtn.classList.add('bg-yellow-400', 'border-yellow-600');
    }
}

// 로딩 표시
function showLoading(message) {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loading-overlay';
    loadingDiv.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    loadingDiv.innerHTML = `
        <div class="bg-white rounded-lg p-6 text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p class="text-gray-700">${message}</p>
        </div>
    `;
    
    document.body.appendChild(loadingDiv);
}

// 로딩 숨기기
function hideLoading() {
    const loadingDiv = document.getElementById('loading-overlay');
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

// 유틸리티 함수들
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatCurrency(amount) {
    if (typeof amount === 'string') {
        return amount;
    }
    
    return new Intl.NumberFormat('ko-KR', {
        style: 'currency',
        currency: 'KRW'
    }).format(amount);
}

// 에러 처리
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    
    if (isVoiceEnabled) {
        speak('오류가 발생했습니다. 페이지를 새로고침해주세요.');
    }
});

// 페이지 이탈 시 데이터 저장
window.addEventListener('beforeunload', function() {
    // 현재 상태 저장
    if (currentUser) {
        sessionStorage.setItem('currentUser', JSON.stringify(currentUser));
    }
    
    if (currentSession) {
        sessionStorage.setItem('currentSession', JSON.stringify(currentSession));
    }
});

// 네트워크 상태 확인
window.addEventListener('online', function() {
    if (isVoiceEnabled) {
        speak('인터넷 연결이 복구되었습니다.');
    }
});

window.addEventListener('offline', function() {
    if (isVoiceEnabled) {
        speak('인터넷 연결이 끊어졌습니다.');
    }
    
    alert('인터넷 연결을 확인해주세요.');
});

// 접근성 개선: 포커스 가능한 요소들에 키보드 이벤트 추가
document.addEventListener('keydown', function(e) {
    // Enter 키로 버튼 클릭
    if (e.key === 'Enter' && e.target.classList.contains('btn')) {
        e.target.click();
    }
    
    // 스페이스바로 체크박스 토글
    if (e.key === ' ' && e.target.type === 'checkbox') {
        e.preventDefault();
        e.target.checked = !e.target.checked;
    }
});

// 스크린 리더 지원
function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

// 터치 디바이스 지원
let touchStartX = 0;
let touchStartY = 0;

document.addEventListener('touchstart', function(e) {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
});

document.addEventListener('touchend', function(e) {
    const touchEndX = e.changedTouches[0].clientX;
    const touchEndY = e.changedTouches[0].clientY;
    
    const deltaX = touchEndX - touchStartX;
    const deltaY = touchEndY - touchStartY;
    
    // 스와이프 제스처 감지 (필요시 구현)
    if (Math.abs(deltaX) > Math.abs(deltaY)) {
        if (deltaX > 50) {
            // 오른쪽 스와이프
        } else if (deltaX < -50) {
            // 왼쪽 스와이프
        }
    }
});

// 개발자 도구 감지 (보안)
let devtools = {
    open: false,
    orientation: null
};

function detectDevTools() {
    if (window.outerHeight - window.innerHeight > 200 || window.outerWidth - window.innerWidth > 200) {
        if (!devtools.open) {
            devtools.open = true;
            console.warn('개발자 도구가 감지되었습니다.');
        }
    } else {
        devtools.open = false;
    }
}

// 주기적으로 개발자 도구 감지
setInterval(detectDevTools, 1000); 
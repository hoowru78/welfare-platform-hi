@echo off
echo 남해 복지 추천 웹사이트 - 긴급 배포 스크립트
echo.

echo 1. 파일 압축 중...
powershell "Compress-Archive -Path '.\*' -DestinationPath '..\welfare-fixed-final.zip' -Force"

echo 2. 탐색기에서 압축 파일 열기...
explorer ..\

echo.
echo ===== 다음 단계 =====
echo 1. welfare-fixed-final.zip 파일 확인
echo 2. GitHub에서 새 저장소 생성
echo 3. 압축 파일 업로드
echo 4. Render에서 새 저장소 연결
echo.
pause 
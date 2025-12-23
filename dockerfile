# 1. 베이스 이미지 설정 (파이썬 3.11 slim 버전 사용)
FROM python:3.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 필수 시스템 패키지 설치 (필요한 경우)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 소스 코드 복사
COPY . .

# 6. 포트 노출 (FastAPI 기본 포트 8000)
EXPOSE 8000

# 7. 실행 명령 (uvicorn 사용)
# --host 0.0.0.0 설정이 있어야 외부(도커 외부)에서 접속이 가능하다.
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
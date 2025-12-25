from fastapi import FastAPI
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from neo4j import GraphDatabase
import os

app = FastAPI()

# 환경 변수에서 설정값 로드 (없을 경우 기본값 사용)
DB_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@rds_endpoint:5432/db_name")
NEO4J_URL = os.getenv("NEO4J_URL", "bolt://IP:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PW = os.getenv("NEO4J_PW", "stolink1234")
SPRING_URL = os.getenv("SPRING_URL", "http://IP:8080")

# DB 설정
engine = create_engine(DB_URL)


@app.get("/api/fastapi/check-all")
def check_all():
    results = {}

    # 1. PostgreSQL 체크
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        results["postgresql"] = "OK"
    except Exception as e:
        results["postgresql"] = f"FAIL: {str(e)}"

    # 2. Neo4j 체크
    try:
        driver = GraphDatabase.driver(
            NEO4J_URL, auth=(NEO4J_USER, NEO4J_PW))
        with driver.session() as session:
            session.run("RETURN 1")
        results["neo4j"] = "OK"
    except Exception as e:
        results["neo4j"] = f"FAIL: {str(e)}"

    # 3. Spring 통신 체크
    try:
        res = requests.get(f"{SPRING_URL}/api/spring/health")
        results["spring_link"] = f"OK ({res.text})"
    except Exception as e:
        results["spring_link"] = f"FAIL: {str(e)}"

    return results


@app.get("/api/fastapi/health")
def health():
    return "FastAPI is Alive"

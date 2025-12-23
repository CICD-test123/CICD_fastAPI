from fastapi import FastAPI
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from neo4j import GraphDatabase

app = FastAPI()

# DB 설정 (PostgreSQL 엔진 정의)
engine = create_engine(
    "postgresql://user:password@localhost:5432/database_name")


@app.get("/api/fastapi/check-all")
def check_all():
    results = {}

    # 1. PostgreSQL 체크e
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        results["postgresql"] = "OK"
    except Exception as e:
        results["postgresql"] = f"FAIL: {str(e)}"

    # 2. Neo4j 체크
    try:
        driver = GraphDatabase.driver(
            "bolt://[NEO4J_PRIVATE_IP]:7687", auth=("neo4j", "password"))
        with driver.session() as session:
            session.run("RETURN 1")
        results["neo4j"] = "OK"
    except Exception as e:
        results["neo4j"] = f"FAIL: {str(e)}"

    # 3. Spring 통신 체크
    try:
        res = requests.get("http://[SPRING_PRIVATE_IP]:8080/api/spring/health")
        results["spring_link"] = f"OK ({res.text})"
    except Exception as e:
        results["spring_link"] = f"FAIL: {str(e)}"

    return results


@app.get("/api/fastapi/health")
def health(): return "FastAPI is Alive"

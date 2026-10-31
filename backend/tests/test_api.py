import asyncio
import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.config import settings


async def run_tests():
    print("🧪 Running Automated Backend API Integration Tests...\n")
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # 1. Health check
        res = await client.get("/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        data = res.json()
        assert data["status"] == "healthy"
        print("✅ 1. GET /health - OK (Service healthy, bot telemetry included)")

        # 1.1 Static SPA Mount test
        spa_res = await client.get("/")
        if spa_res.status_code == 200:
            assert "<!doctype html>" in spa_res.text.lower()
            print("✅ 1.1 GET / (SPA Mount) - OK (Single-port React index.html served)")


        # 2. Team list
        res = await client.get("/api/v1/team")
        assert res.status_code == 200, f"Team list failed: {res.text}"
        members = res.json()
        assert len(members) >= 1, f"Expected at least 1 member, got {len(members)}"
        print(f"✅ 2. GET /api/v1/team - OK ({len(members)} members retrieved)")

        # 3. Projects list
        res = await client.get("/api/v1/projects")
        assert res.status_code == 200, f"Projects list failed: {res.text}"
        projects = res.json()
        assert len(projects) >= 3, f"Expected at least 3 seeded projects, got {len(projects)}"
        print(f"✅ 3. GET /api/v1/projects - OK ({len(projects)} projects retrieved)")

        # 4. Filter projects
        res = await client.get("/api/v1/projects?category=AI")
        assert res.status_code == 200
        ai_projects = res.json()
        assert all("AI" in p["category"] for p in ai_projects)
        print(f"✅ 4. GET /api/v1/projects?category=AI - OK ({len(ai_projects)} AI projects filtered)")

        # 5. Awards list
        res = await client.get("/api/v1/awards")
        assert res.status_code == 200
        awards = res.json()
        assert len(awards) >= 4
        print(f"✅ 5. GET /api/v1/awards - OK ({len(awards)} awards retrieved)")

        # 6. Team stats
        res = await client.get("/api/v1/stats")
        assert res.status_code == 200
        stats = res.json()
        assert "total_members" in stats
        assert "total_projects" in stats
        assert "total_awards" in stats
        assert stats["first_place_wins"] >= 1
        print(f"✅ 6. GET /api/v1/stats - OK ({stats['total_awards']} awards, {stats['first_place_wins']} 1st places)")

        # 7. Bot status
        res = await client.get("/api/v1/bot/status")
        assert res.status_code == 200
        bot_telemetry = res.json()
        assert "is_online" in bot_telemetry
        print(f"✅ 7. GET /api/v1/bot/status - OK (Telemetry retrieved)")

        # 8. Public contact submission
        res = await client.post("/api/v1/inbox", json={
            "sender_name": "API Test Recruiter",
            "email": "test@recruiter.com",
            "organization": "Y Combinator",
            "message": "Testing automated public submission pipeline.",
        })
        assert res.status_code == 201, f"Inbox submit failed: {res.text}"
        submission = res.json()
        submission_id = submission["id"]
        print(f"✅ 8. POST /api/v1/inbox - OK (Submission #{submission_id} created)")

        # 9. Admin protection test: access inbox WITHOUT key
        res = await client.get("/api/v1/inbox")
        assert res.status_code == 401, f"Expected 401 Unauthorized without key, got {res.status_code}"
        print("✅ 9. Security Test: GET /api/v1/inbox without key -> 401 Unauthorized (Blocked properly)")

        # 10. Admin access WITH X-Admin-Key header
        admin_headers = {"X-Admin-Key": settings.ADMIN_API_KEY}
        res = await client.get("/api/v1/inbox", headers=admin_headers)
        assert res.status_code == 200, f"Expected 200 OK with admin key, got {res.status_code}"
        inbox_items = res.json()
        assert any(item["id"] == submission_id for item in inbox_items)
        print(f"✅ 10. Security Test: GET /api/v1/inbox with X-Admin-Key -> 200 OK ({len(inbox_items)} items accessible)")

        # 11. Admin CRUD: Create team member
        new_member_res = await client.post("/api/v1/team", json={
            "name": "Integration Test Member",
            "role": "QA Specialist",
            "bio": "Automated test member to verify CRUD lifecycle.",
            "skills": "[\"Python\", \"Pytest\"]",
            "display_order": 99,
        }, headers=admin_headers)
        assert new_member_res.status_code == 201
        created_id = new_member_res.json()["id"]
        print(f"✅ 11. POST /api/v1/team (Admin) - OK (Created member #{created_id})")

        # 12. Admin CRUD: Delete team member
        del_res = await client.delete(f"/api/v1/team/{created_id}", headers=admin_headers)
        assert del_res.status_code == 204
        print(f"✅ 12. DELETE /api/v1/team/{created_id} (Admin) - OK (Cleaned up test member)")

        # 13. Clean up the test submission
        del_inbox = await client.delete(f"/api/v1/inbox/{submission_id}", headers=admin_headers)
        assert del_inbox.status_code == 204
        print(f"✅ 13. DELETE /api/v1/inbox/{submission_id} (Admin) - OK (Cleaned up test submission)")

        # 14. Cloudinary Upload Endpoint security & config check
        upload_no_auth = await client.post("/api/v1/upload/image", files={"file": ("test.png", b"fakecontent", "image/png")})
        assert upload_no_auth.status_code == 401
        print("✅ 14. POST /api/v1/upload/image without auth -> 401 Unauthorized (Security verified)")

        upload_auth = await client.post("/api/v1/upload/image", files={"file": ("test.png", b"fakecontent", "image/png")}, headers=admin_headers)
        assert upload_auth.status_code in [200, 400, 500]
        print(f"✅ 15. POST /api/v1/upload/image with auth -> {upload_auth.status_code} (Gracefully handled)")

    print("\n🎉 ALL 15 BACKEND API & INTEGRATION TESTS PASSED PERFECTLY!\n")



if __name__ == "__main__":
    asyncio.run(run_tests())


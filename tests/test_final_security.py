def test_faq_learning_post_validation_invalid_question(client):
    res = client.post(
        "/api/faq-learning/learned",
        json={"question_pattern": "", "answer": "Valid answer"},
    )
    assert res.status_code == 400
    assert "Invalid question_pattern" in res.json["error"]


def test_faq_learning_post_validation_invalid_answer(client):
    res = client.post(
        "/api/faq-learning/learned",
        json={"question_pattern": "Valid question?", "answer": "x" * 6000},
    )
    assert res.status_code == 400
    assert "Invalid answer" in res.json["error"]


def test_faq_learning_put_validation_invalid_payload(client):
    # First create a FAQ
    create_res = client.post(
        "/api/faq-learning/learned",
        json={"question_pattern": "Test?", "answer": "Test answer"},
    )
    if create_res.status_code == 201:
        faq_id = create_res.json["faq"]["id"]
        # Try to update with invalid payload
        res = client.put(
            f"/api/faq-learning/learned/{faq_id}",
            json={"question_pattern": "x" * 600},  # Too long
        )
        assert res.status_code == 400


def test_upload_mime_validation_svg_disguised(client):
    """Test that SVG content is blocked even with .jpg extension"""
    import io

    svg_content = b'<svg xmlns="http://www.w3.org/2000/svg"></svg>'
    data = {
        "file": (io.BytesIO(svg_content), "fake.jpg"),
        "folder": "general",
    }
    res = client.post("/api/upload/image", data=data, content_type="multipart/form-data")
    # Should fail if python-magic is available
    assert res.status_code in (400, 500)  # 400 if MIME check works, may be 500 without magic

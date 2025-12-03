def test_upload_rejects_svg(client):
    import io

    data = {
        "file": (io.BytesIO(b"<svg></svg>"), "test.svg"),
        "folder": "general",
    }
    res = client.post("/api/upload/image", data=data, content_type="multipart/form-data")
    assert res.status_code == 400
    assert res.json["success"] is False


def test_upload_rejects_too_large(client):
    import io

    big = io.BytesIO(b"x" * (11 * 1024 * 1024))
    data = {
        "file": (big, "big.jpg"),
        "folder": "general",
    }
    res = client.post("/api/upload/image", data=data, content_type="multipart/form-data")
    assert res.status_code == 413
    assert res.json["success"] is False

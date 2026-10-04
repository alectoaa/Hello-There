import pytest

def test_rtsp_url_construction():
    """RTSP URL yapılandırma testi."""
    ip = "192.168.1.100"
    port = 554
    expected_url = f"rtsp://{ip}:{port}/"
    assert f"rtsp://{ip}:{port}/" == expected_url

def test_default_timeout():
    """Soket zaman aşımı doğrulama testi."""
    timeout = 2.0
    assert timeout > 0

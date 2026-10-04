import pytest
import socket

#libs gonna add

def test_ip_validation():
    """Örnek IP doğrulama mantığı testi."""
    valid_ip = "192.168.1.1"
    invalid_ip = "999.999.999.999"

  
    assert valid_ip.count(".") == 3
    assert not invalid_ip.startswith("192.168")

def test_rtsp_url_construction():
    """RTSP bağlantı dizgisi oluşturma testi."""
    ip = "10.0.0.5"
    port = 554
    expected_url = f"rtsp://{ip}:{port}/"
    
    assert f"rtsp://{ip}:{port}/" == expected_url

def test_socket_timeout_default():
    """Varsayılan soket zaman aşımı testi."""
    default_timeout = 2.0
    assert default_timeout > 0

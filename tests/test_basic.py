import pytest
import sys
import os

# Добавляем путь к приложению
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_basic_math():
    """Простой тест для проверки работы pytest"""
    assert 1 + 1 == 2

def test_import_app():
    """Тест что приложение импортируется без ошибок"""
    try:
        from main import create_app
        app = create_app()
        assert app is not None
        print("✅ Приложение успешно импортировано")
    except Exception as e:
        pytest.fail(f"Ошибка импорта приложения: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

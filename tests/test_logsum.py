import csv
import subprocess
from pathlib import Path
import pytest

@pytest.fixture
def sample_csv(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    file_path = d / "events.csv"
    content = (
        "timestamp,level,service,message\n"
        "2026-10-15T10:00:00,INFO,auth,Login successful\n"
        "2026-10-15T10:01:00,,auth,Missing level test\n"
        "2026-10-15T10:02:00,INFO,auth,Another login\n"
        "2026-10-15T10:03:00,ERROR,payment,Payment failed\n"
    )
    file_path.write_text(content, encoding="utf-8")
    return file_path

@pytest.fixture
def empty_csv(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    file_path = d / "events.csv"
    file_path.write_text("timestamp,level,service,message\n", encoding="utf-8")
    return file_path

def test_cli_execution(sample_csv, tmp_path):
    output_path = tmp_path / "summary.csv"
    result = subprocess.run(
        ["python", "-m", "src.logsum", str(sample_csv), str(output_path)],
	check=False,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert output_path.exists()

def test_grouping_and_aggregation(sample_csv, tmp_path):
    output_path = tmp_path / "summary.csv"
    subprocess.run(["python", "-m", "src.logsum", str(sample_csv), str(output_path)], check=True)
    
    with open(output_path, mode="r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        
    # Check total groups
    assert len(reader) == 3
    
    # Find auth INFO group
    auth_info = next(r for r in reader if r["service"] == "auth" and r["level"] == "INFO")
    assert int(auth_info["count"]) == 2
    assert auth_info["first_seen"] == "2026-10-15T10:00:00"
    assert auth_info["last_seen"] == "2026-10-15T10:02:00"

def test_missing_level_normalization(sample_csv, tmp_path):
    output_path = tmp_path / "summary.csv"
    subprocess.run(["python", "-m", "src.logsum", str(sample_csv), str(output_path)], check=True)
    
    with open(output_path, mode="r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        
    auth_unknown = next(r for r in reader if r["service"] == "auth" and r["level"] == "UNKNOWN")
    assert int(auth_unknown["count"]) == 1

def test_empty_input_behaviour(empty_csv, tmp_path):
    output_path = tmp_path / "summary.csv"
    result = subprocess.run(
        ["python", "-m", "src.logsum", str(empty_csv), str(output_path)],
	check=False,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert output_path.exists()

def test_bad_input_exit_code(tmp_path):
    non_existent = tmp_path / "non_existent.csv"
    output_path = tmp_path / "summary.csv"
    result = subprocess.run(
        ["python", "-m", "src.logsum", str(non_existent), str(output_path)],
	check=False,
        capture_output=True,
        text=True
    )
    assert result.returncode != 0
import subprocess
from pathlib import Path

def check_env_in_gitignore() -> bool:
    """.gitignore에 .env가 있는지 확인."""
    # 여기에 Path('.gitignore').read_text()를 읽고 '.env' in text 반환 코드를 채워요.
    return ".env" in Path(".gitignore").read_text() 

    

def check_env_in_staged() -> bool:
    """git staged 파일 목록에 .env가 없는지 확인 (False면 안전)."""
    # 여기에 subprocess.run(['git', 'diff', '--cached', '--name-only'],
    #   capture_output=True, text=True) 결과의 stdout에 '.env'가 있는지
    #   검사하는 코드를 채워요.
    result = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True)
    return ".env" in result.stdout

if __name__ == "__main__":
    # 여기에 두 검증 결과 출력 + 둘 다 안전하면 "push 가능" 출력 코드를 채워요.
    print(check_env_in_gitignore())
    print(check_env_in_staged())
    if check_env_in_gitignore() and not check_env_in_staged():
        print('push 가능')
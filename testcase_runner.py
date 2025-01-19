from pathlib import Path
import subprocess
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm  # 進捗バー表示のためのライブラリ
from typing import List
import os
import sys

ROOT = Path(__file__).parent
INPUT_DIR = ROOT / 'in'  # 入力ファイルが含まれるディレクトリ
OUTPUT_DIR = ROOT / 'out'  # 出力ファイルを保存するディレクトリ

MAX_WORKERS = 8 # 並列実行数
TIME_LIMIT = 36000.0# 実行時間制限

RUN_COMMAND = ["python" ,"main.py"]  # 実行コマンド

# 出力ディレクトリの作成
OUTPUT_DIR.mkdir(exist_ok=True)

def process_file(input_file: Path) -> int:
    """指定されたファイルを読み込み、コマンドを実行して結果を出力ディレクトリに保存し、スコアを返す"""
    try:
        with open(input_file, "rb") as f:
            input_data = f.read()

        res = subprocess.run(
            RUN_COMMAND,
            input=input_data,
            capture_output=True,
            timeout=TIME_LIMIT
        )

        output_file = OUTPUT_DIR / input_file.name
        with open(output_file, "w") as f:
            f.write(res.stdout.decode('utf-8').strip() + "\n")

        # 標準出力からScoreを抽出
        stderr = res.stderr.decode('utf-8')
        return int(stderr.splitlines()[0])
    except subprocess.TimeoutExpired:
        return 0  # タイムアウト時のスコアは0として扱う

def main():
    input_files = sorted(INPUT_DIR.glob("*.txt"))  # inディレクトリ内のすべての.txtファイル

    total_score = 0  # 総スコア

    # tqdm を使用して進捗状況を表示
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for score in tqdm(executor.map(process_file, input_files), total=len(input_files), desc="Processing files"):
            print(score)
            total_score += score

    print(f"Total Score: {total_score}")
    print(f"Total Score: {total_score}", file=sys.stderr)

if __name__ == "__main__":
    main()

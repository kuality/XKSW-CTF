#!/usr/bin/env python3

import io
import os
import sys
import zipfile
import subprocess
from pathlib import Path

ZIP_LFH = b'PK\x03\x04'   # Local File Header
ZIP_EOCD = b'PK\x05\x06'  # End of Central Directory

VIDEO_EXTS = {'.mp4', '.mov', '.mkv', '.avi', '.webm', '.m4v'}

def carve_zips_from_file(binary_path: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    data = binary_path.read_bytes()
    zips = []

    starts = []
    search_from = 0
    while True:
        i = data.find(ZIP_LFH, search_from)
        if i == -1:
            break
        starts.append(i)
        search_from = i + 1

    if not starts:
        print("[!] ZIP 시작 시그니처(PK\\x03\\x04)를 찾지 못했습니다.")
        return zips

    for idx, start in enumerate(starts, 1):
        pos = start
        while True:
            eocd_pos = data.find(ZIP_EOCD, pos)
            if eocd_pos == -1:
                break
            if eocd_pos + 22 > len(data):
                break
            comment_len = int.from_bytes(data[eocd_pos + 20:eocd_pos + 22], 'little', signed=False)
            end = eocd_pos + 22 + comment_len
            if end > len(data):
                pos = eocd_pos + 1
                continue

            candidate = data[start:end]
            # zipfile로 유효성 검사
            try:
                with zipfile.ZipFile(io.BytesIO(candidate)) as zf:
                    broken = zf.testzip()
                    if broken is not None:
                        pos = eocd_pos + 1
                        continue
            except zipfile.BadZipFile:
                pos = eocd_pos + 1
                continue

            out_path = out_dir / f"carved_{idx}_{eocd_pos-start}.zip"
            out_path.write_bytes(candidate)
            print(f"[+] ZIP 추출: {out_path}")
            zips.append(out_path)
            break

    if not zips:
        print("[!] 유효한 ZIP 블록을 찾지 못했습니다. 파일이 암호화되어 있거나 포맷이 특이할 수 있습니다.")
    return zips

def unzip_all(zip_paths, extract_root: Path):
    extracted_files = []
    extract_root.mkdir(parents=True, exist_ok=True)

    for zp in zip_paths:
        target = extract_root / zp.stem
        target.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(zp) as zf:
                zf.extractall(target)
            print(f"[+] 압축해제: {zp.name} -> {target}")
            for p in target.rglob('*'):
                if p.is_file():
                    extracted_files.append(p)
        except RuntimeError as e:
            print(f"[!] 압축해제 실패(암호 필요 가능): {zp.name} - {e}")
        except zipfile.BadZipFile:
            print(f"[!] 손상된 ZIP: {zp}")
    return extracted_files

def extract_audio_from_videos(paths, audio_out_dir: Path, codec='mp3', bitrate='192k'):
    audio_out_dir.mkdir(parents=True, exist_ok=True)
    made = []

    for p in paths:
        if p.suffix.lower() not in VIDEO_EXTS:
            continue
        # 출력 확장자 결정
        if codec == 'copy':
            out_ext = '.m4a'
        else:
            out_ext = f".{codec}"

        out_name = p.stem + out_ext
        out_path = audio_out_dir / out_name

        # ffmpeg 명령 구성
        cmd = [
            "ffmpeg",
            "-y",           # 덮어쓰기
            "-i", str(p),
            "-vn",          # 영상 제거
        ]
        if codec == 'copy':
            cmd += ["-acodec", "copy"]
        else:
            cmd += ["-ac", "2", "-ar", "44100", "-b:a", bitrate, "-acodec", codec]
        cmd += [str(out_path)]

        print(f"[*] 오디오 추출: {p.name} -> {out_path.name}")
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            made.append(out_path)
        except subprocess.CalledProcessError:
            print(f"[!] ffmpeg 실패: {p}")
    return made

def main(image_path: str, work_dir: str = "work"):
    img = Path(image_path)
    if not img.exists():
        print(f"[!] 입력 파일 없음: {img}")
        sys.exit(1)

    base = Path(work_dir)
    carved_dir = base / "carved_zips"
    extracted_dir = base / "unzipped"
    audio_dir = base / "audio"

    zips = carve_zips_from_file(img, carved_dir)
    if not zips:
        print("[!] 종료: ZIP을 찾지 못했습니다.")
        return

    files = unzip_all(zips, extracted_dir)
    if not files:
        print("[!] 종료: 압축해제 결과가 없습니다.")
        return

    audios = extract_audio_from_videos(files, audio_dir, codec='mp3', bitrate='192k')
    if audios:
        print("\n[✓] 오디오 파일:")
        for a in audios:
            print(" -", a)
    else:
        print("[!] 영상 파일이 없거나 오디오 추출에 실패했습니다.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"사용법: {Path(sys.argv[0]).name} <이미지/바이너리 파일 경로> [작업폴더]")
        sys.exit(0)
    image_path = sys.argv[1]
    work_dir = sys.argv[2] if len(sys.argv) >= 3 else "work"
    main(image_path, work_dir)
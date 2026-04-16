import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"读取文件失败: {path} ({e})") from e


def _load_json_file(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(str(path))

    raw = _read_text(path).strip()
    if raw == "":
        raise ValueError("JSON内容为空")

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON解析失败: {e}") from e


def _load_or_init_readed(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"total_results": 0, "papers": []}

    raw = _read_text(path).strip()
    if raw == "":
        return {"total_results": 0, "papers": []}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"readed_papers JSON解析失败: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("readed_papers 顶层必须是dict")
    if "papers" not in data:
        data["papers"] = []
    if not isinstance(data["papers"], list):
        raise ValueError("readed_papers.papers 必须是list")
    if "total_results" not in data or not isinstance(data.get("total_results"), int):
        data["total_results"] = len(data["papers"])

    return data


def _validate_src(src: Any) -> Dict[str, Any]:
    if not isinstance(src, dict):
        raise ValueError("src-file 顶层必须是dict")
    papers = src.get("papers")
    if not isinstance(papers, list):
        raise ValueError("src-file.papers 必须存在且为list")
    return src


def _atomic_write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    payload = json.dumps(obj, ensure_ascii=False, indent=2)
    try:
        tmp_path.write_text(payload, encoding="utf-8")
        os.replace(tmp_path, path)
    finally:
        try:
            if tmp_path.exists():
                tmp_path.unlink()
        except Exception:  # noqa: BLE001
            pass


def _extract_id_url(paper: Any) -> Tuple[str, str]:
    if not isinstance(paper, dict):
        raise ValueError("paper条目必须是dict")
    pid = paper.get("id")
    url = paper.get("url")
    if not isinstance(pid, str) or pid.strip() == "":
        raise ValueError("paper.id 缺失或不是非空字符串")
    if not isinstance(url, str) or url.strip() == "":
        raise ValueError(f"paper.url 缺失或不是非空字符串 (id={pid})")
    return pid, url


def _pdf_to_src(url: str) -> str:
    if "/pdf/" in url:
        return url.replace("/pdf/", "/src/", 1)
    return url


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Parse arXiv search results and output unread /src/ URLs."
    )
    parser.add_argument("--src-file", required=True, help="待处理的搜索结果JSON文件")
    parser.add_argument("--readed_papers", required=True, help="已读论文JSON文件（会被更新）")
    parser.add_argument("--dst-file", required=True, help="输出的未读URL列表JSON文件")
    args = parser.parse_args()

    src_path = Path(args.src_file)
    readed_path = Path(args.readed_papers)
    dst_path = Path(args.dst_file)

    try:
        src = _validate_src(_load_json_file(src_path))
        readed = _load_or_init_readed(readed_path)
    except FileNotFoundError as e:
        _eprint(f"文件不存在: {e}")
        return 2
    except ValueError as e:
        _eprint(str(e))
        return 2
    except RuntimeError as e:
        _eprint(str(e))
        return 2

    readed_ids: set[str] = set()
    for p in readed.get("papers", []):
        if isinstance(p, dict) and isinstance(p.get("id"), str) and p["id"].strip():
            readed_ids.add(p["id"])

    dst_list: List[Dict[str, str]] = []
    appended = 0

    for paper in src["papers"]:
        try:
            pid, url = _extract_id_url(paper)
        except ValueError as e:
            _eprint(f"跳过无效paper条目: {e}")
            continue

        if pid in readed_ids:
            continue

        dst_list.append({"id": pid, "url": _pdf_to_src(url)})
        readed["papers"].append(paper)
        readed_ids.add(pid)
        appended += 1

    readed["total_results"] = len(readed.get("papers", []))

    try:
        _atomic_write_json(dst_path, dst_list)
        _atomic_write_json(readed_path, readed)
    except Exception as e:  # noqa: BLE001
        _eprint(f"写文件失败: {e}")
        return 3

    print(
        json.dumps(
            {
                "src_total": len(src["papers"]),
                "dst_unread": len(dst_list),
                "readed_appended": appended,
                "readed_total": readed["total_results"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

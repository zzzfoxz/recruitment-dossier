#!/usr/bin/env python3
"""
Standalone zero-cost DuckDuckGo search script for recruitment dossier due diligence.
Usage:
    python scripts/search_dossier.py "华为" "小艺"
"""
import sys
import json

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        print("Error: Please install duckduckgo-search (or run with uv): pip install duckduckgo-search", file=sys.stderr)
        sys.exit(1)

def run_dossier_search(company: str, role_or_dept: str, max_results: int = 5):
    queries = [
        f"site:nowcoder.com OR site:zhihu.com \"{company}\" (毁意向 OR 毁offer OR 毁三方 OR 裁员 OR 锁HC OR 卡转正 OR 试用期辞退)",
        f"\"{company}\" \"{role_or_dept}\" (加班 OR 下班时间 OR WLB OR 大小周 OR 工时 OR 绩效 OR 房补 OR 户口 OR 班车)",
        f"site:nowcoder.com \"{company}\" \"{role_or_dept}\" (面经 OR 手撕 OR 几轮 OR 薪资 OR 开奖 OR 年终奖 OR SP OR SSP)"
    ]
    
    ddgs = DDGS()
    all_results = {}
    for i, q in enumerate(queries, 1):
        print(f"[*] Executing query {i}/3: {q}", file=sys.stderr)
        try:
            res = list(ddgs.text(q, max_results=max_results))
            all_results[f"query_{i}"] = [{
                "title": r.get("title", ""),
                "href": r.get("href", ""),
                "body": r.get("body", "")
            } for r in res]
        except Exception as e:
            print(f"[!] Error on query {i}: {e}", file=sys.stderr)
            all_results[f"query_{i}"] = []
            
    print(json.dumps(all_results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python search_dossier.py <Company> <Role/Dept>", file=sys.stderr)
        sys.exit(1)
    run_dossier_search(sys.argv[1], sys.argv[2])

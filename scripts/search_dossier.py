#!/usr/bin/env python3
"""
recruitment-dossier: Standalone Due-Diligence Search Engine
Zero-cost, multi-source search utility for company & job role risk assessment.

Usage:
    python search_dossier.py <Company> <Role/Dept> [options]
    uv run scripts/search_dossier.py "华为" "小艺算法" --type campus --format markdown
"""

import argparse
import json
import sys
from typing import List, Dict, Any

try:
    from duckduckgo_search import DDGS
except ImportError:
    try:
        from ddgs import DDGS
    except ImportError:
        print("[!] Missing duckduckgo-search package.", file=sys.stderr)
        print("[!] Please install: pip install duckduckgo-search (or use uv: uv run --with duckduckgo-search ...)", file=sys.stderr)
        sys.exit(1)

def build_queries(company: str, target: str, hire_type: str = "campus") -> List[Dict[str, str]]:
    if hire_type == "social":
        return [
            {
                "name": "1. 稳定性与离职裁员排雷 (Offer & Layoffs)",
                "query": f'site:nowcoder.com OR site:zhihu.com "{company}" (裁员 OR 锁HC OR PIP OR 试用期辞退 OR 强制劝退 OR 竞业协议 OR 优化)'
            },
            {
                "name": "2. 团队工时与管理文化 (Culture & WLB)",
                "query": f'"{company}" "{target}" (加班 OR 下班时间 OR WLB OR 大小周 OR 工时 OR 绩效 OR PUA OR 调休 OR 打卡)'
            },
            {
                "name": "3. 职级考核与真实薪酬 (Levels & Compensation)",
                "query": f'site:nowcoder.com OR site:zhihu.com "{company}" "{target}" (职级 OR 定级 OR 薪资 OR 年终奖 OR 几薪 OR 期权 OR 倒挂)'
            }
        ]
    else:  # campus or default
        return [
            {
                "name": "1. 毁约与意向稳定性排雷 (Offer Stability & Reneging)",
                "query": f'site:nowcoder.com OR site:zhihu.com "{company}" (毁意向 OR 毁offer OR 毁三方 OR 裁员 OR 锁HC OR 卡转正 OR 试用期辞退 OR 泡池子)'
            },
            {
                "name": "2. 部门工时与日常体感 (Culture, Hours & Welfare)",
                "query": f'"{company}" "{target}" (加班 OR 下班时间 OR WLB OR 大小周 OR 工时 OR 绩效 OR 房补 OR 户口 OR 班车 OR 公积金)'
            },
            {
                "name": "3. 校招面经与薪资开奖 (Interview Bar & Salary Tiers)",
                "query": f'site:nowcoder.com "{company}" "{target}" (面经 OR 手撕 OR 机考 OR 几轮 OR 薪资 OR 开奖 OR 年终奖 OR SP OR SSP)'
            }
        ]

def run_search(company: str, target: str, hire_type: str = "campus", max_results: int = 5) -> Dict[str, Any]:
    queries = build_queries(company, target, hire_type)
    ddgs = DDGS()
    results = {
        "company": company,
        "target": target,
        "type": hire_type,
        "queries": []
    }

    for item in queries:
        q_name = item["name"]
        q_str = item["query"]
        print(f"[*] Executing search: {q_name}", file=sys.stderr)
        query_entry = {
            "dimension": q_name,
            "query_string": q_str,
            "records": []
        }
        try:
            items = list(ddgs.text(q_str, max_results=max_results))
            for r in items:
                query_entry["records"].append({
                    "title": r.get("title", "").strip(),
                    "href": r.get("href", "").strip(),
                    "snippet": r.get("body", "").strip()
                })
        except Exception as e:
            print(f"[!] Error executing query: {e}", file=sys.stderr)
        results["queries"].append(query_entry)

    return results

def format_markdown(data: Dict[str, Any]) -> str:
    lines = []
    lines.append(f"# 🔍 多源实名/匿名情报抓取结果: {data['company']} - {data['target']}")
    lines.append(f"> **招聘类型**: {'社招/跳槽' if data['type'] == 'social' else '校招/实习'}  ")
    lines.append(f"> **抓取引擎**: DuckDuckGo Zero-Cost Search Engine  \n")
    
    for q in data["queries"]:
        lines.append(f"## {q['dimension']}")
        lines.append(f"`Query`: `{q['query_string']}`\n")
        if not q["records"]:
            lines.append("*未检索到高相关结果。*\n")
            continue
        for i, r in enumerate(q["records"], 1):
            lines.append(f"### {i}. [{r['title']}]({r['href']})")
            lines.append(f"{r['snippet']}\n")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="recruitment-dossier multi-source background check searcher")
    parser.add_argument("company", help="Target company name (e.g. 华为, 字节跳动, 腾讯)")
    parser.add_argument("target", help="Target department or role (e.g. 终端小艺, 算法工程师, 商业化架构)")
    parser.add_argument("--type", choices=["campus", "social"], default="campus", help="Hire type: campus (default) or social")
    parser.add_argument("--max-results", type=int, default=5, help="Max results per search query (default 5)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format: markdown (default) or json")
    parser.add_argument("--output", "-o", help="Optional output file path")

    args = parser.parse_args()

    data = run_search(args.company, args.target, args.type, args.max_results)

    if args.format == "json":
        output_str = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        output_str = format_markdown(data)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_str + "\n")
        print(f"[+] Output saved to {args.output}", file=sys.stderr)
    else:
        print(output_str)

if __name__ == "__main__":
    main()

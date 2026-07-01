# -*- coding: utf-8 -*-
"""
Linux.do 技术日报抓取 + AI 总结模块。

只读取 news.linuxe.top 已整理出的日报摘要和原帖索引，不抓取 linux.do 原帖正文或回复。
"""

import json
import logging
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests

from config import (
    AI_API_URL,
    AI_MODEL,
    GITHUB_TOKEN,
    LINUX_DO_MAX_ITEMS,
    LINUX_DO_MAX_RETRIES,
    LINUX_DO_NEWS_URL,
)

logger = logging.getLogger(__name__)


def fetch_linux_do_daily_items(count=None, max_retries=None):
    """获取 Linux.do 技术日报中的原帖索引。"""
    if count is None:
        count = LINUX_DO_MAX_ITEMS
    if max_retries is None:
        max_retries = LINUX_DO_MAX_RETRIES

    headers = {
        "User-Agent": "github-trending-spider/1.0 (+https://github.com/wenbochang888/github-trending-spider)",
    }
    for attempt in range(max_retries):
        try:
            logger.info("正在获取 Linux.do 技术日报 (第 %d 次尝试)", attempt + 1)
            resp = requests.get(LINUX_DO_NEWS_URL, headers=headers, timeout=30)
            resp.raise_for_status()
            report = parse_linux_do_daily_html(resp.text, LINUX_DO_NEWS_URL)
            items = report.get("items", [])
            if count and count > 0:
                items = items[:count]
            logger.info("Linux.do 技术日报: 解析到 %d 条原帖", len(items))
            return items
        except requests.RequestException as e:
            logger.warning("获取 Linux.do 技术日报失败: %s", e)
            if attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))
        except ValueError as e:
            logger.error("解析 Linux.do 技术日报失败: %s", e)
            return []

    logger.error("获取 Linux.do 技术日报失败，已达最大重试次数 %d", max_retries)
    return []


def parse_linux_do_daily_html(html_text, page_url=LINUX_DO_NEWS_URL):
    """解析 news.linuxe.top 首页 HTML。"""
    soup = BeautifulSoup(html_text or "", 'html.parser')

    title_tag = soup.title
    title = _clean_text(title_tag.get_text()) if title_tag else ""

    meta_bar = soup.find(class_=re.compile("metaBar"))
    meta_text = _clean_text(meta_bar.get_text()) if meta_bar else ""

    daily_headline_node = soup.find(class_=re.compile("dailyHeadline"))
    daily_headline = _clean_text(daily_headline_node.get_text()) if daily_headline_node else ""

    overview_node = soup.find(class_=re.compile("overview"))
    overview = _clean_text(overview_node.get_text()) if overview_node else ""

    note_node = soup.find(class_=re.compile("note"))
    note = _clean_text(note_node.get_text()) if note_node else ""

    highlights = []
    highlight_list = soup.find('ul', class_=re.compile("highlightList"))
    if highlight_list:
        for li in highlight_list.find_all('li', recursive=False):
            highlights.append(_clean_text(li.get_text()))

    sections = []
    for section_node in soup.find_all('section', class_=re.compile("articleSection")):
        h4 = section_node.find('h4')
        section_title = re.sub(r"^\d+\s*\.\s*", "", _clean_text(h4.get_text())).strip() if h4 else ""

        # In the original parser it would match <p> direct children or anywhere before the next section
        p = section_node.find('p')
        section_summary = _clean_text(p.get_text()) if p else ""

        links = []
        article_links = section_node.find('ul', class_=re.compile("articleLinks"))
        if article_links:
            for li in article_links.find_all('li', recursive=False):
                a_tag = li.find('a')
                if a_tag:
                    url = _normalize_topic_url(a_tag.get('href', ''), page_url)
                    link_title = _clean_text(a_tag.get_text())

                    link_meta_node = li.find(class_=re.compile("linkMeta"))
                    reply_count = _extract_reply_count(_clean_text(link_meta_node.get_text())) if link_meta_node else 0

                    links.append({
                        "title": link_title,
                        "url": url,
                        "reply_count": reply_count
                    })

        if section_title or links:
            sections.append({
                "title": section_title,
                "summary": section_summary,
                "links": links
            })

    published_at = _extract_chinese_date(meta_text)
    items = []
    for section in sections:
        section_title = section.get("title", "")
        section_summary = section.get("summary", "")
        for link in section.get("links", []):
            items.append({
                "title": link.get("title", ""),
                "url": link.get("url", ""),
                "reply_count": link.get("reply_count", 0),
                "section_title": section_title,
                "section_summary": section_summary,
                "published_at": published_at,
                "daily_url": page_url,
                "daily_title": title or "linux.do 技术聚合日报",
                "daily_headline": daily_headline,
                "daily_overview": overview,
            })

    report = {
        "daily_url": page_url,
        "daily_title": title or "linux.do 技术聚合日报",
        "published_at": published_at,
        "meta_text": meta_text,
        "daily_headline": daily_headline,
        "overview": overview,
        "note": note,
        "highlights": highlights,
        "sections": sections,
        "items": items,
    }

    if not report.get("items"):
        raise ValueError("未解析到 Linux.do 原帖条目")
    return report


def ai_summarize_linux_do_items(items):
    """
    调用 AI 对 Linux.do 日报条目进行二次改写。

    AI 输入只包含 news.linuxe.top 的日报摘要、标题、链接和回复数。
    """
    if not items:
        return items

    if not GITHUB_TOKEN:
        logger.warning("未配置 GITHUB_TOKEN，跳过 Linux.do AI 总结")
        for item in items:
            item["ai_summary"] = _fallback_summary(item)
        return items

    lines = []
    for i, item in enumerate(items, 1):
        lines.append(
            "{}. 分组: {}\n   标题: {}\n   链接: {}\n   回复数: {}\n   日报标题: {}\n   日报摘要: {}".format(
                i,
                item.get("section_title", ""),
                item.get("title", ""),
                item.get("url", ""),
                item.get("reply_count", 0),
                item.get("daily_headline", ""),
                item.get("section_summary", ""),
            )
        )

    prompt = (
        "以下是 news.linuxe.top 已整理出的 Linux.do 技术聚合日报条目。"
        "请只基于这些摘要信息，为每条原帖写中文摘要（60-100 字）。\n\n"
        "要求：\n"
        "- 说清这个讨论为什么值得技术读者点进去看\n"
        "- 不要声称看过原帖正文或回复全文\n"
        "- 对账号风控、模型能力、工程工具、成本策略等话题要直接点出实际影响\n"
        "- 语气像技术日报编辑，不要用营销腔\n\n"
        "请严格按照以下 JSON 格式返回，不要包含任何多余内容：\n"
        '{{"summaries": [{{"index": 1, "summary": "中文摘要"}}, ...]}}\n\n'
        "条目列表：\n{}"
    ).format("\n\n".join(lines))

    try:
        summaries = _call_linux_do_ai_api(prompt)
        if summaries:
            for summary in summaries:
                idx = summary.get("index", 0) - 1
                if 0 <= idx < len(items):
                    items[idx]["ai_summary"] = summary.get("summary", "")
    except Exception as e:
        logger.error("Linux.do AI 总结失败: %s", e)

    for item in items:
        if not item.get("ai_summary"):
            item["ai_summary"] = _fallback_summary(item)
    return items


def _fallback_summary(item):
    section_title = item.get("section_title", "")
    section_summary = item.get("section_summary", "")
    if section_title and section_summary:
        return "{}：{}".format(section_title, section_summary)
    return section_summary or "（AI 总结生成失败）"


def _call_linux_do_ai_api(prompt, max_retries=10):
    """调用 GitHub Models API 进行 Linux.do 摘要。"""
    headers = {
        "Authorization": "Bearer {}".format(GITHUB_TOKEN),
        "Content-Type": "application/json",
    }
    payload = {
        "model": AI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "你是一个关注中文技术社区和 AI 工具链动态的技术日报编辑。"
                           "你只基于用户提供的日报摘要做判断，不补充未提供的事实。"
                           "请始终返回有效 JSON。",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 8000,
    }

    for attempt in range(max_retries):
        try:
            logger.info("调用 AI API 进行 Linux.do 总结 (第 %d 次尝试)...", attempt + 1)
            resp = requests.post(
                "{}/chat/completions".format(AI_API_URL),
                headers=headers,
                json=payload,
                timeout=120,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"].strip()
            json_match = re.search(r"\{.*\}", content, re.DOTALL)
            if json_match:
                content = json_match.group(0)
            return json.loads(content).get("summaries", [])
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else 0
            if status == 429:
                wait = 60 * (attempt + 1)
                logger.warning("Linux.do 摘要 API 限流，等待 %d 秒后重试...", wait)
                time.sleep(wait)
            elif attempt < max_retries - 1:
                logger.error("Linux.do AI API HTTP 错误 %d: %s", status, e)
                time.sleep(5 * (attempt + 1))
            else:
                logger.error("Linux.do AI API HTTP 错误，已放弃: %s", e)
        except Exception as e:
            if attempt < max_retries - 1:
                logger.error("Linux.do AI 总结调用失败: %s", e)
                time.sleep(5 * (attempt + 1))
            else:
                logger.error("Linux.do AI 总结调用失败，已放弃: %s", e)

    return None



def _normalize_topic_url(href, page_url):
    href = href or ""
    if href.startswith("/t/"):
        return urljoin("https://linux.do", href)
    return urljoin(page_url, href)


def _clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


def _extract_reply_count(text):
    match = re.search(r"(\d+)\s*回复", text or "")
    if not match:
        return 0
    return int(match.group(1))


def _extract_chinese_date(text):
    match = re.search(r"(20\d{2})年(\d{1,2})月(\d{1,2})日", text or "")
    if not match:
        return ""
    year, month, day = match.groups()
    return "{}-{:02d}-{:02d}".format(int(year), int(month), int(day))

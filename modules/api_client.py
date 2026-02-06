#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API 调用模块 — OpenAI 兼容格式 chat completions
使用 urllib.request，无外部依赖
"""

import json
import os
import ssl
import urllib.request
import urllib.error


# ── 配置读写 ─────────────────────────────────────────

def load_config(config_path):
    """读取 config.json，不存在则返回空字典"""
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_config(config_path, cfg):
    """保存配置到 config.json"""
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


# ── API 调用 ─────────────────────────────────────────

def call_chat(url, token, model, messages, stream=False, timeout=60):
    """
    调用 OpenAI 兼容 chat completions API。

    参数:
        url      : API endpoint（如 https://api.example.com/v1/chat/completions）
        token    : Bearer token
        model    : 模型名称
        messages : [{"role": "system"|"user"|"assistant", "content": "..."}]
        stream   : 是否流式输出
        timeout  : 超时秒数

    返回（非流式）: str — AI 回复文本
    返回（流式）  : generator — 逐 chunk 产出文本片段
    """
    # 自动补全 URL：用户可能只填了基础地址
    url = url.rstrip("/")
    if not url.endswith("/chat/completions"):
        if url.endswith("/v1"):
            url += "/chat/completions"
        else:
            url += "/v1/chat/completions"

    body = {
        "model": model,
        "messages": messages,
        "stream": stream,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    # 允许自签名证书（用户可能使用本地代理）
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    if stream:
        return _stream_response(req, ctx, timeout)
    else:
        return _blocking_response(req, ctx, timeout)


def _blocking_response(req, ctx, timeout):
    """非流式：等待完整响应"""
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise APIError(f"HTTP {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise APIError(f"网络错误: {e.reason}") from e
    except TimeoutError:
        raise APIError("请求超时")

    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        raise APIError(f"JSON 解析失败: {raw[:200]}")

    # 标准 OpenAI 格式
    try:
        return obj["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise APIError(f"意外的响应结构: {raw[:300]}")


def _stream_response(req, ctx, timeout):
    """流式：逐 chunk 产出文本"""
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=timeout)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise APIError(f"HTTP {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise APIError(f"网络错误: {e.reason}") from e
    except TimeoutError:
        raise APIError("请求超时")

    def _gen():
        try:
            buffer = ""
            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="replace")
                buffer += line
                while "\n" in buffer:
                    one_line, buffer = buffer.split("\n", 1)
                    one_line = one_line.strip()
                    if not one_line:
                        continue
                    if one_line == "data: [DONE]":
                        return
                    if one_line.startswith("data: "):
                        payload = one_line[6:]
                        try:
                            chunk = json.loads(payload)
                            delta = chunk["choices"][0].get("delta", {})
                            text = delta.get("content", "")
                            if text:
                                yield text
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue
        finally:
            resp.close()

    return _gen()


# ── 异常 ─────────────────────────────────────────────

class APIError(Exception):
    """API 调用异常"""
    pass

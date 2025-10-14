set windows-shell := ["sh", "-c"]
set dotenv-load := true

COMMON_JUST_URL := 'https://raw.githubusercontent.com/esclient/tools/refs/heads/main/python/common.just'
LOAD_ENVS_URL := 'https://raw.githubusercontent.com/esclient/tools/refs/heads/main/load_envs.sh'

PROTO_REPO := 'https://raw.githubusercontent.com/esclient/protos'

COMMENT_PROTO_TAG := 'v0.0.8'
COMMENT_PROTO_NAME := 'comment.proto'

USER_PROTO_TAG := 'v0.0.8'
USER_PROTO_NAME := 'user.proto'

RATING_PROTO_TAG := 'v0.0.15'
RATING_PROTO_NAME := 'rating.proto'

MOD_PROTO_TAG := 'v0.1.2'
MOD_PROTO_NAME := 'mod.proto'

TMP_DIR := '.proto'
OUT_DIR := 'src/apigateway/stubs'

MKDIR_TOOLS := 'mkdir -p tools'

FETCH_COMMON_JUST := 'curl -fsSL ' + COMMON_JUST_URL + ' -o tools/common.just'
FETCH_LOAD_ENVS := 'curl -fsSL ' + LOAD_ENVS_URL + ' -o tools/load_envs.sh'

import? 'tools/common.just'

default:
    @just --list

fetch-tools:
    {{ MKDIR_TOOLS }}
    {{ FETCH_COMMON_JUST }}
    {{ FETCH_LOAD_ENVS }}

include .env

COMMENT_PROTO_TAG ?= v0.0.8
COMMENT_PROTO_NAME := comment.proto

USER_PROTO_TAG ?= v0.0.8
USER_PROTO_NAME := user.proto

RATING_PROTO_TAG ?= v0.0.15
RATING_PROTO_NAME := rating.proto

MOD_PROTO_TAG ?= v0.1.0
MOD_PROTO_NAME := mod.proto

PROTO_REPO := https://raw.githubusercontent.com/esclient/protos

TMP_DIR := .proto
OUT_DIR := stubs

ifeq ($(OS),Windows_NT)
MKDIR    = powershell -Command "New-Item -ItemType Directory -Force -Path"
RM       = powershell -NoProfile -Command "Remove-Item -Path '$(TMP_DIR)' -Recurse -Force"
DOWN     = powershell -Command "Invoke-WebRequest -Uri"
DOWN_OUT = -OutFile
FIX_IMPORTS = powershell -Command "& { \
	Get-ChildItem -Path '$(OUT_DIR)' -Filter '*_pb2_grpc.py' | \
	ForEach-Object { \
	(Get-Content $$_.FullName) -replace '^import (.*_pb2)', 'from . import $$1' | \
	Set-Content -Path $$_.FullName -Encoding UTF8 \
	} \
}"
else
MKDIR    = mkdir -p
RM       = rm -rf $(TMP_DIR)
DOWN     = wget
DOWN_OUT = -O
FIX_IMPORTS = \
    for f in $(OUT_DIR)/*_pb2_grpc.py; do \
      sed -i 's/^import \(.*_pb2\)/from . import \1/' $$f; \
    done
endif

.PHONY: clean

$(TMP_DIR) $(OUT_DIR):
	$(MKDIR) "$@"

$(TMP_DIR)/$(COMMENT_PROTO_NAME): | $(TMP_DIR)
	$(DOWN) "$(PROTO_REPO)/$(COMMENT_PROTO_TAG)/$(COMMENT_PROTO_NAME)" $(DOWN_OUT) "$@"

$(TMP_DIR)/$(USER_PROTO_NAME): | $(TMP_DIR)
	$(DOWN) "$(PROTO_REPO)/$(USER_PROTO_TAG)/$(USER_PROTO_NAME)" $(DOWN_OUT) "$@"

$(TMP_DIR)/$(RATING_PROTO_NAME): | $(TMP_DIR)
	$(DOWN) "$(PROTO_REPO)/$(RATING_PROTO_TAG)/$(RATING_PROTO_NAME)" $(DOWN_OUT) "$@"

$(TMP_DIR)/$(MOD_PROTO_NAME): | $(TMP_DIR)
	$(DOWN) "$(PROTO_REPO)/$(MOD_PROTO_TAG)/$(MOD_PROTO_NAME)" $(DOWN_OUT) "$@"


clean:
	$(RM)

update-%: $(TMP_DIR)/%.proto | $(OUT_DIR)
	$(MKDIR) "$(OUT_DIR)"
	pdm run python -m grpc_tools.protoc \
		--proto_path="$(TMP_DIR)" \
		--python_out="$(OUT_DIR)" \
		--grpc_python_out="$(OUT_DIR)" \
		--pyi_out="$(OUT_DIR)" \
		"$(TMP_DIR)/$*.proto"
	$(FIX_IMPORTS)
	$(MAKE) clean

docker-build:
	docker build --build-arg PORT=$(PORT) -t gateway-dev .

run: docker-build
	docker run --rm -it \
		--env-file .env \
		-p $(PORT):$(PORT) \
		-v $(CURDIR):/app \
		-e WATCHFILES_FORCE_POLLING=true \
		gateway-dev



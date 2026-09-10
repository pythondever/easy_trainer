#!/usr/bin/env bash
# EasyTrainer Linux 安装脚本（对应 Windows 端 Win.installer 的组件流程）
#
# 用法: ./installer.sh [-d 安装目录] [-p] [-h]
#   -d  安装根目录（默认 ~/EasyTrainer）
#   -p  同时安装预训练权重（默认跳过；官方 GCS 约 880MB，大陆网络可能失败，失败仅警告）
#   -h  显示帮助
#
# 需与本脚本同目录放置 program.zip、requirements-release.txt、pretrained-assets.txt
# （build.py 的 Linux 发布产物）。默认锁定 CUDA 版 torch，可用 TORCH_INDEX 环境变量换 pytorch 源。
# .so 按 Python 3.10(cp310) 编译，本脚本要求系统 python 恰为 3.10.x，否则拒绝安装。
set -u

PIP_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple"
# requirements 锁了 torch==2.5.1+cu121，该版本只在 pytorch 源有，用 extra-index-url 叠进来
CUDA_INDEX="https://download.pytorch.org/whl/cu121"
VERSION="1.0.0"
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$HOME/EasyTrainer"
WITH_PRETRAINED=0

# 预训练权重表（无共享清单时的兜底）：优先读三端共用的 pretrained-assets.txt（build.py 会一起打包）
declare -a PRETRAINED=( \
  "rf-detr-nano.pth|https://storage.googleapis.com/rfdetr/nano_coco/checkpoint_best_regular.pth|D8D6B9EE57D4D0ED2B1F305163624712A0532CB7BCE0C747317984FC5457440D" \
  "rf-detr-seg-nano.pt|https://storage.googleapis.com/rfdetr/rf-detr-seg-n-ft.pth|A44613A4ECD6B5BA61A62002C600B0B6CB7A9DA2936A45317EC4B62C635FB99B" \
  "rf-detr-seg-small.pt|https://storage.googleapis.com/rfdetr/rf-detr-seg-s-ft.pth|6DE3DA31B2572CAC214A1C76CCE4A92A13966D56390AC2B3A3DE9A8DC2B2BCA3" \
  "rf-detr-seg-medium.pt|https://storage.googleapis.com/rfdetr/rf-detr-seg-m-ft.pth|3AD325094735F431AEE9962A8D204D68EB5BFC393D53E7E836E70998FEF5EA58" \
  "rf-detr-seg-large.pt|https://storage.googleapis.com/rfdetr/rf-detr-seg-l-ft.pth|CA7B7C630BA22496067CC4F034C4E70C8E47FD7ADCEA04C3A49AA8C1755CBE6B" \
)

ASSETS_FILE="$SELF_DIR/pretrained-assets.txt"
if [ -f "$ASSETS_FILE" ]; then
  PRETRAINED=()
  while IFS=$'\t' read -r fname url sha _rest; do
    fname="${fname%$'\r'}"; url="${url%$'\r'}"; sha="${sha%$'\r'}"
    case "$fname" in ''|\#*) continue ;; esac
    if [ -n "$url" ] && [ -n "$sha" ]; then
      PRETRAINED+=("$fname|$url|$sha")
    fi
  done < "$ASSETS_FILE"
fi

LOG_FILE=""
log()  { local l="[$(date '+%H:%M:%S')] $*"; echo "$l"; [ -n "$LOG_FILE" ] && echo "$l" >> "$LOG_FILE" 2>/dev/null || true; }
die()  { log "错误: $*"; exit 1; }
usage(){ sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0; }

while getopts "d:ph" opt; do
  case "$opt" in
    d) ROOT="$OPTARG" ;;
    p) WITH_PRETRAINED=1 ;;
    h) usage ;;
    *) usage ;;
  esac
done

need_cmd() { command -v "$1" >/dev/null 2>&1 || die "缺少命令: $1（请先安装）"; }
need_cmd python3
need_cmd curl

# ── 1. 定位 Python 3.10 ───────────────────────────────────────────────
find_python310() {
  [ -n "${PY:-}" ] && [ -x "$PY" ] && { echo "$PY"; return 0; }
  local cand
  for cand in python3.10 python3; do
    if command -v "$cand" >/dev/null 2>&1 && \
       "$cand" -c 'import sys; raise SystemExit(0 if sys.version_info[:2] == (3,10) else 1)' 2>/dev/null; then
      echo "$cand"; return 0
    fi
  done
  return 1
}
PY="$(find_python310)" || die "需要 Python 3.10（编译产物 .so 按 cp310 ABI）。\n   Ubuntu 22.04+ 可安装: sudo apt install python3.10 python3.10-venv\n   也可用 PY=/path/to/python3.10 ./installer.sh 指定"

# ── 2. 基础准备 ───────────────────────────────────────────────────────
mkdir -p "$ROOT" || die "无法创建安装目录: $ROOT"
LOG_FILE="$ROOT/install.log"
log "EasyTrainer $VERSION 安装开始，目标: $ROOT"
log "Python: $($PY --version 2>&1)"

ZIP="$SELF_DIR/program.zip"
REQ="$SELF_DIR/requirements-release.txt"
[ -f "$ZIP" ] || die "同目录缺少 program.zip（发布不完整）：$ZIP"

# ── 3. 虚拟环境 ───────────────────────────────────────────────────────
VENV_DIR="$ROOT/runtime/venv"
if [ ! -x "$VENV_DIR/bin/python" ]; then
  log "创建虚拟环境 runtime/venv …"
  "$PY" -m venv "$VENV_DIR" 2>/dev/null || die "创建 venv 失败（缺少 python3.10-venv?）:\n   Ubuntu: sudo apt install python3.10-venv"
fi
VPY="$VENV_DIR/bin/python"
VPIP="$VENV_DIR/bin/pip"

# ── 4. 解压程序本体 ───────────────────────────────────────────────────
log "解压程序本体（program.zip）…"
"$VPY" -m zipfile -e "$ZIP" "$ROOT" || die "解压 program.zip 失败"
[ -f "$ROOT/app/easy_trainer.py" ] || die "program.zip 内容异常：缺少 app/easy_trainer.py"

# ── 5. pip 安装依赖 ───────────────────────────────────────────────────
[ -f "$REQ" ] || die "同目录缺少 requirements-release.txt：$REQ"
PIP_LOG="$ROOT/pip-install.log"
log "正在安装 Python 依赖（torch 较大，可能 5~30 分钟，进度见 $PIP_LOG）…"
# requirements 锁的是 torch==2.5.1+cu121（Windows 默认源只有 CPU 版），该版本只在 pytorch 源有，
# 故叠一个 torch 专用 index；其余包仍走国内源。TORCH_INDEX 可从外部覆盖换源。
if ! "$VPIP" install --disable-pip-version-check --timeout 60 --retries 10 -r "$REQ" \
     -i "$PIP_INDEX" --extra-index-url "${TORCH_INDEX:-$CUDA_INDEX}" >> "$PIP_LOG" 2>&1; then
  die "pip 安装依赖失败，详见: $PIP_LOG"
fi
log "Python 依赖安装完成"
command -v nvidia-smi >/dev/null 2>&1 || log "提示: 未检测到 NVIDIA 显卡，CUDA 版 torch 将只以 CPU 模式运行"

# ── 6. 预训练权重（可选）──────────────────────────────────────────────
PRETRAIN_DIR="$ROOT/pretrained"
if [ "$WITH_PRETRAINED" = "1" ]; then
  mkdir -p "$PRETRAIN_DIR"
  if [ -f "$SELF_DIR/pretrained.zip" ]; then
    log "解压同目录 pretrained.zip（离线分发）…"
    "$VPY" -m zipfile -e "$SELF_DIR/pretrained.zip" "$PRETRAIN_DIR" || log "警告: pretrained.zip 解压失败"
  else
    log "在线下载预训练权重（官方 GCS，单文件失败仅警告，重跑可续传）…"
    for entry in "${PRETRAINED[@]}"; do
      IFS='|' read -r fname url sha <<< "$entry"
      target="$PRETRAIN_DIR/$fname"
      if [ -f "$target" ] && echo "$sha  $target" | sha256sum -c --status 2>/dev/null; then
        log "  $fname 已就绪，跳过"; continue
      fi
      if curl -fL --retry 2 -C - -o "$target.part" "$url" >> "$LOG_FILE" 2>&1; then
        mv "$target.part" "$target"
        if echo "$sha  $target" | sha256sum -c --status 2>/dev/null; then
          log "  $fname 完成"
        else
          rm -f "$target"; log "  警告: $fname SHA256 校验失败，已删除"
        fi
      else
        rm -f "$target.part"; log "  警告: $fname 下载失败（网络？），重跑 installer.sh -p 可续传"
      fi
    done
  fi
else
  log "跳过预训练权重（如需: ./installer.sh -p）"
fi

# ── 7. 桌面启动项 + installed.json ────────────────────────────────────
SCRIPT_FILE="$ROOT/app/easy_trainer.py"
desktop_dir="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$desktop_dir"
icon=""
for f in "$ROOT"/resources/*.png "$ROOT"/resources/*.svg; do
  [ -f "$f" ] && { icon="$f"; break; }
done
DESKTOP_ENTRY="[Desktop Entry]
Type=Application
Name=EasyTrainer
Comment=EasyTrainer 标注/训练工具
Exec=\"$VPY\" \"$SCRIPT_FILE\"
Path=$ROOT
Terminal=false
Categories=Development;Graphics;"
if [ -n "$icon" ]; then DESKTOP_ENTRY="$DESKTOP_ENTRY
Icon=$icon"; fi
printf '%s\n' "$DESKTOP_ENTRY" > "$desktop_dir/easy-trainer.desktop"
chmod +x "$desktop_dir/easy-trainer.desktop"
for d in "$HOME/Desktop" "$HOME/桌面"; do
  if [ -d "$d" ]; then
    cp "$desktop_dir/easy-trainer.desktop" "$d/" && chmod +x "$d/easy-trainer.desktop" 2>/dev/null
    break
  fi
done
log "已创建启动项: $desktop_dir/easy-trainer.desktop"

COMP_STR="runtime,program"
[ "$WITH_PRETRAINED" = "1" ] && COMP_STR="$COMP_STR,pretrained"
"$VPY" - "$ROOT" "$VERSION" "$COMP_STR" <<'PY' || die "写入 installed.json 失败"
import json, sys, datetime
root, ver, comps = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
json.dump({"app": "EasyTrainer", "version": ver,
           "installedAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           "components": [c for c in comps if c]},
          open(root + "/installed.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
PY

log "全部完成。启动方式: $VPY \"$SCRIPT_FILE\"（或在应用菜单中打开 EasyTrainer）"

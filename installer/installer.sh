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
# 重复安装 = 覆盖升级：开始前先清掉 app/ ui/ 下的旧 .so 与明文 .py（否则上一版已删除的模块会被继续 import），
# 并在解压前做磁盘空间预检（装运行时约需 10GB）。venv 与已装依赖保留复用。
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
# 消息里的 \n 要真展开成换行：bash 的 echo 不带 -e 不解释转义，直接 log 会把 \n 打成字面量
die()  { while IFS= read -r _l; do log "$_l"; done <<< "$(printf '%b' "错误: $*")"; exit 1; }
# 帮助文本直接取头部注释块（读到 set -u 为止），不写死行号，增删注释行也不会错位
usage(){
  local n=0 line
  while IFS= read -r line; do
    n=$((n + 1)); [ "$n" -eq 1 ] && continue
    [ "$line" = "set -u" ] && break
    # case 的 pattern 是整串匹配，剥前缀要带通配符（写成 '# ' 只会匹配恰好两字符的那行）
    case "$line" in
      '# '*) line="${line#'# '}" ;;
      '#')   line="" ;;
    esac
    printf '%s\n' "$line"
  done < "$0"
  exit 0
}

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

human_kb() { awk -v k="${1:-0}" 'BEGIN{ if (k >= 1048576) printf "%.1fGB", k/1048576; else printf "%.0fMB", k/1024 }'; }

# 解压是覆盖式的，上一版遗留的 .so / 明文 .py 不会被清掉，但导入优先级是 扩展模块 > 源码，
# 于是新版已删除的模块会被旧产物"复活"（改了代码没生效 / 幽灵模块）。只清 app、ui 两棵子树。
clean_old_build() {
  local dirs=() nso npy
  [ -d "$ROOT/app" ] && dirs+=("$ROOT/app")
  [ -d "$ROOT/ui" ] && dirs+=("$ROOT/ui")
  [ "${#dirs[@]}" -eq 0 ] && return 0
  nso=$(find "${dirs[@]}" \( -name '*.so' -o -name '*.pyd' \) 2>/dev/null | wc -l)
  npy=$(find "${dirs[@]}" -name '*.py' ! -name '__init__.py' ! -name 'easy_trainer.py' 2>/dev/null | wc -l)
  if [ "$((nso + npy))" -gt 0 ]; then
    find "${dirs[@]}" \( -name '*.so' -o -name '*.pyd' -o -name '*.pyc' \) -delete 2>/dev/null
    find "${dirs[@]}" -name '*.py' ! -name '__init__.py' ! -name 'easy_trainer.py' -delete 2>/dev/null
    find "${dirs[@]}" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null
    log "已清理上一版残留: $nso 个 .so/.pyd, $npy 个旧 .py"
  fi
  return 0
}

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
# 后面 clean_old_build 会按 ROOT 清旧产物，先把指到根目录/家目录本身的写法挡住。
# 先去掉尾斜杠，否则 -d /root/ 会绕过等值判断（"//" 这类要反复剥，剥空即命中）
while [ "${ROOT%/}" != "$ROOT" ]; do ROOT="${ROOT%/}"; done
if [ -z "$ROOT" ] || [ "$ROOT" = "${HOME%/}" ]; then
  die "安装目录不合理: ${ROOT:-<空>}\n   请用 -d 指定一个专用子目录（默认 $HOME/EasyTrainer）"
fi
mkdir -p "$ROOT" || die "无法创建安装目录: $ROOT"
LOG_FILE="$ROOT/install.log"
log "EasyTrainer $VERSION 安装开始，目标: $ROOT"
log "Python: $($PY --version 2>&1)"

ZIP="$SELF_DIR/program.zip"
REQ="$SELF_DIR/requirements-release.txt"
[ -f "$ZIP" ] || die "同目录缺少 program.zip（发布不完整）：$ZIP"

# 空间预检：装到一半才发现磁盘满，会留下一个半残的 venv。口径与 Windows 安装器一致
# （RuntimeInstalledBytes=9GB + 各组件体积；程序本体按 zip 解压后的实际大小）
prog_kb=$("$PY" -c 'import sys,zipfile;print(sum(i.file_size for i in zipfile.ZipFile(sys.argv[1]).infolist())//1024)' "$ZIP" 2>/dev/null) || prog_kb=0
case "$prog_kb" in ''|*[!0-9]*) prog_kb=0 ;; esac
need_kb=$((prog_kb + 9 * 1024 * 1024))
[ "$WITH_PRETRAINED" = "1" ] && need_kb=$((need_kb + 880 * 1024))
free_kb=$(df -Pk "$ROOT" 2>/dev/null | awk 'NR==2 {print $4}')
case "$free_kb" in ''|*[!0-9]*) free_kb="" ;; esac
if [ -n "$free_kb" ] && [ "$free_kb" -lt "$need_kb" ]; then
  die "磁盘空间不足: 本次安装约需 $(human_kb "$need_kb")，$ROOT 所在分区当前可用 $(human_kb "$free_kb")。\n   请用 -d 换一个空间充足的目录，或清理磁盘后重试"
fi
log "空间检查通过: 需约 $(human_kb "$need_kb")${free_kb:+，可用 $(human_kb "$free_kb")}"

# ── 3. 虚拟环境 ───────────────────────────────────────────────────────
VENV_DIR="$ROOT/runtime/venv"
if [ ! -x "$VENV_DIR/bin/python" ]; then
  log "创建虚拟环境 runtime/venv …"
  "$PY" -m venv "$VENV_DIR" 2>/dev/null || die "创建 venv 失败（缺少 python3.10-venv?）:\n   Ubuntu: sudo apt install python3.10-venv"
fi
VPY="$VENV_DIR/bin/python"
VPIP="$VENV_DIR/bin/pip"

# ── 4. 解压程序本体 ───────────────────────────────────────────────────
clean_old_build
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

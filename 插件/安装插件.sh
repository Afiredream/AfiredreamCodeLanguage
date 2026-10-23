#!/usr/bin/env bash
#
# 燃梦中文语言 VSCode 插件安装脚本
#
# 用法：
#   ./安装插件.sh                自动探测编辑器并安装
#   ./安装插件.sh --列表          列出可安装的位置，不做改动
#   ./安装插件.sh --目标 <目录>   安装到指定的扩展目录
#   ./安装插件.sh --卸载          从已探测到的位置移除
#
# 安装优先走命令行（code --install-extension），失败时自动改为直接复制。
# 脚本只在你指定或探测到的扩展目录里增删文件，不修改系统配置。
#
# 说明：bash 不支持中文变量名，所以变量用英文，函数名用中文。

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$SCRIPT_DIR/vscode-燃梦中文语言"
PLUGIN_NAME="ranmeng-chinese-language"
PLUGIN_VERSION="0.1.0"
INSTALL_DIR_NAME="${PLUGIN_NAME}-${PLUGIN_VERSION}"

if [ -t 1 ]; then
    GREEN=$'\033[32m'; YELLOW=$'\033[33m'; RED=$'\033[31m'; GREY=$'\033[90m'; RESET=$'\033[0m'
else
    GREEN=""; YELLOW=""; RED=""; GREY=""; RESET=""
fi

提示() { printf '%s\n' "${GREEN}==>${RESET} $*"; }
警告() { printf '%s\n' "${YELLOW}注意：${RESET}$*"; }
错误() { printf '%s\n' "${RED}错误：${RESET}$*" >&2; }
说明() { printf '%s\n' "${GREY}    $*${RESET}"; }

# ── 参数解析 ──────────────────────────────────────────────

TARGET_DIR=""
ACTION="install"

while [ $# -gt 0 ]; do
    case "$1" in
        --列表|--list)       ACTION="list"; shift ;;
        --卸载|--uninstall)  ACTION="uninstall"; shift ;;
        --目标|--target)
            if [ $# -lt 2 ]; then 错误 "--目标 需要跟一个目录"; exit 1; fi
            TARGET_DIR="$2"; shift 2 ;;
        -h|--帮助|--help)
            sed -n '3,14p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
            exit 0 ;;
        *) 错误 "未知参数：$1（用 --帮助 查看用法）"; exit 1 ;;
    esac
done

# ── 检查插件文件 ──────────────────────────────────────────

if [ ! -d "$PLUGIN_DIR" ]; then
    错误 "找不到插件目录：$PLUGIN_DIR"
    exit 1
fi

for REQUIRED in package.json syntaxes/ranmeng.tmLanguage.json \
                language-configuration/language-configuration.json; do
    if [ ! -f "$PLUGIN_DIR/$REQUIRED" ]; then
        错误 "插件缺少文件：$REQUIRED"
        exit 1
    fi
done

# ── 探测真实主目录与扩展目录 ──────────────────────────────

REAL_HOME=""
if PW_ENTRY=$(getent passwd "$(id -un)" 2>/dev/null); then
    REAL_HOME=$(printf '%s' "$PW_ENTRY" | cut -d: -f6)
fi
[ -n "$REAL_HOME" ] || REAL_HOME="$HOME"

CANDIDATES=()
for DIR in \
    "${CODIUM_EXTENSIONS_DIR:-}" \
    "${VSCODE_EXTENSIONS_DIR:-}" \
    "$REAL_HOME/.vscode-oss/extensions" \
    "$REAL_HOME/.vscode/extensions" \
    "$REAL_HOME/.vscode-insiders/extensions" \
    "$REAL_HOME/.codium/extensions" \
    "$REAL_HOME/.config/Codium/extensions" \
    "$REAL_HOME/.config/Code/extensions" \
    "$HOME/.vscode-oss/extensions" \
    "$HOME/.vscode/extensions"; do
    [ -n "$DIR" ] && CANDIDATES+=("$DIR")
done

EXT_DIRS=()
for DIR in "${CANDIDATES[@]}"; do
    DUP=0
    for SEEN in "${EXT_DIRS[@]:-}"; do
        [ "$SEEN" = "$DIR" ] && DUP=1 && break
    done
    [ $DUP -eq 0 ] && EXT_DIRS+=("$DIR")
done

CLI_TOOLS=()
for TOOL in code codium code-oss; do
    command -v "$TOOL" >/dev/null 2>&1 && CLI_TOOLS+=("$TOOL")
done

# ── 列表模式 ──────────────────────────────────────────────

if [ "$ACTION" = "list" ]; then
    提示 "插件位置：$PLUGIN_DIR"
    echo
    echo "可用的命令行工具："
    if [ ${#CLI_TOOLS[@]} -eq 0 ]; then
        说明 "（没有找到 code / codium / code-oss）"
    else
        for TOOL in "${CLI_TOOLS[@]}"; do
            说明 "$TOOL -> $(command -v "$TOOL")"
        done
    fi
    echo
    echo "候选扩展目录："
    for DIR in "${EXT_DIRS[@]}"; do
        if [ -d "$DIR" ]; then
            说明 "$DIR  ${GREEN}(已存在)${RESET}"
        else
            说明 "$DIR  ${GREY}(可以创建)${RESET}"
        fi
    done
    echo
    echo "已安装的情况："
    FOUND=0
    for DIR in "${EXT_DIRS[@]}"; do
        if [ -d "$DIR/$INSTALL_DIR_NAME" ]; then
            说明 "$DIR/$INSTALL_DIR_NAME"
            FOUND=1
        fi
    done
    [ $FOUND -eq 0 ] && 说明 "尚未安装"
    exit 0
fi

# ── 卸载模式 ──────────────────────────────────────────────

if [ "$ACTION" = "uninstall" ]; then
    提示 "卸载燃梦中文语言插件"
    REMOVED=0
    for DIR in "${EXT_DIRS[@]}"; do
        for TARGET in "$DIR/$INSTALL_DIR_NAME" "$DIR/$PLUGIN_NAME"*/; do
            if [ -d "$TARGET" ] && [ -f "$TARGET/package.json" ]; then
                rm -rf "$TARGET"
                printf '  已删除 %s\n' "$TARGET"
                REMOVED=$((REMOVED + 1))
            fi
        done
    done
    for TOOL in "${CLI_TOOLS[@]:-}"; do
        [ -z "$TOOL" ] && continue
        if "$TOOL" --list-extensions 2>/dev/null | grep -qx "$PLUGIN_NAME"; then
            if "$TOOL" --uninstall-extension "$PLUGIN_NAME" >/dev/null 2>&1; then
                printf '  已通过 %s 卸载\n' "$TOOL"
                REMOVED=$((REMOVED + 1))
            fi
        fi
    done
    if [ $REMOVED -eq 0 ]; then
        警告 "没有找到已安装的插件"
    else
        提示 "卸载完成，重启编辑器后生效"
    fi
    exit 0
fi

# ── 安装：直接复制 ────────────────────────────────────────

复制安装() {
    local ext_dir="$1"
    local target="$ext_dir/$INSTALL_DIR_NAME"

    if ! mkdir -p "$ext_dir" 2>/dev/null; then
        错误 "无法创建目录：$ext_dir（可能需要权限）"
        return 1
    fi
    if [ ! -w "$ext_dir" ]; then
        错误 "目录不可写：$ext_dir"
        return 1
    fi

    rm -rf "$target"
    if ! cp -R "$PLUGIN_DIR" "$target" 2>/dev/null; then
        错误 "复制文件失败：$target"
        return 1
    fi

    if [ ! -f "$target/package.json" ]; then
        错误 "安装后缺少 package.json"
        rm -rf "$target"
        return 1
    fi
    printf '  已复制到 %s\n' "$target"
    return 0
}

# ── 安装：命令行 ──────────────────────────────────────────

打包VSIX() {
    local out="$SCRIPT_DIR/${PLUGIN_NAME}-${PLUGIN_VERSION}.vsix"
    rm -f "$out"

    if command -v npx >/dev/null 2>&1; then
        if (cd "$PLUGIN_DIR" && npx --yes @vscode/vsce package \
                --allow-missing-repository -o "$out" >/dev/null 2>&1) \
                && [ -f "$out" ]; then
            printf '%s' "$out"
            return 0
        fi
    fi

    if command -v zip >/dev/null 2>&1; then
        rm -f "$out"
        if (cd "$PLUGIN_DIR" && zip -qr "$out" .) >/dev/null 2>&1 && [ -f "$out" ]; then
            printf '%s' "$out"
            return 0
        fi
    fi
    return 1
}

命令行安装() {
    local tool="$1"
    local pkg
    if ! pkg=$(打包VSIX); then
        return 1
    fi
    printf '  已打包 %s\n' "$pkg"
    if "$tool" --install-extension "$pkg" --force >/dev/null 2>&1; then
        printf '  已通过 %s 安装\n' "$tool"
        rm -f "$pkg"
        return 0
    fi
    rm -f "$pkg"
    return 1
}

# ── 开始安装 ──────────────────────────────────────────────

提示 "安装燃梦中文语言插件"

INSTALLED_AT=""

if [ -n "$TARGET_DIR" ]; then
    if 复制安装 "$TARGET_DIR"; then
        INSTALLED_AT="$TARGET_DIR"
    else
        exit 1
    fi
else
    SUCCESS=0

    for TOOL in "${CLI_TOOLS[@]:-}"; do
        [ -z "$TOOL" ] && continue
        if 命令行安装 "$TOOL"; then
            SUCCESS=1
            INSTALLED_AT="（由 $TOOL 管理）"
            break
        fi
    done

    if [ $SUCCESS -eq 0 ]; then
        [ ${#CLI_TOOLS[@]} -gt 0 ] && 警告 "命令行安装没有成功，改用直接复制"
        for DIR in "${EXT_DIRS[@]}"; do
            if 复制安装 "$DIR"; then
                SUCCESS=1
                INSTALLED_AT="$DIR"
                break
            fi
        done
    fi

    if [ $SUCCESS -eq 0 ]; then
        错误 "所有安装方式都失败了"
        说明 "可以手动指定可写的目录：./安装插件.sh --目标 <扩展目录>"
        exit 1
    fi
fi

echo
提示 "安装完成"
说明 "位置：$INSTALLED_AT"
echo
说明 "重启编辑器后，打开 .象 或 .燃梦 文件即可看到语法高亮"

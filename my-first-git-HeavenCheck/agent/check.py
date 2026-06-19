import os
import json
import cv2
import numpy as np
from maa import Tasker, Controller, Resource
# ========================
# 1. 读取外部关键词
# ========================
# 使用绝对路径或正确的相对路径
KEYWORD_FILE = r"E:\Software_tools\DevSpace\Projects\Script\my-first-git-HeavenCheck\txt\神秘数字.txt"

def load_keyword(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines()]
        for l in lines:
            if l:
                return l
        raise ValueError("神秘数字.txt 为空或未读到有效关键词")
    except FileNotFoundError:
        raise FileNotFoundError(f"找不到文件: {path}")

keyword = load_keyword(KEYWORD_FILE)
print(f"[INFO] 读取到关键词: {keyword}")

# ========================
# 2. 初始化 Maa 核心对象（新版写法）
# ========================
tasker = Tasker()
controller = Controller(address="127.0.0.1:16416")  # 确认这是你的 MuMu 端口

# ✅ 使用 Windows 绝对路径（根据你的实际路径调整）
resource_path = r"E:\Software_tools\DevSpace\Projects\Script\my-first-git-HeavenCheck\resource"
resource = Resource(path=resource_path)

# ✅ 新版本绑定方式（无需 MaaInstance）
tasker.bind_controller(controller)
tasker.bind_resource(resource)

print("[INFO] Maa 核心对象初始化完成")

# ========================
# 3. 加载并注入 Pipeline
# ========================
# ✅ 使用 Windows 绝对路径
pipeline_path = r"E:\Software_tools\DevSpace\Projects\Script\my-first-git-HeavenCheck\assets\resource\pipeline\start.json"

try:
    with open(pipeline_path, "r", encoding="utf-8") as f:
        pipeline_obj = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"找不到 Pipeline 文件: {pipeline_path}")

# 替换 {{KEYWORD}} 占位符
pipe_str = json.dumps(pipeline_obj, ensure_ascii=False)
pipe_str = pipe_str.replace("{{KEYWORD}}", keyword)
injected_pipeline = json.loads(pipe_str)

# ✅ 正确注入方式
resource.override_pipeline(injected_pipeline)
print("[INFO] Pipeline 注入完成")

# ========================
# 4. 执行任务
# ========================
print("[INFO] 开始执行任务: 打开JMComic2")
tid = tasker.post_task("打开JMComic2")
status = tasker.wait_task(tid)

print(f"[INFO] 任务结束，状态码: {status}")

# ========================
# 5. 截图保存
# ========================
img_bytes = controller.screencap()
if img_bytes:
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    save_path = os.path.join(os.getcwd(), f"result_{keyword}.png")
    cv2.imwrite(save_path, img)
    print(f"[INFO] 截图已保存: {save_path}")
else:
    print("[WARN] 截图失败，未获取到图像数据")

# ========================
# 6. 清理资源（可选）
# ========================
# 如果需要多次运行，可以在这里添加清理逻辑
# tasker.clear()
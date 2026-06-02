# 百度智能云 OCR 使用说明

## 配置方式

两种方法任选一种：

### 方法一：填 API Key + Secret Key（推荐）
在设置页直接填「百度 API Key」和「百度 Secret Key」，代码会自动换取 access_token 并使用。

### 方法二：直接填 access_token
如果不想暴露 API Key，或者已有保存的 token：

1. 在浏览器打开以下链接（替换成你的 Key）：
   ```
   https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=你的APIKey&client_secret=你的SecretKey
   ```
2. 页面会返回一段 JSON，复制其中的 `access_token` 值（长字符串）
3. 粘到设置页的「Access Token（可选）」输入框

## 注意事项
- access_token 有效期 **30 天**，过期后需要重新获取
- API Key 和 Secret Key 在百度智能云控制台 → 文字识别 → 应用列表 查看
- 前端调用会暴露 API Key，家庭自用无影响

"""
🔌 MODEL CONTEXT PROTOCOL (MCP) SERVER MODULE
Mô phỏng kiến trúc MCP Server (Client-Server Architecture) cung cấp công cụ chuẩn hóa.
"""

import json
import sys
from typing import Dict, Any, List
from tools import TOOLS_SCHEMA, dispatch_tool_call

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class MCPAcademicServer:
    """
    Giả lập MCP Server tuân thủ chuẩn giao thức Model Context Protocol
    """
    def __init__(self, server_name: str = "supply-chain-mcp-server"):
        self.server_name = server_name
        self.version = "2026.1.0"
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """Trả về danh sách các Tools chuẩn giao thức MCP"""
        return TOOLS_SCHEMA

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Thực thi request gọi Tool theo chuẩn MCP JSON-RPC.
        """
        raw_result = dispatch_tool_call(tool_name, arguments)

        try:
            content = json.loads(raw_result)
        except json.JSONDecodeError:
            content = {
                "status": "INVALID_RESPONSE",
                "message": raw_result
            }

        return {
            "jsonrpc": "2.0",
            "server": self.server_name,
            "tool": tool_name,
            "result": content
        }
        # --------------------------------------------------------------------------
        # TODO 2.1: HỌC VIÊN HOÀN THIỆN HÀM GỌI TOOL CHUẨN MCP JSON-RPC
        # 🎯 YÊU CẦU THỰC THI THUẬT TOÁN:
        # 1. Gọi hàm dispatch_tool_call(tool_name, arguments) để lấy chuỗi JSON kết quả từ Tool Router.
        # 2. Chuyển đổi chuỗi JSON kết quả thành Python Dictionary (dùng json.loads).
        # 3. Đóng gói phản hồi và trả về Dict theo đúng chuẩn giao thức MCP JSON-RPC 2.0:
        #    - Các trường bắt buộc: "jsonrpc": "2.0", "server": self.server_name, "tool": tool_name, "result": content
        # --------------------------------------------------------------------------


if __name__ == "__main__":
    print("==========================================================")
    print("🔌 KIỂM THỬ ĐỘC LẬP MCP SERVER (supply-chain-mcp-server)")
    print("==========================================================")
    
    server = MCPAcademicServer(server_name="supply-chain-mcp-server")
    tools = server.list_tools()
    print(f"✅ Khởi tạo thành công MCP Server: {server.server_name} (Version: {server.version})")
    print(f"📦 Số lượng Tools công bố: {len(tools)}")
    
    for tool_name in ["track_order", "get_warehouse_location", "update_order_status"]:
        tool = next((t for t in tools if t.get("name") == tool_name), None)
        if tool and tool.get("parameters", {}).get("properties"):
            print(f"✅ [SCHEMA OK]: Tool '{tool_name}' đã có schema đầy đủ.")
        else:
            print(f"⏳ [SCHEMA TODO]: Tool '{tool_name}' chưa được định nghĩa đầy đủ.")

    test_result = server.call_tool("track_order", {"tracking_code": "VN2026001"})
    if not test_result:
        print("⏳ [CALL_TOOL]: Hàm call_tool() đang trả về rỗng.")
    else:
        print(f"✅ [CALL_TOOL]: Test dispatch tool 'track_order' thành công:")
        print(f"   Phản hồi JSON-RPC: {json.dumps(test_result, ensure_ascii=False)}")

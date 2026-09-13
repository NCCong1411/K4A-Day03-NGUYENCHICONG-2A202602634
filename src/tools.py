"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    {
        "name": "track_order",
        "description": "Tra cứu chi tiết đơn hàng và mã vận đơn bằng mã vận đơn hoặc mã đơn hàng.",
        "parameters": {
            "type": "object",
            "properties": {
                "tracking_code": {
                    "type": "string",
                    "description": "Mã vận đơn cần tra cứu (ví dụ: 'VN2026001')"
                },
                "order_id": {
                    "type": "string",
                    "description": "Mã đơn hàng nếu người dùng cung cấp (ví dụ: 'DH-2026-001')"
                }
            },
            "required": []
        }
    },
    {
        "name": "get_warehouse_location",
        "description": "Tra cứu vị trí lưu kho hiện tại của một đơn hàng hoặc mã vận đơn.",
        "parameters": {
            "type": "object",
            "properties": {
                "tracking_code": {
                    "type": "string",
                    "description": "Mã vận đơn cần kiểm tra vị trí lưu kho"
                },
                "order_id": {
                    "type": "string",
                    "description": "Mã đơn hàng nếu người dùng cung cấp"
                }
            },
            "required": []
        }
    },
    {
        "name": "update_order_status",
        "description": "Cập nhật trạng thái mới cho đơn hàng và ghi lại nhật ký xử lý kho vận.",
        "parameters": {
            "type": "object",
            "properties": {
                "tracking_code": {
                    "type": "string",
                    "description": "Mã vận đơn cần cập nhật trạng thái"
                },
                "order_id": {
                    "type": "string",
                    "description": "Mã đơn hàng nếu người dùng cung cấp"
                },
                "new_status": {
                    "type": "string",
                    "description": "Trạng thái mới của đơn hàng (ví dụ: 'Đang giao hàng', 'Đã giao', 'Đang đóng gói')"
                },
                "note": {
                    "type": "string",
                    "description": "Ghi chú bổ sung cho cập nhật trạng thái"
                }
            },
            "required": ["new_status"]
        }
    }
]
    
    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - student_id (string): Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')
    #    - datetime_str (string): Thời gian hẹn (ví dụ: '14:00 15/09/2026')
    #    - advisor_name (string): Tên cố vấn học tập
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "VN2026001": {
        "tracking_code": "VN2026001",
        "order_id": "DH-2026-001",
        "customer_name": "Nguyễn Văn An",
        "item": "Laptop Dell XPS 13",
        "quantity": 1,
        "warehouse_location": "Kho Hà Nội - Tầng 2 - Khu A",
        "status": "Đang đóng gói",
        "destination": "TP.HCM",
        "eta": "2026-09-15",
        "carrier": "Giao hàng nhanh"
    },
    "VN2026002": {
        "tracking_code": "VN2026002",
        "order_id": "DH-2026-002",
        "customer_name": "Trần Thị Bình",
        "item": "Điện thoại Samsung Galaxy S24",
        "quantity": 1,
        "warehouse_location": "Kho Đà Nẵng - Khu B1",
        "status": "Đang vận chuyển",
        "destination": "Hà Nội",
        "eta": "2026-09-16",
        "carrier": "Giao hàng tiết kiệm"
    }
}


def _normalize(value: str) -> str:
    return (value or "").strip().upper()


def _find_order(tracking_code: str = "", order_id: str = "") -> Dict[str, Any]:
    normalized_tracking_code = _normalize(tracking_code)
    normalized_order_id = (order_id or "").strip().upper()

    if normalized_tracking_code and normalized_tracking_code in MOCK_DATABASE:
        return MOCK_DATABASE[normalized_tracking_code]

    for order in MOCK_DATABASE.values():
        if normalized_order_id and order.get("order_id", "").upper() == normalized_order_id:
            return order

    return {}


def execute_track_order(tracking_code: str = "", order_id: str = "") -> str:
    """Thực thi tra cứu chi tiết đơn hàng theo mã vận đơn hoặc mã đơn hàng."""
    order = _find_order(tracking_code, order_id)
    if order:
        return json.dumps({
            "status": "SUCCESS",
            "tracking_code": order.get("tracking_code", tracking_code or ""),
            "data": order
        }, ensure_ascii=False)

    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Không tìm thấy dữ liệu đơn hàng với mã vận đơn hoặc mã đơn hàng '{tracking_code or order_id}'."
    }, ensure_ascii=False)


def execute_get_warehouse_location(tracking_code: str = "", order_id: str = "") -> str:
    """Thực thi tra cứu vị trí lưu kho hiện tại của đơn hàng."""
    order = _find_order(tracking_code, order_id)
    if order:
        return json.dumps({
            "status": "SUCCESS",
            "tracking_code": order.get("tracking_code", tracking_code or ""),
            "data": {
                "tracking_code": order.get("tracking_code"),
                "order_id": order.get("order_id"),
                "warehouse_location": order.get("warehouse_location"),
                "status": order.get("status"),
                "destination": order.get("destination")
            }
        }, ensure_ascii=False)

    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Không tìm thấy dữ liệu vị trí lưu kho cho mã vận đơn hoặc mã đơn hàng '{tracking_code or order_id}'."
    }, ensure_ascii=False)


def execute_update_order_status(tracking_code: str = "", order_id: str = "", new_status: str = "", note: str = "") -> str:
    """Thực thi cập nhật trạng thái đơn hàng."""
    order = _find_order(tracking_code, order_id)
    if not order:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu đơn hàng để cập nhật với mã vận đơn hoặc mã đơn hàng '{tracking_code or order_id}'."
        }, ensure_ascii=False)

    order["status"] = new_status
    order["last_note"] = note or "Cập nhật trạng thái theo yêu cầu của đội vận hành"

    return json.dumps({
        "status": "SUCCESS",
        "tracking_code": order.get("tracking_code", tracking_code or ""),
        "data": {
            "tracking_code": order.get("tracking_code"),
            "order_id": order.get("order_id"),
            "status": order.get("status"),
            "last_note": order.get("last_note"),
            "warehouse_location": order.get("warehouse_location")
        },
        "message": f"Đã cập nhật trạng thái đơn hàng {order.get('tracking_code')} thành '{new_status}'."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "track_order": execute_track_order,
    "get_warehouse_location": execute_get_warehouse_location,
    "update_order_status": execute_update_order_status
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)

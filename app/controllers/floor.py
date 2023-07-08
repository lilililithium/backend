from fastapi import APIRouter
from app.schemas import FloorPlanInputSchema, FloorPlanOutputSchema, FurniturePosition, Furniture

router = APIRouter()

# 家具のリストを受け取り、床の上に配置した家具のリストを返す
@router.post("/floor/generate")
def generate_floor_plan(
    floor_info: FloorPlanInputSchema,
) -> FloorPlanOutputSchema:
    # 配置する家具のリスト{name, width, length}
    furniture_list = floor_info.furnitures
    # 部屋の縦横の長さ
    floor_width = floor_info.floor.width
    floor_length = floor_info.floor.length

    furniture_position_list = []
    for furniture in furniture_list:
        furniture_postion = FurniturePosition(
            name=furniture.name,
            width=furniture.width,
            length=furniture.length,
            # とりあえず原点に配置
            x=0,
            y=0
        )
        furniture_position_list.append(furniture_postion)
    
    return FloorPlanOutputSchema(floor=floor_info.floor, furniture=furniture_position_list)

# 家具のリストを取得
@router.get("/floor/furnitures")
def get_furnitures() -> list[Furniture]:
    furnitures = [
        Furniture(
            name="Chair",
            width=0.5,
            length=0.5
        ),
        Furniture(
            name="Table",
            width=1.0,
            length=1.0
        )
    ]
    return furnitures
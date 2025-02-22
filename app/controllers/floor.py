from fastapi import APIRouter
from app.schemas import FloorPlanInputSchema, FloorPlanOutputSchema, FurniturePlace, Furniture
from app.furniture_data import furniture_list_all
from app.AI import generate_room, squeeze_room, get_position
router = APIRouter()

# 家具のリストを受け取り、床の上に配置した家具のリストを返す
@router.post("/floor/generate")
def generate_floor_plan(
    floor_info: FloorPlanInputSchema,
) -> FloorPlanOutputSchema:
    """
    ### 間取り生成用のAPI
    #### リクエスト
    - ***floor***: 床面積の情報
    - ***furnitures***: 家具のリスト
    家具の数をquantityで指定することで、同じ家具を複数個配置することができる
    ある家具の数が1個以上のときに含める

    #### レスポンス
    - ***floor***: 床面積の情報
    - ***furnitures***: 家具のリスト (家具の位置情報を含む)
    """
    # 配置する家具のリスト{name, width, length}
    furniture_list = []
    #print(f'''FLOOR INFO FURNITURES : {floor_info.furnitures}''')
    for furniture in floor_info.furnitures:
        for i in range(furniture.quantity):
            #print(f'''APPEND FURNITURE : {furniture_list_all[furniture.id]}''')
            furniture_list.append(furniture_list_all[furniture.id])
    # 部屋の縦横の長さ
    #print("-----><-----")
    floor_width = floor_info.floor.width
    floor_length = floor_info.floor.length
    #ランダムに家具の配置を作成
    #print(f'''INPUT : {furniture_list}''')
    generated_room = generate_room(room_width=floor_width, room_length=floor_length, furnitures=furniture_list, generate_num=1)
    #AIによりベストな家具配置を見つける
    squeezed_room = generated_room.iloc[squeeze_room(generated_room)]

    furniture_position_list = []
    #各家具の出現数を数えるための辞書
    name_counter = {}
    for furniture in furniture_list:
        if furniture.name not in name_counter:
            name_counter[furniture.name] = 1
        else:
            name_counter[furniture.name] += 1
        #ベストな家具配置パターンの家具の位置を取得
        x, y, rotation = get_position(furniture.name, name_counter, squeezed_room)
        furniture_postion = FurniturePlace(
            id = 0, #ダミーデータ
            name=furniture.name,
            width=furniture.width,
            length=furniture.length,
            x=x,
            y=y,
            rotation=rotation,
            restriction = "",
            rotation_range = [0]
        )
        furniture_position_list.append(furniture_postion)
    
    return FloorPlanOutputSchema(floor=floor_info.floor, furnitures=furniture_position_list)

# 家具のリストを取得
@router.get("/floor/furnitures")
def get_furnitures() -> list[Furniture]:
    """
    ### 使用できる家具のリストを取得するAPI
    #### レスポンス
    [id, name, width, length]をカラムに持つオブジェクトが複数個入った配列が返ってくる
    """
    return furniture_list_all

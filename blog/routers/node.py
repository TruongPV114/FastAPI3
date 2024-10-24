from typing import List
from fastapi import APIRouter, Depends,status,HTTPException
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
import csv
import os

router = APIRouter(
    prefix='/node',
    tags=['Nodes']
)
get_db = database.get_db

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_node(request: schemas.Node, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_node = models.Node(
        street_name=request.street_name,
        pwm=request.pwm,
        volt=request.volt,
        ampe=request.ampe,
        health=request.health,
        log=request.log,
        user_id=current_user.id  # Sử dụng user_id của người dùng hiện tại
    )
    db.add(new_node)
    db.commit()
    db.refresh(new_node)
    return new_node


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_node(id:int, db:Session=Depends(get_db)):
    node = db.query(models.Node).filter(models.Node.id == id)
    if not node.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Node with the id {id} is not found')
    node.delete(synchronize_session=False)
    db.commit()
    return 'done'


@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_node(id:int,request: schemas.Node,db: Session = Depends(get_db)):
    node = db.query(models.Node).filter(models.Node.id == id)
    if not node.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Node with the id {id} is not found')
    node.update(request.model_dump())
    db.commit()
    return 'updated'


@router.get('/{id}',status_code=200,response_model=schemas.ShowNode)
def show_node(id:int,db: Session = Depends(get_db)):
    node = db.query(models.Node).filter(models.Node.id == id).first()
    if not node:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Node with the id {id} is not available')
    return node


@router.get('/',response_model=List[schemas.ShowNode])
def all_node(db: Session = Depends(get_db)):
    nodes = db.query(models.Node).all()
    return nodes



# @router.put('/update_and_save/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update_and_save_node(id: int, request: schemas.NodeBase, db: Session = Depends(get_db)):
#     # Tìm node theo id
#     node = db.query(models.Node).filter(models.Node.id == id).first()

#     # Kiểm tra xem node có tồn tại không
#     if not node:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Node with id {id} is not found')

#     # Cập nhật các thông số của node
#     node.pwm = request.pwm
#     node.volt = request.volt
#     node.ampe = request.ampe
#     node.health = request.health
#     node.log = request.log

#     # Lưu thay đổi vào database
#     db.commit()
#     db.refresh(node)

#     # Tạo đường dẫn tới folder "node_data"
#     folder_name = 'node_data'
    
#     # Kiểm tra xem folder "node_data" đã tồn tại chưa, nếu chưa thì tạo mới
#     if not os.path.exists(folder_name):
#         os.makedirs(folder_name)

#     # Sử dụng uid của node để đặt tên file csv và lưu vào folder "node_data"
#     file_name = os.path.join(folder_name, f'{node.uid}.csv')

#     # Kiểm tra file đã tồn tại hay chưa
#     file_exists = os.path.isfile(file_name)

#     # Ghi dữ liệu vào file csv có tên là uid
#     with open(file_name, mode='a', newline='') as file:
#         writer = csv.writer(file)
        
#         # Nếu file chưa tồn tại, ghi tên cột trước
#         if not file_exists:
#             writer.writerow(['ID', 'PWM', 'Volt', 'Ampe', 'Health', 'Log'])

#         # Ghi dữ liệu của node
#         writer.writerow([node.id, node.pwm, node.volt, node.ampe, node.health, node.log])

#     return {"message": f"Node updated and state saved to {file_name}"}

@router.put('/update_and_save/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_and_save_node(id: int, request: schemas.NodeBase, db: Session = Depends(get_db)):
    # Tìm node theo id
    node = db.query(models.Node).filter(models.Node.id == id).first()

    # Kiểm tra xem node có tồn tại không
    if not node:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Node with id {id} is not found')

    # Cập nhật các trường nếu dữ liệu mới khác với dữ liệu hiện tại
    if request.pwm and request.pwm != node.pwm:
        node.pwm = request.pwm
    if request.volt and request.volt != node.volt:
        node.volt = request.volt
    if request.ampe and request.ampe != node.ampe:
        node.ampe = request.ampe
    if request.health and request.health != node.health:
        node.health = request.health
    if request.log and request.log != node.log:
        node.log = request.log

    # Lưu thay đổi vào database
    db.commit()
    db.refresh(node)

    # Tạo đường dẫn tới folder "node_data"
    folder_name = 'node_data'
    
    # Kiểm tra xem folder "node_data" đã tồn tại chưa, nếu chưa thì tạo mới
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Sử dụng uid của node để đặt tên file csv và lưu vào folder "node_data"
    file_name = os.path.join(folder_name, f'{node.uid}.csv')

    # Kiểm tra file đã tồn tại hay chưa
    file_exists = os.path.isfile(file_name)

    # Ghi dữ liệu vào file csv có tên là uid
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Nếu file chưa tồn tại, ghi tên cột trước
        if not file_exists:
            writer.writerow(['ID', 'PWM', 'Volt', 'Ampe', 'Health', 'Log'])

        # Chỉ ghi dữ liệu đã được cập nhật vào CSV
        writer.writerow([node.id, node.pwm, node.volt, node.ampe, node.health, node.log])

    return {"message": f"Node updated and state saved to {file_name}"}


from jsql import sql
from fastapi import HTTPException, status
from domain.utils.general import UserInfo, switch_role



def create_account(conn, user_info: UserInfo):
    
    row_count = switch_role(conn, user_info.user_id)
    if row_count == 0:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    sql(
        conn,
        """
            INSERT INTO `manager` (`user_id`)
            VALUES(:user_id)
        """,
        user_id = user_info.id
    )



def delet_manager(conn, user_info: UserInfo, manager_id):

    is_here = sql(
        conn,
        """
            SELECT COUNT(*) FROM `manager`
            WHERE `manager_id` = :id
        """,
        id = manager_id
    ).scalar()
    if is_here != 0:
        sql(
        conn,
        """
            DELETE FROM manager
            WHERE `manager_id` = :id
        """,
        id = manager_id
        
    ).lastrowid
    
    
def manager_details(conn, manager_id):
    data = sql(
        conn,
        """
            SELECT manager_id, company_permissions
            FROM manager
            WHERE manager_id =:manager_id 
        """,
        manager_id = manager_id
    ).dict()    
    return data




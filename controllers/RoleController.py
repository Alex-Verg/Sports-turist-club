from models.Role import Role


def role_from_base(cursor, needed_role):
    # TODO exception
    select_role = """SELECT *
                     FROM role
                     WHERE name = %s"""
    cursor.execute(select_role, (needed_role,))
    return Role(cursor.fetchall()[0])

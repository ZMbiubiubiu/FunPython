import pymysql 
import click 


@click.command()  # 装饰一个函数，使之成为一个命令行接口
# option 为其添加命令行选项
@click.option('--host', '-h', default='localhost', help="the host of mysql") # default 默认值
@click.option('--port', '-p',default=3306, help="the port of mysql")
@click.option('--user', '-u', prompt='Username') # 如果用户没有在命令行填入user，则提示用户输入
@click.option('--password', '-p', prompt='Password', hide_input=True) # hide_input 隐秘输入
@click.option('--db', prompt='Which db')
def connection(host, port, user, password, db):
    con = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        db=db,
        charset='utf8'
    )
    # 获取游标
    cursor = con.cursor()

    # 处理逻辑
    print("处理逻辑.....")

    # 批量插入
    # effect_row = cursor.executemany(
    #     'INSERT INTO `tbl_question_bank` (`question`, `right_answer`, `wrong_answer1`, `wrong_answer2`, `wrong_answer3`,`answer_analysis`) VALUES (%s, %s, %s, %s, %s, %s)',
    #     [(), ()]
    # )

    # 提交
    con.commit()

if __name__ == "__main__":
    connection()
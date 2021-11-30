from flask import Flask, request, jsonify
from time import sleep
import pymysql
conn = pymysql.connect(
    '127.0.0.1',
    'root',
    '1607439239',
    'mystorage',
    charset='utf8mb4',
)
cursor = conn.cursor()

app = Flask(__name__)


# record = 1


def execute_sql(sql):
    while 1:
        try:
            cursor.execute(sql)
            # global record
            # record += 1
            # if record % 8 == 0:
            #     conn.commit()
            break
        except:
            continue


# 登陆
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        num, pwd, name = request.json['num'], request.json['pwd'], request.json['nick']
        execute_sql('select name from wuziqiuser where number="%s" and pwd="%s"' % (num, pwd))
        if cursor.fetchone():
            execute_sql('update wuziqiuser set name="%s" where number="%s"' % (name, num))
            conn.commit()
            return 'ok'
        else:
            return 'error'


# 匹配请求
@app.route('/match', methods=['POST'])
def match():
    if request.method == 'POST':
        conn.ping(reconnect=True)
        # 查询是否有正在匹配的
        execute_sql('select game_id,user_first from wuziqigame where condi=0 limit 1')
        game = cursor.fetchone()
        if game:
            # 匹配成功
            execute_sql('update wuziqigame set user_second="%s", condi=1 where game_id="%d"' % (request.json['name'], game[0]))
            execute_sql('select name,info,record from wuziqiuser where number="%s"' % game[1])
            user_info = cursor.fetchone()
            return jsonify([game[0], user_info, 1])
        # 没有正在匹配的
        else:
            execute_sql('insert into wuziqigame(user_first, man_list, condi) values("%s", "[[], []]", 0)' % request.json['name'])
            execute_sql('select @@IDENTITY')
            game_id = cursor.fetchone()[0]
            # 循环等待15s
            for i in range(17):
                execute_sql('select game_id,user_second from wuziqigame where game_id="%d"' % game_id)
                second_name = cursor.fetchone()
                # 返回玩家昵称
                if second_name:
                    if second_name[1]:
                        execute_sql('select name,info,record from wuziqiuser where number="%s"' % second_name[1])
                        user_info = cursor.fetchone()
                        return jsonify([game_id, user_info, 0])
                    # 继续等待
                    sleep(1)
                else:
                    break
            # 超时，删除匹配记录
            execute_sql('delete from wuziqigame where game_id="%s"' % game_id)
            return 'no game'


# 取消匹配
@app.route('/give_up_match', methods=['POST'])
def give_up_match():
    if request.method == 'POST':
        conn.ping(reconnect=True)
        execute_sql('delete from wuziqigame where user_first="%s"' % request.json['name'])
        return '取消成功'


# 客户发送给服务器
@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        conn.ping(reconnect=True)
        game_id, pos, is_first = request.json['game_id'], request.json['pos'], request.json['is_first']
        # 超时
        execute_sql('select man_list from wuziqigame where game_id="%s"' % game_id)
        man_list = eval(cursor.fetchone()[0])
        player = 'first'
        if is_first:
            man_list[0].append(pos)
        else:
            man_list[1].append(pos)
            player = 'second'
        if request.json['pos'] != [-1, -1]:
            execute_sql('update wuziqigame set man_list="%s", last_in="%s", last_player="%s" where game_id="%s"' % (str(man_list), str(pos), player, game_id))
        else:
            execute_sql('update wuziqigame set last_in="%s", last_player="%s" where game_id="%s"' % (str(pos), player, game_id))
        return 'ok'


# 服务器转发给客户
@app.route('/recv', methods=['POST'])
def recv():
    if request.method == 'POST':
        conn.ping(reconnect=True)
        game_id, is_first = request.json['game_id'], request.json['is_first']
        if is_first:
            is_first = 'second'
        else:
            is_first = 'first'
        for i in range(40):
            execute_sql('select last_in from wuziqigame where game_id="%s" and last_player="%s"' % (game_id, is_first))
            last_in = cursor.fetchone()
            if last_in:
                return jsonify(last_in[0])
            else:
                sleep(0.5)
        return 'timeout'


# 请求用户信息
@app.route('/get_conf', methods=['POST'])
def get_conf():
    if request.method == 'POST':
        num = request.json['num']
        execute_sql('select name,info,record from wuziqiuser where number="%s"' % num)
        data = cursor.fetchone()
        return jsonify(data)


# 修改用户信息
@app.route('/set_conf', methods=['POST'])
def set_conf():
    if request.method == 'POST':
        num = request.json['num']
        if request.json.get('man'):
            info = [request.json['man'], request.json['bg'], request.json['avatar']]
            execute_sql('update wuziqiuser set info="%s" where number="%s"' % (str(info), num))
        if request.json.get('name'):
            name = request.json['name']
            execute_sql('update wuziqiuser set name="%s" where number="%s"' % (name, num))
        conn.commit()
        return 'ok'


app.run(debug=True)

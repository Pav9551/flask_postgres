import requests
import psycopg2
import json
from datetime import datetime as dt
from flask import Flask, request, jsonify
def addtobase(host="postg_jser", port=5432, num = 3):
    conn = psycopg2.connect(host=host, port=port, dbname="main", user="root", password="1234")
    try:
        cur = conn.cursor()
        #количество строк в таблице
        cur.execute("SELECT count(*) FROM public.raw_quiz_data")
        row_count = cur.fetchall()[0][0]
        if (row_count == 0):
            max_count = 0
            pak = []
            tupleid = []
            #print("empty")
        else:
            #значение метки последней пачки
            cur.execute("SELECT MAX(count) FROM public.raw_quiz_data")
            max_count = cur.fetchall()[0][0] 
            #запрос последней пачки зная метку
            cur.execute("SELECT id, answer, question, created_at, count FROM public.raw_quiz_data WHERE count = %s", (max_count,))
            pak = cur.fetchall()    
            #добавление новой пачки 
            #запрос кортежей существующих ID
            cur.execute("SELECT id FROM public.raw_quiz_data")
            tupleid = cur.fetchall()
            #запрашиваем новые данные
        flag = True
        path = 'https://jservice.io/api/random?count='+str(num)
        while(flag):
            req = requests.get(path)
            new_id = []
            #print(tupleid)
            #создаем список кортежей добавляемых id
            for elem in json.loads(req.text):
                new_id.append(tuple([elem['id'],]) )
                #print(elem['id'])
            #print(new_id)
            set_new_id = set(new_id)
            set_tupleid = set(tupleid)
            #проверяем на повторы 
            if (len(set_new_id & set_tupleid) == 0):
                #повторов нет, то добавляем данные
                for elem in json.loads(req.text):
                    cur.execute("""
                    INSERT INTO public.raw_quiz_data(id, answer, question, created_at, count)
                    VALUES(%s, %s, %s, %s, %s)
                    """, [
                          elem["id"]
                          , elem["answer"]
                          , elem["question"]
                          , elem["created_at"]
                          , max_count + 1
                    ]) 
                    conn.commit()      
                #print("ok")
                flag = False      
        return (pak)
    except:#psycopg2.errors.InFailedSqlTransaction:
        conn.rollback()
        return ([])    

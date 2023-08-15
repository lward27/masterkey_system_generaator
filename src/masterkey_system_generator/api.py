from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from generator import MasterKeySystemGen
import uuid
import psycopg2
import psycopg2.extras

app = FastAPI()
connection = psycopg2.connect(
    host="172.17.0.3",
    database="masterkey_system_generator",
    user="postgres",
    password="topsecretpassword",
)
psycopg2.extras.register_uuid()

@app.on_event("shutdown")
def shutdown_event():
    connection.close()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/generate")
async def get_generate(
    great_grand_master_key:str, 
    rotation:str,
    number_of_pins:int,
    key_bitting_array_1:str,
    key_bitting_array_2:str,
    key_bitting_array_3:str,
    key_bitting_array_4:str,
    key_bitting_array_5:str | None = None,
    number_of_masters:int = Query(16, enum=[16, 64]), 
    maximum_adjacent_cuts:int = 7
    ):
    combined_key_bitting_array = []
    combined_key_bitting_array.append([eval(i) for i in list(key_bitting_array_1)])
    combined_key_bitting_array.append([eval(i) for i in list(key_bitting_array_2)])
    combined_key_bitting_array.append([eval(i) for i in list(key_bitting_array_3)])
    combined_key_bitting_array.append([eval(i) for i in list(key_bitting_array_4)])
    combined_key_bitting_array.append([eval(i) for i in list(key_bitting_array_5)]) if key_bitting_array_5 else None
    kBA_length = len(combined_key_bitting_array)
    # print([eval(i) for i in list(great_grand_master_key)])
    # print([eval(i) for i in list(rotation)])
    # print(combined_key_bitting_array)
    # print(number_of_pins)
    # print(kBA_length)
    # print(number_of_masters)
    # print(maximum_adjacent_cuts)
    mks = MasterKeySystemGen([eval(i) for i in list(great_grand_master_key)], [eval(i) for i in list(rotation)], combined_key_bitting_array, number_of_pins, kBA_length, number_of_masters, maximum_adjacent_cuts)
    generator_output = mks.build_iterator()
    mks = {
            "id":mks.id,
            "great_grand_master_key":great_grand_master_key,
            "rotation":rotation,
            "key_bitting_array_1":key_bitting_array_1,
            "key_bitting_array_2":key_bitting_array_2,
            "key_bitting_array_3":key_bitting_array_3,
            "key_bitting_array_4":key_bitting_array_4,
            "key_bitting_array_5":key_bitting_array_5,
            "number_of_pins":number_of_pins,
            "kBA_length":kBA_length,
            "page_master_count":number_of_masters,
            "maximum_adjacent_cuts":maximum_adjacent_cuts,
        }
    cur = connection.cursor()
    cur.execute(
        """INSERT INTO masterkey_system (
            id, great_grand_master_key, rotation, key_bitting_array_1, key_bitting_array_2, 
            key_bitting_array_3, key_bitting_array_4, key_bitting_array_5, number_of_pins, 
            kBA_length, page_master_count, maximum_adjacent_cuts, created_on) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)""", 
        (mks["id"], mks["great_grand_master_key"], mks["rotation"], mks["key_bitting_array_1"], 
        mks["key_bitting_array_2"], mks["key_bitting_array_3"], mks["key_bitting_array_4"], 
        mks["key_bitting_array_5"], mks["number_of_pins"], mks["kBA_length"],
        mks["page_master_count"], mks["maximum_adjacent_cuts"],)
        )

    batch_oh_keys = [tuple(d.values()) for d in generator_output]
    psycopg2.extras.execute_batch(cur, "INSERT INTO bitting (id, blind_code, bitting, top_pin, bottom_pin, state, master_key_system, great_grand_master, row_master, page_master, page_block_master, page_group_master, page_section_master, block_master, key_level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", batch_oh_keys)
    connection.commit()
    cur.close()
    return mks

@app.get("/list/systems")
async def list_systems():
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query_sql = "SELECT * FROM masterkey_system;" 
    cur.execute(query_sql)
    results = cur.fetchall()
    cur.close()
    return results

@app.get("/retrieve/system")
async def retrieve_system(masterkey_system_id: uuid.UUID):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM bitting WHERE master_key_system = (%s);", (masterkey_system_id,))
    results = cur.fetchall()
    cur.close()
    return results

@app.get("/retrieve/system/great_grand_master")
async def retrieve_great_grand_master(masterkey_system_id: uuid.UUID):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM bitting WHERE master_key_system = (%s) AND key_level = 'Great Grand Master';", (masterkey_system_id,))
    results = cur.fetchall()
    cur.close()
    return results

@app.get("/retrieve/system/page_section_masters")
async def retrieve_system_page_section_masters(masterkey_system_id: uuid.UUID):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM bitting WHERE master_key_system = (%s) AND key_level = 'Page Section Master';", (masterkey_system_id,))
    results = cur.fetchall()
    cur.close()
    return results

@app.get("/retrieve/system/page_group_masters")
async def retrieve_system_page_group_masters(masterkey_system_id: uuid.UUID):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM bitting WHERE master_key_system = (%s) AND key_level = 'Page Group Master';", (masterkey_system_id,))
    results = cur.fetchall()
    cur.close()
    return results

@app.get("/retrieve/system/page_block_masters")
async def retrieve_system_page_block_masters(masterkey_system_id: uuid.UUID):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM bitting WHERE master_key_system = (%s) AND key_level = 'Page Block Master';", (masterkey_system_id,))
    results = cur.fetchall()
    cur.close()
    return results

@app.get("/retrieve/system/page_masters")
async def retrieve_system_page_masters(masterkey_system_id: uuid.UUID):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM bitting WHERE master_key_system = (%s) AND key_level = 'Page Master';", (masterkey_system_id,))
    results = cur.fetchall()
    cur.close()
    return results

@app.get("/retrieve/system/row_masters")
async def retrieve_system_row_masters(masterkey_system_id: uuid.UUID):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM bitting WHERE master_key_system = (%s) AND key_level = 'Row Master';", (masterkey_system_id,))
    results = cur.fetchall()
    cur.close()
    return results

@app.get("/retrieve/system/block_masters")
async def retrieve_system_block_masters(masterkey_system_id: uuid.UUID):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM bitting WHERE master_key_system = (%s) AND key_level = 'Block Master';", (masterkey_system_id,))
    results = cur.fetchall()
    cur.close()
    return results

@app.get("/retrieve/system/change_keys")
async def retrieve_system_change_keys(masterkey_system_id: uuid.UUID, page_master_id: uuid.UUID):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM bitting WHERE master_key_system = (%s) AND page_master = (%s) AND key_level = 'Change Key';", (masterkey_system_id, page_master_id,))
    results = cur.fetchall()
    cur.close()
    return results



# mk = MasterKeySystemGen([3,5,2,4,6,7], [1, 2, 3, 4, 5, 6], [[1, 3, 5, 6, 2, 4],[4, 5, 2, 3, 1, 6],[1, 2, 3, 4, 5, 6],[6, 4, 3, 5, 2, 1]], 6, 4, 16, 7)
# system_output = mk.build_iterator()

# @app.get("/info")
# async def get_info(ticker_name: str):
#     tick = yf.Ticker(ticker_name)
#     return tick.info

# @app.get("/history")
# async def get_history(ticker_name: str, period: str, return_type: str = Query("dict", enum=["dict", "html", "text", "dataframe"])):
#     tick = yf.Ticker(ticker_name)
#     hist = tick.history(period="1mo")
#     if return_type == "dict":
#         return hist.to_dict()
#     if return_type == "html":
#         return HTMLResponse(content=hist.to_html(),status_code=200)
#     if return_type == "text":
#         return hist.to_string()
#     if return_type == "dataframe":
#         return hist
import pymongo
from flask import Flask, request, jsonify
from bson import ObjectId

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['teste']
collection = db["voucher"]

@app.route('/api/salvar', methods=['POST'])
def create_voucher():
    data = request.get_json()
    voucher = {"Celular": data['Celular'], "Mei": data['Mei']}
    collection.insert_one(voucher).inserted_id
    return jsonify({'Mensagem': 'Cadastrado com Sucesso!'})

@app.route('/api/vouchers', methods=['GET'])
def read_all_vouchers():
   data = list(collection.find())
   for item in data:
        item['_id'] = str(item['_id'])
   return jsonify(data)

@app.route('/api/voucher/<mei>', methods=['GET'])
def read_one_voucher(mei):
    voucher = collection.find_one({"Mei": mei})
    if voucher:
        voucher['_id'] = str(voucher['_id'])
        return jsonify(voucher)
    else:
        return jsonify({"Mensagem": "Mei nao Encontrado"}, 404)

@app.route('/api/voucher/<mei>', methods=['DELETE'])
def delete_voucher(mei):
    query = {"Mei": mei}
    result = collection.delete_one(query)
    if result.deleted_count > 0:
        return jsonify({"menssagem": "Mei deletado com Sucesso"})
    else:
        return jsonify({"menssagem": "Mei não encontrado!"}, 404)

@app.route('/api/voucher/<mei>', methods=['PATCH'])
def update_voucher(mei):
    data = request.get_json()
    query = {"Mei": int(mei)}
    update_operation = {"$set": data}
    result = collection.update_one(query, update_operation)

    if result.modified_count > 0:
        return jsonify({'Mensagem': 'Update com Sucesso!'})
    else:
        return jsonify({'Mensagem': 'Nenhum documento foi atualizado'}, 404)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request, send_file
import os

app = Flask(__name__)

ICONS_FOLDER = os.path.join(os.getcwd(), 'icons')
app.config['ICONS_FOLDER'] = ICONS_FOLDER

'''
{
  "id": 0,
  "name": "string",
  "description": "string",
  "icon": "string
}
'''

products = []

def get_id():
    num = len(products)
    while True:
        num += 1
        yield num

id_generator = get_id()


@app.route('/product', methods=['POST'])
def add_product():
    request_data = request.get_json()
    request_keys = request_data.keys()

    if 'name' not in request_keys or\
            'description' not in request_keys:
        
        return jsonify(message='Error: Requset must contain name and description'), 400
    
    product = {
        'id': next(id_generator),
        'name': request_data['name'],
        'description': request_data['description'],
        'icon': ''
    }

    products.append(product)
    return jsonify(product), 200


@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    for product in products:
        if product['id'] == id:
            return jsonify(product), 200
        
    return jsonify(message=f'Error: Product id={id} not found'), 400


@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    for product in products:
        if product['id'] == id:
            request_data = request.get_json()
            request_keys = request_data.keys()
            
            for key in request_keys:
                product[key] = request_data[key]

            return jsonify(product), 200
        
    return jsonify(message=f'Error: Product id={id} not found'), 400


@app.route('/product/<int:id>', methods=['DELETE'])
def del_product(id):
    for product in products:
        if product['id'] == id:
            products.remove(product)

            return jsonify(product), 200
        
    return jsonify(message=f'Error: Product id={id} not found'), 400


@app.route('/products', methods=['GET'])
def get_products_list():
    return jsonify(products)


@app.route('/product/<int:id>/image', methods=['POST'])
def upload_icon(id):
    for product in products:
        if product['id'] == id:
            if 'icon' not in request.files:
                return jsonify(message=f'Error: No icon in request'), 400    
            
            icon = request.files['icon']
            if icon.filename == '':
                return jsonify(message=f'Error: No icon is selected'), 400    
            
            icon_path = os.path.join(app.config['ICONS_FOLDER'], icon.filename)
            icon.save(icon_path)
            product['icon'] = icon.filename

            return jsonify(message=f'Icon for product id={id} uploaded successfully'), 200
        
    return jsonify(message=f'Error: Product id={id} not found'), 400


@app.route('/product/<int:id>/image', methods=['GET'])
def get_icon(id):
    for product in products:
        if product['id'] == id:
            image_path = os.path.join(ICONS_FOLDER, product['icon'])
            if os.path.exists(image_path):
                return send_file(image_path, mimetype='image/png'), 200
            
    return jsonify(message=f'Error: Product id={id} not found'), 400

if __name__ == '__main__':
    app.run(debug=True)

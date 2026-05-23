from flask import Flask, render_template, request, redirect, url_for, session
from agent import agent, format_response # Al importar agent se ejecuta todo el script agent.py
import uuid

# __name__ es el nombre del script.
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Definimos las rutas.
# Devolvemos una plantilla que está en el
# directorio templates (tiene que llamarse templates)
@app.route('/')
def home():
    session['thread_id'] = str(uuid.uuid4())
    if 'messages' not in session:
        session['messages'] = []
    print('home', session)
    return render_template('chat.html', messages=session['messages'])

# Esta función va a invocar al agente.
@app.route('/send', methods=['POST'])
def send():
    user_message = request.form['message']
    user_lat = request.form.get('latitude')
    user_lon = request.form.get('longitude')
    print(user_lat, user_lon)
    
    if user_lat and user_lon:
        session['user_location'] = {'lat': user_lat, 'lon': user_lon}
    
    response = agent.invoke({"messages": [{'role': 'user', 'content':user_message}]}, 
                        {"configurable": {"thread_id":session['thread_id']}})
    
    # session sirve como un almacenamiento de data del usuario,
    # como los mensajes, la conversación, etc.
    # Se guarda en las cookies del usuario.
    session['messages'].append({'type': 'human', 'content': user_message})
    session['messages'].append({'type': 'ai', 'content': format_response(response['messages'][-1].content)})
    session.modified = True
    print(session)
    return redirect(url_for('home'))

app.run(debug=True)
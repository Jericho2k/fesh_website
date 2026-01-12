from flask import Flask, render_template, request
from datetime import datetime, timedelta
import os
from collections import Counter, defaultdict
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/track/<action>', methods=['POST'])
def track(action):
    log_file = 'stats.log'
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now()}: {action}\n")
    return '', 204

@app.route('/healthz')
def healthz():
    return '', 200

@app.route('/stats101')
def stats():
    log_file = 'stats.log'
    stats_data = {'visit': 0, 'appstore': 0, 'playmarket': 0, 'email': 0, 'telegram': 0}
    daily_stats = defaultdict(lambda: {'visit': 0, 'appstore': 0, 'playmarket': 0, 'email': 0, 'telegram': 0})
    recent_activity = []
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split(': ')
                if len(parts) >= 2:
                    timestamp_str = ': '.join(parts[:-1])
                    action = parts[-1].strip()
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace(' ', 'T'))
                        date_key = timestamp.strftime('%Y-%m-%d')
                        if action in stats_data:
                            stats_data[action] += 1
                            daily_stats[date_key][action] += 1
                        recent_activity.append({'timestamp': timestamp, 'action': action})
                    except:
                        pass
    
    # Get last 7 days
    last_7_days = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    daily_chart_data = {
        'dates': last_7_days,
        'visits': [daily_stats[date]['visit'] for date in last_7_days],
        'clicks': [sum(daily_stats[date].values()) - daily_stats[date]['visit'] for date in last_7_days]
    }
    
    # Recent activity (last 10)
    recent_activity = sorted(recent_activity, key=lambda x: x['timestamp'], reverse=True)[:10]
    
    # Conversion rates
    total_visits = stats_data['visit']
    conversion_rates = {
        'appstore': (stats_data['appstore'] / total_visits * 100) if total_visits > 0 else 0,
        'playmarket': (stats_data['playmarket'] / total_visits * 100) if total_visits > 0 else 0,
        'email': (stats_data['email'] / total_visits * 100) if total_visits > 0 else 0,
        'telegram': (stats_data['telegram'] / total_visits * 100) if total_visits > 0 else 0
    }
    
    return render_template('stats.html', 
                         stats=stats_data, 
                         daily_chart=json.dumps(daily_chart_data),
                         recent_activity=recent_activity,
                         conversion_rates=conversion_rates)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
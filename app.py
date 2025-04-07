from flask import Flask, request, jsonify, render_template
import sys
import traceback
from tax_calculator import calculate_tax

app = Flask(__name__)
app.debug = False

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Error rendering index: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        try:
            # 从请求中获取数据，如果不存在则使用默认值
            salary = float(data.get('salary', 0))
            salary_type = data.get('salary_type', 'monthly')
            bonus = float(data.get('bonus', 0))
            bonus_type = data.get('bonus_type', 'separate')
            labor_income = float(data.get('labor_income', 0))
            manuscript_income = float(data.get('manuscript_income', 0))
            license_income = float(data.get('license_income', 0))
            social_security_base = float(data.get('social_security_base', 0))
            housing_fund_rate = float(data.get('housing_fund_rate', 0))
            special_deductions = data.get('special_deductions', {})
            
            # 调用计算函数
            result = calculate_tax(
                salary=salary,
                salary_type=salary_type,
                bonus=bonus,
                bonus_type=bonus_type,
                labor_income=labor_income,
                manuscript_income=manuscript_income,
                license_income=license_income,
                social_security_base=social_security_base,
                housing_fund_rate=housing_fund_rate,
                special_deductions=special_deductions
            )
            
            return jsonify({'success': True, 'result': result})
            
        except ValueError as e:
            return jsonify({'error': f'Invalid numeric input: {str(e)}'}), 400
            
    except Exception as e:
        app.logger.error(f"Error in calculate: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False) 
from flask import Flask, render_template, request, jsonify
import sys
import os

# 添加父目录到系统路径以导入tax_calculator模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tax_calculator import calculate_tax

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        # 从请求中获取数据
        salary = float(data.get('salary', 0))
        salary_type = data.get('salary_type', 'monthly')
        bonus = float(data.get('bonus', 0))
        bonus_type = data.get('bonus_type', 'separate')
        labor_income = float(data.get('labor_income', 0))
        manuscript_income = float(data.get('manuscript_income', 0))
        license_income = float(data.get('license_income', 0))
        
        # 获取扣除信息
        social_security_base = float(data.get('social_security_base', 0))
        housing_fund_rate = float(data.get('housing_fund_rate', 0))
        special_deductions = {
            'children_education': float(data.get('children_education', 0)),
            'continuing_education': float(data.get('continuing_education', 0)),
            'housing_loan': float(data.get('housing_loan', 0)),
            'housing_rent': float(data.get('housing_rent', 0)),
            'elderly_care': float(data.get('elderly_care', 0))
        }
        
        # 计算个税
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
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True) 